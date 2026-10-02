"""
校验音画同步：逐句比对「实测语音起始」与音轨的计划起始。

镜头起始以已渲染画面的实际时长累加为准（见 build_audio.shot_starts），
这样报告的是真实的音画对齐误差，而不是计划与画面之间的累计漂移。

默认校验 renders/track.wav；也可传入成片 mp4，此时会先从音轨解码再比对。

用法：
  python check_sync.py                      # 校验 renders/track.wav
  python check_sync.py renders/xxx.mp4      # 从成片解码校验
"""
from __future__ import annotations

import subprocess
import sys
import wave
from array import array
from pathlib import Path

from build_audio import TIMING, shot_starts

HERE = Path(__file__).parent
FFMPEG = Path("E:/soft/GPT-SoVITS-v2/runtime/ffmpeg/bin/ffmpeg.exe")
SR = 32000
BIN = 160          # 5ms
# 判定「有声音」的包络阈值
THRESH = 300
# 每句允许的搜索窗口
WINDOW = 0.8


def load_mono(src: Path) -> tuple[array, float]:
    """
    取单声道采样：wav 直接读并按需抽取声道，视频则先解码。
    @param src 音频或视频路径
    @returns (采样数组, 时长秒)
    """
    tmp = src
    if src.suffix.lower() != ".wav":
        tmp = HERE / ".tmp_sync.wav"
        subprocess.run([str(FFMPEG), "-y", "-v", "error", "-i", str(src),
                        "-ar", str(SR), "-ac", "1", str(tmp)], check=True)
    with wave.open(str(tmp), "rb") as w:
        nch = w.getnchannels()
        a = array("h")
        a.frombytes(w.readframes(w.getnframes()))
        total = w.getnframes() / SR
    if nch > 1:
        # 多声道是交错采样，必须抽成单声道，否则包络的时间轴会被拉长 nch 倍
        a = a[0::nch]
    if tmp is not src:
        tmp.unlink()
    return a, total


def main() -> None:
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "renders" / "track.wav"
    a, total = load_mono(src)

    starts, picture = shot_starts()
    print(f"音源 {src.name}  时长 {total:.2f}s  画面合计 {picture:.2f}s  脚本计划 {TIMING['total']:.2f}s")

    env = []
    for i in range(0, len(a) - BIN, BIN):
        seg = a[i:i + BIN]
        env.append((sum(x * x for x in seg) / BIN) ** 0.5)
    step = BIN / SR

    worst = (0.0, None)
    per_shot: dict[int, float] = {}
    missed = 0
    for shot, base in zip(TIMING["shots"], starts):
        for c in shot["cues"]:
            expect = base + c["start"]
            i0 = int(expect / step)
            i1 = min(len(env), i0 + int(WINDOW / step))
            hit = next((i for i in range(i0, i1) if env[i] > THRESH), None)
            if hit is None:
                missed += 1
                print(f"  ⚠ 镜 {shot['id']:02d} 行 {c['file']} 计划 {expect:.3f}s 未检出语音")
                continue
            d = hit * step - expect
            per_shot[shot["id"]] = max(per_shot.get(shot["id"], 0.0), abs(d))
            if abs(d) > abs(worst[0]):
                worst = (d, (shot["id"], c["file"], expect))

    print(f"\n共 {sum(len(s['cues']) for s in TIMING['shots'])} 句，未检出 {missed} 句")
    print(f"最大偏差 {worst[0]:+.3f}s（镜 {worst[1][0]:02d} {worst[1][1]}，计划 {worst[1][2]:.3f}s）")
    print("各镜最大偏差：")
    for sid, d in sorted(per_shot.items()):
        flag = "  ← 偏大" if d > 0.3 else ""
        print(f"  镜 {sid:02d}  {d:.3f}s{flag}")


if __name__ == "__main__":
    main()
