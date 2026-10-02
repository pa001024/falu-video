"""
法露茜攻略视频的公共层：配色、字体、时间轴、字幕轨、HUD 与镜头基类。

镜头脚本只需继承 `Shot`、设置 `shot_id`，在 `construct()` 里用 `self.at(cue, ...)` 把动画挂到旁白时刻上。
"""
from __future__ import annotations

import json
import os
import re

import numpy as np
from manimlib import *

HERE = os.path.dirname(os.path.abspath(__file__))
IMGS = "E:/dev/dna-builder/public/imgs"

with open(os.path.join(HERE, "timing.json"), encoding="utf-8") as _fp:
    TIMING = json.load(_fp)

FPS = TIMING["fps"]

# ---- 配色 ----
BG = "#0A0C11"
PANEL = "#121720"
PANEL_EDGE = "#2A3242"
TXT = "#E9ECF2"
TXT2 = "#A3ACBC"
TXT3 = "#5E6778"
FIRE = "#FF5A36"
BLOOD = "#E3263F"
GOLD = "#FFC94D"
CALAM = "#A970FF"
DISORDER = "#FF9A3C"
FULL = "#3FD8FF"
SKILL = "#FF6F4F"
WEAPON = "#4FA8FF"
SHARED = "#7BE0B0"
COLD = "#86A8D8"
CRIMSON = "#C0142F"
TERM = "#FFAE85"

# ---- 字体 ----
FONT = "Noto Sans SC"
SERIF = "Noto Serif SC"
NUM = "Bahnschrift"


def asset(name: str) -> str:
    """
    @param name 文件名
    @returns 本项目 assets 目录下的绝对路径
    """
    return os.path.join(HERE, "assets", name)


def img(rel: str) -> str:
    """
    @param rel 相对 public/imgs 的路径，如 "webp/T_Head_Falu.webp"
    @returns 绝对路径
    """
    return f"{IMGS}/{rel}"


