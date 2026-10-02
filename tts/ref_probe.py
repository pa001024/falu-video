"""估算参考音频的基频中位数，用于判断音色性别（男声约 85–160 Hz，女声约 165–280 Hz）。"""
import glob
import os

import librosa
import numpy as np

REF_DIR = r"E:\soft\GPT-SoVITS-v2\参考音频"

for path in sorted(glob.glob(os.path.join(REF_DIR, "*.wav"))):
    y, sr = librosa.load(path, sr=16000)
    f0, voiced, _ = librosa.pyin(y, fmin=60, fmax=500, sr=sr)
    f0 = f0[voiced & ~np.isnan(f0)]
    med = float(np.median(f0)) if f0.size else float("nan")
    rms = float(np.sqrt(np.mean(y ** 2)))
    print(f"{med:7.1f} Hz  rms={rms:.3f}  dur={len(y) / sr:.2f}s  {os.path.basename(path)}")
