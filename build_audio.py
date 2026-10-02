"""
把 timing.json 排好的全部旁白直排成全片音轨（采样级对齐），输出 renders/track.wav。

不依赖 adelay / amix：直接按「镜头起 + 行起」把每句采样写进全片缓冲区，
既能避免滤镜图在不同声道数下行为不一致，也便于逐点校验。

全片只有人声，不加任何转场音效。

用法：
  python build_audio.py            # 生成 renders/track.wav
  python build_audio.py --check    # 回读文件逐句比对，并校验句子不越镜头边界
"""
from __future__ import annotations

import argparse
import json
import math
import subprocess
import wave
from array import array
from pathlib import Path

HERE = Path(__file__).parent
RENDERS = HERE / "renders"
TIMING = json.loads((HERE / "timing.json").read_text(encoding="utf-8"))
FFPROBE = Path("E:/soft/GPT-SoVITS-v2/runtime/ffmpeg/bin/ffprobe.exe")
# 与 TTS 源采样率一致，全程不做重采样
SR = 32000
# 每句首尾的淡入淡出时长（秒），消除拼接爆音
FADE = 0.012
# 音轨比画面多出的余量（秒），让 -shortest 以画面长度为准
MARGIN = 1.0
# 峰值上限，避免 AAC 编码过冲
PEAK_LIMIT = 31000
# 句首底噪裁剪：TTS 个别句子开头带半秒上下的底噪，会让语音晚于字幕出现
ONSET_WIN = int(0.1 * SR)
ONSET_RMS = 600
ONSET_MAX_TRIM = 0.9
ONSET_MIN_TRIM = 0.08


