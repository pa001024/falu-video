"""
逐行合成旁白（GPT-SoVITS v2 底模 · 零样本），并用 FunASR 回听校验。

运行：E:/soft/GPT-SoVITS-v2/runtime/python.exe synth.py [--force] [--only 05,06] [--speed 1.33]
产出：tts/wav/sNN_LL.wav（32 kHz 单声道、首尾静音已修剪）＋ tts/manifest.json

`--speed` 走的是 VITS 文本编码器的时长插值（不是重采样），**音高不变、只把时间压紧**；
非 1 的语速会切到串行推理路径，必须配 `--force` 才能覆盖已有音频。
"""
import argparse
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(HERE)
GSV_ROOT = r"E:\soft\GPT-SoVITS-v2"

os.chdir(GSV_ROOT)
sys.path.insert(0, GSV_ROOT)
sys.path.insert(0, os.path.join(GSV_ROOT, "GPT_SoVITS"))
sys.path.insert(0, PROJECT)
os.environ["PATH"] = os.path.join(GSV_ROOT, "runtime", "ffmpeg", "bin") + os.pathsep + os.environ["PATH"]

import re  # noqa: E402

import numpy as np  # noqa: E402
import soundfile as sf  # noqa: E402
from pypinyin import Style, pinyin  # noqa: E402

from narration import iter_lines, to_tts  # noqa: E402

# 参考音色：仆人（阿蕾奇诺）原声，由 assets/ref_audio.mp3 截取首句 0–7.30s（32 kHz 单声道）
REF_WAV = os.path.join(HERE, "ref_father.wav")
REF_TEXT = "我是愚人众执行官第四席，仆人阿蕾奇诺，也是壁炉之家的孩子们口中的父亲。"
WAV_DIR = os.path.join(HERE, "wav")
MANIFEST = os.path.join(HERE, "manifest.json")
SR = 32000
MAX_ATTEMPTS = 5
ACCEPT_SER = 0.06


def cache_key(speed: float, tts: str) -> str:
    """
    合成缓存的键：语速与口播文本共同决定一段音频。
    @param speed 语速倍率
    @param tts 口播文本
    @returns 缓存键
    """
    return f"{speed:g}|{tts}"


def pinyin_seq(text: str) -> list:
    """
    把文本转换成「每字可能读音集合」的序列（只取汉字），多音字取全部读音，
    这样「地/的」「溯/宿」「行/航」这类 ASR 同音写法不会被误判。
    @param text 任意文本（ASR 输出中的阿拉伯数字先按口播规则转中文）
    @returns 读音集合列表
    """
    han = "".join(ch for ch in to_tts(text) if "\u4e00" <= ch <= "\u9fff")
    return [set(p) | {"de"} if ch in "地的得" else set(p)
            for ch, p in zip(han, pinyin(han, style=Style.NORMAL, heteronym=True))]


def edit_distance(a: list, b: list) -> int:
    """
    计算两个读音集合序列的编辑距离，两字读音集合有交集即视为相同。
    @param a 序列 A
    @param b 序列 B
    @returns 最少编辑次数
    """
    prev = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        cur = [i] + [0] * len(b)
        for j, y in enumerate(b, 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (0 if x & y else 1))
        prev = cur
    return prev[-1]


def line_ser(target_text: str, heard: str) -> float:
    """
    计算音节错误率。目标含英文（如「Q」「boss」）时，ASR 会把它听成一两个汉字，额外放宽 1 个音节。
    @param target_text 口播文本
    @param heard ASR 转写
    @returns 音节错误率
    """
    target = pinyin_seq(target_text)
    dist = edit_distance(target, pinyin_seq(heard))
    if re.search(r"[A-Za-z]", target_text):
        dist = max(0, dist - 1)
    return dist / max(1, len(target))


