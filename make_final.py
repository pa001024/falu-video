"""
把 20 个镜头的画面拼成全片，并合上 build_audio.py 产出的音轨，得到最终成片。

用法：
  python make_final.py                 # → renders/falu_guide_hd.mp4
  python make_final.py --preview       # → renders/falu_guide_preview.mp4
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).parent
RENDERS = HERE / "renders"
TIMING = json.loads((HERE / "timing.json").read_text(encoding="utf-8"))
FFMPEG = Path("E:/soft/GPT-SoVITS-v2/runtime/ffmpeg/bin/ffmpeg.exe")
FFPROBE = Path("E:/soft/GPT-SoVITS-v2/runtime/ffmpeg/bin/ffprobe.exe")
# 画面比计划时长多出多少秒算「动画超时」，需要人工确认
OVERRUN = 0.12


def probe(path: Path, entries: str) -> dict[str, str]:
    """
    读取媒体流信息。
    @param path 文件
    @param entries ffprobe -show_entries 的值
    @returns 键值对
    """
    res = subprocess.run(
        [str(FFPROBE), "-v", "error", "-select_streams", "v:0",
         "-show_entries", entries, "-of", "default=nw=1", str(path)],
        capture_output=True, text=True,
    )
    out = {}
    for line in res.stdout.strip().splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            out[k] = v
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="拼接并合成最终成片")
    parser.add_argument("--preview", action="store_true", help="按 480p 预览命名输出")
    args = parser.parse_args()

    shots = TIMING["shots"]
    missing = [s["id"] for s in shots if not (RENDERS / f"S{s['id']:02d}.mp4").exists()]
    if missing:
        raise FileNotFoundError(f"缺少镜头画面：{missing}")

    print("=== 画面自检 ===")
    warn = []
    res_set = set()
    for s in shots:
        info = probe(RENDERS / f"S{s['id']:02d}.mp4", "stream=width,height,r_frame_rate,duration")
        res_set.add((info.get("width"), info.get("height"), info.get("r_frame_rate")))
        dur = float(info.get("duration", 0))
        drift = dur - s["duration"]
        if drift > OVERRUN:
            warn.append((s["id"], dur, s["duration"]))
        print(f"  镜 {s['id']:02d}  画面 {dur:6.2f}s / 计划 {s['duration']:6.2f}s  差 {drift:+.2f}s")
    if len(res_set) > 1:
        raise ValueError(f"镜头分辨率/帧率不一致：{res_set}")
    print(f"  统一规格：{res_set.pop()}")
    if warn:
        print(f"  ⚠ {len(warn)} 个镜头的动画长于旁白计划：{warn}")

    lst = RENDERS / "concat_list.txt"
    lst.write_text("".join(f"file 'S{s['id']:02d}.mp4'\n" for s in shots), encoding="utf-8")

    track = RENDERS / "track.wav"
    if not track.exists():
        raise FileNotFoundError("缺少音轨，请先运行 build_audio.py")

    final = RENDERS / ("falu_guide_preview.mp4" if args.preview else "falu_guide_hd.mp4")
    print("\n=== 拼接 + 合音 ===")
    subprocess.run([
        str(FFMPEG), "-y", "-v", "error",
        "-f", "concat", "-safe", "0", "-i", str(lst),
        "-i", str(track),
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "32000", "-ac", "2",
        "-shortest", "-movflags", "+faststart",
        str(final),
    ], check=True)
    lst.unlink()

    info = probe(final, "stream=width,height,r_frame_rate,duration")
    total = subprocess.run(
        [str(FFPROBE), "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(final)],
        capture_output=True, text=True,
    ).stdout.strip()
    dur = float(total)
    print(f"✓ 成片：{final}")
    print(f"  {info.get('width')}x{info.get('height')} @ {info.get('r_frame_rate')}  "
          f"{dur:.2f}s ≈ {int(dur // 60)} 分 {dur % 60:.1f} 秒")
    print(f"  大小 {final.stat().st_size / 1024 / 1024:.1f} MB（计划总长 {TIMING['total']:.2f}s）")


if __name__ == "__main__":
    main()