def trim_lead(src: array) -> int:
    """
    裁掉句首的底噪段，让语音尽量贴在计划起点上。
    @param src 单声道采样，原地修改
    @returns 丢弃的采样数（未达阈值则为 0）
    """
    limit = min(len(src) - ONSET_WIN, int(ONSET_MAX_TRIM * SR))
    cut = 0
    for i in range(0, max(0, limit), ONSET_WIN // 2):
        seg = src[i:i + ONSET_WIN]
        if (sum(x * x for x in seg) / len(seg)) ** 0.5 > ONSET_RMS:
            cut = i
            break
    if cut < int(ONSET_MIN_TRIM * SR):
        return 0
    del src[:cut]
    return cut


def read_mono(path: Path) -> tuple[array, int]:
    """
    读取单声道 16bit WAV 采样。
    @param path 文件路径
    @returns (采样数组, 采样率)
    """
    with wave.open(str(path), "rb") as w:
        if w.getsampwidth() != 2:
            raise ValueError(f"{path} 不是 16bit 采样")
        nch = w.getnchannels()
        samples = array("h")
        samples.frombytes(w.readframes(w.getnframes()))
        if nch > 1:
            samples = array("h", samples[::nch])
        return samples, w.getframerate()


def shot_starts() -> tuple[list[float], float]:
    """
    按已渲染画面的实际时长累加出各镜起始时刻。渲染每镜会比计划多出约 1 帧，
    若沿用计划起始，全片末尾会累积约 0.3 秒的音画偏差。
    @returns (各镜起始时刻列表, 全片实际总长)
    """
    starts, cursor = [], 0.0
    for shot in TIMING["shots"]:
        starts.append(cursor)
        video = RENDERS / f"S{shot['id']:02d}.mp4"
        dur = shot["duration"]
        if video.exists():
            res = subprocess.run(
                [str(FFPROBE), "-v", "error", "-show_entries", "format=duration",
                 "-of", "default=nw=1:nk=1", str(video)],
                capture_output=True, text=True,
            )
            try:
                dur = float(res.stdout.strip())
            except ValueError:
                pass
        cursor += dur
    return starts, cursor


def main() -> None:
    parser = argparse.ArgumentParser(description="直排全片音轨")
    parser.add_argument("--check", action="store_true", help="回读校验")
    args = parser.parse_args()

    starts, total = shot_starts()
    n = math.ceil((total + MARGIN) * SR)
    buf = array("h", bytes(2 * n))

    placed: list[tuple[int, float, int, array]] = []
    # 句子必须落在所属镜头内，否则说明调度或时间轴有误
    overflow = []
    trimmed = 0
    for shot, base in zip(TIMING["shots"], starts):
        shot_end = base + shot["duration"]
        for c in shot["cues"]:
            src, src_sr = read_mono(HERE / c["file"])
            if src_sr != SR:
                raise ValueError(f"{c['file']} 采样率 {src_sr} ≠ {SR}")
            trimmed += trim_lead(src)
            if base + c["start"] + len(src) / SR > shot_end + 1e-6:
                overflow.append((shot["id"], c["start"], c["file"]))
            fade = min(int(FADE * SR), len(src) // 2)
            for i in range(fade):
                g = i / fade
                src[i] = int(src[i] * g)
                src[-1 - i] = int(src[-1 - i] * g)
            off = round((base + c["start"]) * SR)
            if off + len(src) > len(buf):
                buf.extend(bytes(2 * (off + len(src) - len(buf))))
            for i, v in enumerate(src):
                buf[off + i] = v
            placed.append((shot["id"], c["start"], off, src))

    gain = 1.0
    peak = max(abs(v) for v in buf) or 1
    if peak > PEAK_LIMIT:
        gain = PEAK_LIMIT / peak
        for i in range(len(buf)):
            buf[i] = int(buf[i] * gain)
        print(f"峰值 {peak} 超限，整体衰减 {20 * math.log10(gain):.2f} dB")

    stereo = array("h", bytes(4 * len(buf)))
    stereo[0::2] = buf
    stereo[1::2] = buf

    out = RENDERS / "track.wav"
    with wave.open(str(out), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(stereo.tobytes())
    print(f"✓ 音轨：{out}")
    print(f"  时长 {len(buf) / SR:.2f}s（画面 {total:.2f}s，计划 {TIMING['total']:.2f}s），"
          f"{len(placed)} 句，峰值 {min(peak, PEAK_LIMIT)}")
    print(f"  句首底噪共裁掉 {trimmed / SR:.2f}s")
    if overflow:
        print(f"  ⚠ 越界到镜头外的句子 {len(overflow)} 条：{overflow[:5]}")

    if args.check:
        # 回读成品文件，抽样比对写入位置与幅度，验证时间轴落点、增益与立体声交织
        with wave.open(str(out), "rb") as w:
            raw = array("h", w.readframes(w.getnframes()))
            nch = w.getnchannels()
        left, right = raw[0::2], raw[1::2]
        worst = 0
        for _, _, off, src in placed:
            for i in range(0, len(src), 7):
                worst = max(worst, abs(left[off + i] - int(src[i] * gain)))
        print(f"  回读抽样：{len(placed)} 句，最大误差 {worst}（左右声道一致："
              f"{left[:SR] == right[:SR]}）")
        silent = [sid for sid, _, off, src in placed
                  if not any(abs(v) > 300 for v in left[off:off + min(SR, len(src))])]
        print(f"  首秒无可听内容的句子：{len(silent)} 条")
        last = max(off + len(src) for _, _, off, src in placed) / SR
        print(f"  末句结束于 {last:.2f}s，音轨末端 {len(buf) / SR - last:.2f}s 为静音")
        for shot, base in zip(TIMING["shots"], starts):
            # 静音镜没有 cue，末句止就用镜头末帧代替
            tail = base + (shot["cues"][-1]["end"] if shot["cues"] else shot["duration"])
            print(f"    镜 {shot['id']:02d} 起 {base:7.2f}s 计划 {shot['duration']:6.2f}s "
                  f"末句止 {tail:7.2f}s")


if __name__ == "__main__":
    main()
