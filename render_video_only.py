"""
渲染全片 20 个镜头并合成为完整视频（无音频版）。

用法：
  python render_video_only.py              # 低画质预览（480p）
  python render_video_only.py --hd         # 高清成片（1080p）
  python render_video_only.py --shots 1-5  # 只渲染指定镜头
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
VENV = HERE / ".venv" / "Scripts"
MANIMGL = VENV / "manimgl.exe"
FFMPEG = Path("E:/soft/GPT-SoVITS-v2/runtime/ffmpeg/bin/ffmpeg.exe")
RENDERS = HERE / "renders"


def render_shot(shot_id: int, quality: str) -> Path:
    """
    渲染单个镜头。
    @param shot_id 镜头号 1–20
    @param quality "hd" 高清 1080p / "low" 低画质 480p（注意：manimgl 的 -h 是帮助标志，高清必须用 --hd）
    @returns 产出的 .mp4 路径
    """
    scene_name = f"S{shot_id:02d}"
    out = RENDERS / f"{scene_name}.mp4"
    if out.exists():
        print(f"  [{shot_id:02d}] 已存在，跳过")
        return out
    
    flag = "--hd" if quality == "hd" else "-l"
    cmd = [str(MANIMGL), "shots.py", scene_name, "-w", flag]
    print(f"  [{shot_id:02d}] 渲染中...", flush=True)
    result = subprocess.run(cmd, cwd=HERE, capture_output=True, text=True)
    
    if result.returncode != 0 or not out.exists():
        print(f"\n镜 {shot_id:02d} 渲染失败：")
        print(result.stderr[-500:] if result.stderr else result.stdout[-500:])
        raise RuntimeError(f"Shot {shot_id:02d} failed")
    
    return out


def concat_videos(videos: list[Path], output: Path) -> None:
    """
    用 ffmpeg concat 协议无损拼接视频。
    @param videos 按顺序的视频路径列表
    @param output 输出路径
    """
    list_file = RENDERS / "concat_list.txt"
    list_file.write_text("\n".join(f"file '{v.name}'" for v in videos), encoding="utf-8")
    
    cmd = [
        str(FFMPEG), "-y", "-f", "concat", "-safe", "0", "-i", str(list_file),
        "-c", "copy", str(output)
    ]
    print(f"\n合成全片 → {output.name}", flush=True)
    subprocess.run(cmd, check=True, capture_output=True)
    list_file.unlink()


def parse_shot_range(spec: str) -> list[int]:
    """解析镜头范围，如 '1-5' → [1,2,3,4,5], '1,4,6' → [1,4,6]"""
    if "-" in spec:
        start, end = spec.split("-")
        return list(range(int(start), int(end) + 1))
    else:
        return [int(s.strip()) for s in spec.split(",")]


def main() -> None:
    parser = argparse.ArgumentParser(description="渲染法露茜攻略视频（无音频）")
    parser.add_argument("--hd", action="store_true", help="高清 1080p（默认 480p 预览）")
    parser.add_argument("--shots", help="仅渲染指定镜头，如 1-5 或 1,4,6")
    args = parser.parse_args()
    
    quality = "hd" if args.hd else "low"
    res = "1080p" if args.hd else "480p"
    
    if args.shots:
        shot_ids = parse_shot_range(args.shots)
    else:
        shot_ids = list(range(1, 21))
    
    print(f"=== 渲染 {len(shot_ids)} 个镜头（{res}，无音频）===", flush=True)
    
    videos = []
    for sid in shot_ids:
        video = render_shot(sid, quality)
        videos.append(video)
        print(f"  [{sid:02d}] ✓ {video.name}")
    
    final = RENDERS / f"falu_guide_{'hd' if args.hd else 'preview'}_silent.mp4"
    concat_videos(videos, final)
    
    size_mb = final.stat().st_size / 1024 / 1024
    print(f"\n✓ 全片完成（无音频）：{final}")
    print(f"  {len(shot_ids)} 个镜头，{size_mb:.1f} MB")


if __name__ == "__main__":
    main()
