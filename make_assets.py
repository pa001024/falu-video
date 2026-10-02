"""
生成视频用的位图素材：全屏背景、各色辉光贴图。

用法：python make_assets.py
产出：assets/bg.png、assets/glow_<name>.png
"""
from __future__ import annotations

import os

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets")
W, H = 1920, 1080

GLOWS = {
    "fire": "#FF5A36",
    "blood": "#E3263F",
    "gold": "#FFC94D",
    "calam": "#A970FF",
    "full": "#3FD8FF",
    "cold": "#86A8D8",
    "weapon": "#4FA8FF",
    "white": "#FFFFFF",
}


def hex_rgb(h: str) -> np.ndarray:
    """
    十六进制颜色转 0–1 浮点 RGB。
    @param h 形如 #RRGGBB
    @returns shape (3,) 数组
    """
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], dtype=np.float32) / 255.0


def radial(cx: float, cy: float, r: float) -> np.ndarray:
    """
    以 (cx, cy) 为心、r 为半径的平滑径向权重（中心 1、外缘 0）。
    @returns shape (H, W) 数组
    """
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / r
    t = np.clip(1 - d, 0, 1)
    return t * t * (3 - 2 * t)


def make_bg() -> None:
    """生成深色背景：中心微亮、四角压暗、左上冷光与右下火光、点阵纹理与细颗粒抖动（抑制色带）。"""
    inner, outer = hex_rgb("#161B26"), hex_rgb("#06070A")
    w = radial(W * 0.5, H * 0.44, 1250)[..., None]
    img = outer + (inner - outer) * w
    img += hex_rgb("#4A6A9A") * 0.07 * radial(W * 0.12, H * 0.1, 900)[..., None]
    img += hex_rgb("#FF5A36") * 0.06 * radial(W * 0.92, H * 0.96, 820)[..., None]
    yy, xx = np.mgrid[0:H, 0:W]
    dots = ((xx % 48) < 2) & ((yy % 48) < 2)
    img[dots] += 0.018
    rng = np.random.default_rng(7)
    img += (rng.random((H, W, 1), dtype=np.float32) - 0.5) * (2.2 / 255)
    out = (np.clip(img, 0, 1) * 255 + 0.5).astype(np.uint8)
    Image.fromarray(out, "RGB").save(os.path.join(OUT, "bg.png"))


def make_glow(name: str, color: str, size: int = 512) -> None:
    """
    生成带透明通道的径向辉光贴图。
    @param name 文件名后缀
    @param color 辉光颜色
    @param size 边长像素
    """
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32)
    c = (size - 1) / 2
    d = np.sqrt((xx - c) ** 2 + (yy - c) ** 2) / c
    alpha = np.clip(1 - d, 0, 1) ** 2.2
    rgb = np.broadcast_to(hex_rgb(color), (size, size, 3))
    out = np.dstack([rgb, alpha[..., None]])
    Image.fromarray((out * 255 + 0.5).astype(np.uint8), "RGBA").save(os.path.join(OUT, f"glow_{name}.png"))


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    make_bg()
    for name, color in GLOWS.items():
        make_glow(name, color)
    print("素材已生成：", sorted(os.listdir(OUT)))


if __name__ == "__main__":
    main()