def fix_text_bbox(mob) -> None:
    """
    修正病态字形撑大的包围盒。

    Noto Sans SC 里个别汉字（如「玩」「细」）的字形带有超远控制点，会让整个 Text 的包围盒
    虚高数倍；包围盒一旦失真，居中 / 贴边对齐就会整体偏移。这里按子对象高度的中位数
    剔除异常字形后重算包围盒缓存。

    ⚠️ 只改包围盒，不动字形本身，渲染结果不变。
    """
    subs = getattr(mob, "submobjects", None)
    if not subs or len(subs) < 2:
        return
    boxes = [np.array(s.get_bounding_box(), dtype=float) for s in subs]
    heights = sorted(bb[2][1] - bb[0][1] for bb in boxes)
    med = heights[len(heights) // 2]
    if med <= 0:
        return
    keep = [bb for bb in boxes if bb[2][1] - bb[0][1] <= med * 3.0]
    if len(keep) == len(boxes):
        return
    lo = np.min([bb[0] for bb in keep], axis=0)
    hi = np.max([bb[2] for bb in keep], axis=0)
    mob.bounding_box = np.array([lo, (lo + hi) / 2, hi])
    mob._needs_new_bounding_box = False


# Noto Sans SC 的字形路径在部分字号（如 21、44）会被 Pango/cairo 输出成带超远控制点的病态路径，
# 且字号逐个不同、离散散布，无法逐字号规避；统一用基准字号生成再等比缩放可绕开整类问题。
TEXT_BASE = 48


def tx(text: str, size: float = 30, color: str = TXT, bold: bool = False, font: str = FONT, **kw) -> Text:
    """
    创建单色文本。
    @param text 文本
    @param size 字号
    @param color 颜色
    @param bold 是否粗体
    @param font 字体
    @returns Text
    """
    t = Text(text, font=font, font_size=TEXT_BASE, weight=BOLD if bold else NORMAL, **kw)
    if size != TEXT_BASE:
        t.scale(size / TEXT_BASE)
    t.set_fill(color, 1)
    fix_text_bbox(t)
    return t


def to_markup(text: str, base: str = TXT, strong: str = GOLD, term: str = TERM) -> str:
    """
    把字幕标记转换成 Pango markup：`**强调**` 金色加粗、`[术语]` 暖色。
    @param text 含标记的文本
    @returns markup 字符串
    """
    s = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    s = re.sub(r"\*\*(.+?)\*\*", lambda m: f'<span foreground="{strong}" font_weight="bold">{m.group(1)}</span>', s)
    s = re.sub(r"\[(.+?)\]", lambda m: f'<span foreground="{term}">{m.group(1)}</span>', s)
    return f'<span foreground="{base}">{s}</span>'


def mk(text: str, size: float = 30, base: str = TXT, strong: str = GOLD, term: str = TERM, font: str = FONT,
       **kw) -> MarkupText:
    """
    创建带强调标记的文本。
    @param text 含 `**…**` / `[…]` 标记的文本
    @returns MarkupText
    """
    m = MarkupText(to_markup(text, base, strong, term), font=font, font_size=TEXT_BASE, **kw)
    if size != TEXT_BASE:
        m.scale(size / TEXT_BASE)
    fix_text_bbox(m)
    return m


def num(text: str, size: float = 40, color: str = TXT, bold: bool = True) -> Text:
    """
    数字专用字体（Bahnschrift）的文本。
    @param text 数字串，如 "71.016"
    @returns Text
    """
    return tx(text, size=size, color=color, bold=bold, font=NUM)


def panel(width: float, height: float, color: str = PANEL, edge: str = PANEL_EDGE, opacity: float = 0.92,
          radius: float = 0.16, stroke: float = 1.5) -> RoundedRectangle:
    """
    圆角面板。
    @returns RoundedRectangle
    """
    return RoundedRectangle(width=width, height=height, corner_radius=radius,
                            fill_color=color, fill_opacity=opacity, stroke_color=edge, stroke_width=stroke)


def chip(text: str, color: str = FIRE, size: float = 22, fill_opacity: float = 0.16, pad: float = 0.16,
         text_color: str | None = None, bold: bool = True) -> VGroup:
    """
    胶囊标签：半透明底 + 同色描边 + 文字。
    @returns VGroup(底, 文字)
    """
    t = tx(text, size=size, color=text_color or color, bold=bold)
    box = RoundedRectangle(width=t.get_width() + pad * 2.4, height=t.get_height() + pad * 1.6,
                           corner_radius=(t.get_height() + pad * 1.6) / 2,
                           fill_color=color, fill_opacity=fill_opacity, stroke_color=color, stroke_width=1.5)
    t.move_to(box)
    return VGroup(box, t)


def icon(rel_or_abs: str, height: float = 1.2) -> ImageMobject:
    """
    载入图标（public/imgs 相对路径或绝对路径）。
    @returns ImageMobject
    """
    path = rel_or_abs if os.path.isabs(rel_or_abs) else img(rel_or_abs)
    return ImageMobject(path, height=height)


def glow(name: str = "fire", height: float = 4.0, opacity: float = 0.5) -> ImageMobject:
    """
    径向辉光贴图。
    @param name fire / blood / gold / calam / full / cold / weapon / white
    @returns ImageMobject
    """
    g = ImageMobject(asset(f"glow_{name}.png"), height=height)
    g.set_opacity(opacity)
    return g


def icon_card(rel: str, label: str, color: str = TXT3, size: float = 1.25, label_size: float = 20,
              ring: str | None = None) -> Group:
    """
    图标卡：深色圆角底 + 图标 + 下方名称。
    @returns Group(底, 图标, 名称)
    """
    base = panel(size + 0.22, size + 0.22, radius=0.18, edge=ring or PANEL_EDGE, stroke=2 if ring else 1.5)
    ic = icon(rel, height=size)
    ic.move_to(base)
    name = tx(label, size=label_size, color=color)
    name.next_to(base, DOWN, buff=0.14)
    return Group(base, ic, name)


class HBar(VGroup):
    """
    横向数值条：底槽 + 填充 + 可选刻度文字。由 ValueTracker 驱动填充比例。
    """

    def __init__(self, width: float = 6.0, height: float = 0.32, color: str = BLOOD, value: float = 1.0,
                 track: str = "#1C2230", radius: float | None = None, **kw):
        super().__init__(**kw)
        r = height / 2 if radius is None else radius
        self.full_width = width
        self.bar_height = height
        self.track = RoundedRectangle(width=width, height=height, corner_radius=r,
                                      fill_color=track, fill_opacity=1, stroke_color=PANEL_EDGE, stroke_width=1)
        self.fill = Rectangle(width=width, height=height, fill_color=color, fill_opacity=1, stroke_width=0)
        self.value = ValueTracker(value)
        self.add(self.track, self.fill)
        self.fill.add_updater(self._sync)

    def _sync(self, m: Mobject) -> None:
        """按当前比例把填充贴齐到底槽左端。"""
        v = max(0.002, min(1.0, self.value.get_value()))
        m.set_width(self.full_width * v, stretch=True)
        m.set_height(self.bar_height, stretch=True)
        m.move_to(self.track.get_left(), aligned_edge=LEFT)

    def anim_to(self, v: float, **kw) -> Animation:
        """
        @param v 目标比例 0–1
        @returns 填充比例变化的动画
        """
        return self.value.animate.set_value(v).set_anim_args(**kw) if kw else self.value.animate.set_value(v)


class Subtitles(Group):
    """
    字幕轨：每句预先排好，随场景时钟淡入淡出（不占用 play/wait 调度）。
    """

    def __init__(self, scene: Scene, cues: list[dict], y: float = -3.28, size: float = 34, max_width: float = 12.8):
        super().__init__()
        self.scene = scene
        self.cues = cues
        self.items = []
        for c in cues:
            t = mk(c["display"], size=size)
            if t.get_width() > max_width:
                t.set_width(max_width)
            t.move_to([0, y, 0])
            t.set_backstroke(BG, 5)
            t.set_opacity(0)
            self.items.append(t)
            self.add(t)
        self.alphas = [0.0] * len(cues)
        self.add_updater(lambda m: m._tick())

    def _tick(self) -> None:
        """按当前时刻计算每句字幕的不透明度，只在变化时写回。"""
        t = self.scene.time
        fade = 0.12
        for i, c in enumerate(self.cues):
            a = min(1.0, max(0.0, (t - (c["start"] - 0.06)) / fade)) * min(1.0, max(0.0, (c["show_end"] - t) / fade))
            a = round(a, 3)
            if a != self.alphas[i]:
                self.alphas[i] = a
                self.items[i].set_opacity(a)
                self.items[i].set_stroke(BG, 5, opacity=a, behind=True)


class Shot(Scene):
    """
    镜头基类：背景、HUD（镜号 · 标题 · 全片进度）、字幕轨，以及按旁白时刻调度动画的工具。
    """

    shot_id: int = 0

    def setup(self) -> None:
        self.meta = TIMING["shots"][self.shot_id - 1]
        self.cues = self.meta["cues"]
        self.duration = self.meta["duration"]
        self.global_start = self.meta["start"]
        self.total = TIMING["total"]

        bg = ImageMobject(asset("bg.png"), height=FRAME_HEIGHT)
        bg.set_width(FRAME_WIDTH, stretch=True)
        bg.set_z_index(-100)
        self.add(bg)

        self.hud = self.build_hud()
        self.progress = self.build_progress()
        self.subs = Subtitles(self, self.cues)
        self.subs.set_z_index(50)
        self.add(self.progress, self.subs)

    # ---- HUD ----
    def build_hud(self) -> VGroup:
        """
        左上角镜号 + 标题，右上角栏目名。
        @returns VGroup
        """
        number = num(f"{self.shot_id:02d}", size=34, color=FIRE)
        bar = Line(UP * 0.2, DOWN * 0.2, stroke_color=TXT3, stroke_width=2)
        title = tx(self.meta["title"], size=24, color=TXT2)
        tag = VGroup(number, bar, title).arrange(RIGHT, buff=0.22)
        tag.to_corner(UL, buff=0.42)
        brand = tx("二重螺旋 · 法露茜机制拆解", size=18, color=TXT3)
        brand.to_corner(UR, buff=0.5)
        hud = VGroup(tag, brand)
        hud.set_z_index(40)
        return hud

    def build_progress(self) -> VGroup:
        """
        底部全片进度条，每镜一个刻度。
        @returns VGroup
        """
        y = -FRAME_HEIGHT / 2 + 0.035
        track = Rectangle(width=FRAME_WIDTH, height=0.05, fill_color="#1A1F2A", fill_opacity=1, stroke_width=0)
        track.move_to([0, y, 0])
        ticks = VGroup()
        for s in TIMING["shots"][1:]:
            x = -FRAME_WIDTH / 2 + FRAME_WIDTH * s["start"] / self.total
            ticks.add(Rectangle(width=0.02, height=0.05, fill_color=BG, fill_opacity=1, stroke_width=0).move_to([x, y, 0]))
        fill = Rectangle(width=FRAME_WIDTH, height=0.05, fill_color=FIRE, fill_opacity=0.9, stroke_width=0)

        def sync(m: Mobject) -> None:
            ratio = (self.global_start + self.time) / self.total
            m.set_width(max(0.001, FRAME_WIDTH * min(1.0, ratio)), stretch=True)
            m.move_to([-FRAME_WIDTH / 2, y, 0], aligned_edge=LEFT)

        fill.add_updater(sync)
        group = VGroup(track, fill, ticks)
        group.set_z_index(60)
        return group

    # ---- 时间调度 ----
    def T(self, i: int, offset: float = 0.0) -> float:
        """
        @param i 字幕行号（负数从尾部数），或超出范围时视为秒数偏移
        @returns 该行旁白开始时刻 + 偏移，或直接返回 i + offset
        """
        if -len(self.cues) <= i < len(self.cues):
            return self.cues[i]["start"] + offset
        else:
            # 超出范围，视为绝对时间偏移
            return float(i) + offset

    def E(self, i: int, offset: float = 0.0) -> float:
        """
        @param i 字幕行号
        @returns 该行旁白结束时刻 + 偏移
        """
        return self.cues[i]["end"] + offset

    def until(self, t: float) -> None:
        """
        等到场景时钟到达 t；已超过则立即返回（并记录偏差）。
        @param t 镜内时刻（秒）
        """
        dt = t - self.time
        if dt >= 0.5 / FPS:
            self.wait(dt)
        elif dt < -0.12:
            log.warning(f"镜 {self.shot_id:02d} 调度落后 {-dt:.2f}s（目标 {t:.2f}s）")

    def at(self, t: float, *anims: Animation, run_time: float = 0.8, **kw) -> None:
        """
        在时刻 t 开始播放动画。
        @param t 镜内时刻
        @param anims 动画
        @param run_time 时长
        """
        self.until(t)
        self.play(*anims, run_time=run_time, **kw)

    def intro(self, *extra: Animation, run_time: float = 0.5) -> None:
        """镜头开场：HUD 淡入，可附带首批画面动画。"""
        self.play(FadeIn(self.hud, shift=RIGHT * 0.15), *extra, run_time=run_time)

    def outro(self, *keep: Mobject) -> None:
        """
        镜头收尾：在末尾 0.4 秒淡出除背景 / 进度条 / 字幕外的全部内容，并把时长对齐到时间轴。
        @param keep 不需要淡出的额外对象
        """
        fixed = {id(m) for m in self.mobjects[:1]} | {id(self.progress), id(self.subs)} | {id(k) for k in keep}
        rest = [m for m in self.mobjects if id(m) not in fixed]
        self.until(self.duration - 0.4)
        if rest:
            self.play(*[FadeOut(m) for m in rest], run_time=0.4)
        self.until(self.duration)
        total_frames = round(self.time * FPS)
        expected = round(self.duration * FPS)
        if total_frames != expected:
            log.warning(f"镜 {self.shot_id:02d} 帧数 {total_frames} ≠ 计划 {expected}")
