"""
由 tts/manifest.json 生成全片时间轴 timing.json（镜头时长、每行字幕的起止时刻，均对齐到帧）。

`narration.py` 里标了 `"silent"` 的镜头没有旁白，时长直接取该字段的秒数，cues 为空。

用法：python plan.py
"""
from __future__ import annotations

import json
import math
import os

from narration import SHOTS

HERE = os.path.dirname(os.path.abspath(__file__))
FPS = 30
# 镜头开头留白（秒），首镜稍长让画面先立住
LEAD = {1: 1.2}
LEAD_DEFAULT = 0.5
# 句间停顿：逗号类 / 句号类（语速 1.32 下按 1.0 的听感折算，0.12/0.24 ≈ 原来的 0.16/0.32）
GAP = {"short": 0.12, "long": 0.24}
# 镜头末尾留白（秒），含 0.4 秒淡出；镜 17 只有两句旁白，画面要多停一会儿，末镜给品牌动画收尾
TAIL = {17: 2.6, 20: 3.6}
TAIL_DEFAULT = 0.55


def snap(t: float) -> float:
    """
    把时刻对齐到最近的帧。
    @param t 秒
    @returns 对齐后的秒
    """
    return round(t * FPS) / FPS


def main() -> None:
    with open(os.path.join(HERE, "tts", "manifest.json"), encoding="utf-8") as fp:
        manifest = json.load(fp)
    by_shot: dict[int, list] = {}
    for e in manifest:
        by_shot.setdefault(e["shot"], []).append(e)

    shots = []
    cursor = 0.0
    for shot in SHOTS:
        sid = shot["id"]
        # 静音镜：没有旁白，时长取 narration.py 里写死的秒数
        hold = shot.get("silent")
        if hold:
            duration = math.ceil(hold * FPS) / FPS
            shots.append({"id": sid, "title": shot["title"], "start": round(cursor, 4),
                          "duration": duration, "cues": []})
            cursor += duration
            continue
        lines = sorted(by_shot[sid], key=lambda e: e["line"])
        assert len(lines) == len(shot["lines"]), f"镜 {sid} 行数与 manifest 不一致，请先重跑 synth.py"
        t = LEAD.get(sid, LEAD_DEFAULT)
        cues = []
        for i, e in enumerate(lines):
            start = snap(t)
            end = start + e["duration"]
            cues.append({"start": start, "end": round(end, 4), "display": e["display"], "file": e["file"],
                         "pause": e["pause"]})
            t = end + (GAP[e["pause"]] if i < len(lines) - 1 else 0)
        duration = math.ceil((t + TAIL.get(sid, TAIL_DEFAULT)) * FPS) / FPS
        # 字幕显示窗口：短停顿内衔接到下一句，避免闪烁
        for i, c in enumerate(cues):
            if i + 1 < len(cues):
                nxt = cues[i + 1]["start"]
                c["show_end"] = round(nxt - 1 / FPS if nxt - c["end"] < 0.9 else c["end"] + 0.35, 4)
            else:
                c["show_end"] = round(min(c["end"] + 0.6, duration - 0.45), 4)
        shots.append({"id": sid, "title": shot["title"], "start": round(cursor, 4), "duration": duration,
                      "cues": cues})
        cursor += duration

    out = {"fps": FPS, "total": round(cursor, 4), "shots": shots}
    with open(os.path.join(HERE, "timing.json"), "w", encoding="utf-8") as fp:
        json.dump(out, fp, ensure_ascii=False, indent=1)
    for s in shots:
        print(f"镜 {s['id']:02d} {s['title']:<22} 起 {s['start']:7.2f}s 长 {s['duration']:6.2f}s  {len(s['cues'])} 行")
    print(f"全片 {cursor:.2f}s ≈ {int(cursor // 60)} 分 {cursor % 60:.1f} 秒")


if __name__ == "__main__":
    main()