def trim_silence(audio: np.ndarray, threshold_db: float = -42.0, margin: float = 0.04) -> np.ndarray:
    """
    修剪首尾静音，保留少量余量避免吞字。
    @param audio 单声道浮点音频
    @param threshold_db 静音判定阈值（相对满幅 dBFS）
    @param margin 首尾保留的秒数
    @returns 修剪后的音频
    """
    frame = int(SR * 0.01)
    if audio.size < frame * 3:
        return audio
    n = audio.size // frame
    rms = np.sqrt(np.mean(audio[: n * frame].reshape(n, frame) ** 2, axis=1) + 1e-12)
    db = 20 * np.log10(rms)
    voiced = np.where(db > threshold_db)[0]
    if voiced.size == 0:
        return audio
    pad = int(SR * margin)
    start = max(0, voiced[0] * frame - pad)
    end = min(audio.size, (voiced[-1] + 1) * frame + pad)
    return audio[start:end]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="忽略缓存全部重合成")
    parser.add_argument("--only", default="", help="只处理指定镜号，逗号分隔")
    parser.add_argument("--redo-bad", action="store_true", help="对已有但 SER 超阈的行换种子重试")
    parser.add_argument("--speed", type=float, default=1.0,
                        help="整体语速倍率（>1 更快）。非 1 时走串行推理，且必须配 --force 才会全量重合成")
    args = parser.parse_args()
    only = {int(x) for x in args.only.split(",") if x.strip()}

    os.makedirs(WAV_DIR, exist_ok=True)
    by_tts = {}
    if os.path.exists(MANIFEST):
        with open(MANIFEST, "r", encoding="utf-8") as fp:
            for e in json.load(fp):
                path = os.path.join(PROJECT, e["file"])
                if os.path.exists(path):
                    # 按「语速 + 口播文本」缓存：行号平移不必重合成，语速一变自动失效
                    e["_bytes"] = open(path, "rb").read()
                    by_tts[cache_key(e.get("speed", 1.0), e["tts"])] = e

    from TTS_infer_pack.TTS import TTS, TTS_Config
    from funasr import AutoModel

    tts = TTS(TTS_Config(os.path.join(HERE, "tts_infer.yaml")))
    asr_dir = os.path.join(GSV_ROOT, "tools", "asr", "models")
    asr = AutoModel(
        model=os.path.join(asr_dir, "speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch"),
        model_revision="v2.0.4",
        disable_update=True,
    )

    entries = []
    t0 = time.time()
    for sid, idx, item in iter_lines():
        key = f"{sid:02d}_{idx:02d}"
        wav_path = os.path.join(WAV_DIR, f"s{key}.wav")
        ckey = cache_key(args.speed, item["tts"])
        hit = by_tts.get(ckey)
        have = hit is not None
        if have:
            cached = {k: v for k, v in hit.items() if k != "_bytes"}
            with open(wav_path, "wb") as fp:
                fp.write(hit["_bytes"])
            cached.update({
                "shot": sid, "line": idx, "display": item["display"], "text": item["text"], "pause": item["pause"],
                "file": os.path.relpath(wav_path, PROJECT).replace("\\", "/"),
                "ser": round(line_ser(item["tts"], cached["heard"]), 4),
            })
        if only and sid not in only:
            if have:
                entries.append(cached)
            continue
        if have and not args.force and (cached["ser"] <= ACCEPT_SER or not args.redo_bad):
            entries.append(cached)
            continue

        n_target = len(pinyin_seq(item["tts"]))
        best = None
        first_attempt = 0
        if have and not args.force:
            # 已有成品但仍超阈：作为候选参与比较，换一批种子重试
            keep = wav_path + ".keep.wav"
            os.replace(wav_path, keep)
            best = {"score": cached["ser"], "ser": cached["ser"], "dur": cached["duration"], "heard": cached["heard"],
                    "tmp": keep, "attempt": cached["attempt"], "seed": cached["seed"]}
            first_attempt = max(cached["attempt"] + 1, 10)
        for attempt in range(first_attempt, first_attempt + MAX_ATTEMPTS):
            seed = 1000 + sid * 100 + idx * 7 + attempt * 9973
            req = {
                "text": item["tts"],
                "text_lang": "zh",
                "ref_audio_path": REF_WAV,
                "prompt_text": REF_TEXT,
                "prompt_lang": "zh",
                "top_k": 15,
                "top_p": 1.0,
                "temperature": 1.0 if attempt == 0 else 0.8,
                "text_split_method": "cut0",
                "batch_size": 1,
                "speed_factor": args.speed,
                "fragment_interval": 0.2,
                "seed": seed,
                "parallel_infer": True,
                "repetition_penalty": 1.35,
                "return_fragment": False,
            }
            sr, audio = next(tts.run(req))
            if np.issubdtype(audio.dtype, np.integer):
                audio = audio.astype(np.float32) / 32768.0
            audio = trim_silence(audio.astype(np.float32))
            tmp_path = wav_path + f".try{attempt}.wav"
            sf.write(tmp_path, audio, sr)
            heard = "".join(r.get("text", "") for r in asr.generate(input=tmp_path)).replace(" ", "")
            ser = line_ser(item["tts"], heard)
            dur = audio.size / sr
            per_char = dur / max(1, n_target)
            sane = 0.13 <= per_char <= 0.38
            score = ser + (0 if sane else 0.5)
            print(f"{key} try{attempt} ser={ser:.3f} dur={dur:.2f}s {per_char:.3f}s/字 | {heard}", flush=True)
            if best is None or score < best["score"]:
                if best is not None and os.path.exists(best["tmp"]):
                    os.remove(best["tmp"])
                best = {"score": score, "ser": ser, "dur": dur, "heard": heard, "tmp": tmp_path,
                        "attempt": attempt, "seed": seed}
            else:
                os.remove(tmp_path)
            if ser <= ACCEPT_SER and sane:
                break

        os.replace(best["tmp"], wav_path)
        entry = {
            "shot": sid, "line": idx, "text": item["text"], "display": item["display"],
            "tts": item["tts"], "pause": item["pause"], "speed": args.speed,
            "file": os.path.relpath(wav_path, PROJECT).replace("\\", "/"),
            "duration": round(best["dur"], 4), "ser": round(best["ser"], 4), "heard": best["heard"],
            "attempt": best["attempt"], "seed": best["seed"],
        }
        entries.append(entry)
        with open(MANIFEST, "w", encoding="utf-8") as fp:
            json.dump(entries, fp, ensure_ascii=False, indent=1)

    with open(MANIFEST, "w", encoding="utf-8") as fp:
        json.dump(entries, fp, ensure_ascii=False, indent=1)
    referenced = {os.path.basename(e["file"]) for e in entries}
    for name in os.listdir(WAV_DIR):
        if name.endswith(".wav") and name not in referenced:
            os.remove(os.path.join(WAV_DIR, name))
    total = sum(e["duration"] for e in entries)
    bad = [e for e in entries if e["ser"] > ACCEPT_SER]
    print(f"完成 {len(entries)} 行，语音合计 {total:.1f}s，用时 {time.time() - t0:.0f}s；SER 超阈 {len(bad)} 行")
    for e in bad:
        print(f"  {e['shot']:02d}_{e['line']:02d} ser={e['ser']:.3f} 期望={e['tts']} 听到={e['heard']}")


if __name__ == "__main__":
    main()
