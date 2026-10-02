"""旁白质检：逐条统计基频中位数（音色漂移）、最长内部静音、峰值与 RMS。"""
import json
import os

import librosa
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(HERE)

with open(os.path.join(HERE, "manifest.json"), encoding="utf-8") as fp:
    entries = json.load(fp)

rows = []
for e in entries:
    y, sr = librosa.load(os.path.join(PROJECT, e["file"]), sr=16000)
    f0, voiced, _ = librosa.pyin(y, fmin=70, fmax=500, sr=sr, frame_length=1024)
    f0 = f0[voiced & ~np.isnan(f0)]
    med = float(np.median(f0)) if f0.size else float("nan")
    frame = 160
    n = y.size // frame
    db = 20 * np.log10(np.sqrt(np.mean(y[: n * frame].reshape(n, frame) ** 2, axis=1)) + 1e-9)
    silent = db < -40
    longest = run = 0
    for s in silent:
        run = run + 1 if s else 0
        longest = max(longest, run)
    rows.append((e["shot"], e["line"], med, longest * frame / sr, float(np.abs(y).max()),
                 float(20 * np.log10(np.sqrt(np.mean(y ** 2)) + 1e-9)), e["duration"]))

meds = np.array([r[2] for r in rows])
print(f"F0 中位数分布：median={np.nanmedian(meds):.1f}Hz  p5={np.nanpercentile(meds, 5):.1f}  p95={np.nanpercentile(meds, 95):.1f}")
print(f"RMS dBFS：min={min(r[5] for r in rows):.1f} max={max(r[5] for r in rows):.1f}")
for r in rows:
    flags = []
    if not (150 <= r[2] <= 300):
        flags.append("F0")
    if r[3] > 0.55:
        flags.append("SIL")
    if r[4] > 0.99:
        flags.append("CLIP")
    if flags:
        print(f"{r[0]:02d}_{r[1]:02d} f0={r[2]:.0f}Hz 最长静音={r[3]:.2f}s 峰值={r[4]:.2f} rms={r[5]:.1f}dB 时长={r[6]:.2f}s {','.join(flags)}")
