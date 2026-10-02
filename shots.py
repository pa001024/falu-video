import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from common import *


# ================ 镜 1：开场 ================
class S01(Shot):
    shot_id = 1

    def construct(self):
        # 两张头像并排放在上部，正文与芯片依次排在下方，避免压在脸上
        head = icon("webp/T_Head_Falu.webp", height=2.3).shift(LEFT * 1.3 + UP * 1.45)
        skin = icon("webp/T_Head_Falu01.webp", height=2.3).shift(RIGHT * 1.3 + UP * 1.45)
        g1 = glow("fire", height=3.2, opacity=0.55).move_to(head)
        g2 = glow("fire", height=3.2, opacity=0.55).move_to(skin)

        self.intro(FadeIn(g1, scale=1.1), FadeIn(g2, scale=1.1), FadeIn(head, scale=0.9), FadeIn(skin, scale=0.9))

        # 出场：名字 + 身份副标
        name = mk("**法露茜**", size=54, strong=FIRE).move_to([0, -0.12, 0])
        sub = tx("另一个用火的女人", size=26, color=TXT2).move_to([0, -0.88, 0])
        self.at(self.T(2), FadeIn(name, shift=UP * 0.15), FadeIn(sub, shift=UP * 0.1))

        # 金句：她的子弹是拿血换的
        hook = mk("**她的子弹，是拿血换的。**", size=46, strong=BLOOD).move_to([0, -1.75, 0])
        self.at(self.T(4), FadeIn(hook, scale=0.9))

        # 两枚核心资源芯片
        c1 = chip("觉醒", BLOOD, size=26).move_to([-1.5, -2.62, 0])
        c2 = chip("羽化", CALAM, size=26).move_to([1.5, -2.62, 0])
        self.at(self.T(5), FadeIn(c1, scale=0.85), FadeIn(c2, scale=0.85))

        self.outro()


# ================ 镜 2：她不是武器输出 ================
class S02(Shot):
    shot_id = 2

    def construct(self):
        self.intro()

        # 顶部结论
        title = mk("话先说死：她不是**武器输出**", size=38, strong=GOLD).move_to([0, 2.78, 0])
        self.at(self.T(0), FadeIn(title, shift=UP * 0.12), run_time=0.5)

        # 上排：无声的嘶吼（专武双刀）与血染织羽（灾厄双枪）图标卡分列左右
        w1 = icon_card("webp/T_Head_Dualblade_Wusheng.webp", "无声的嘶吼", TXT2, 1.5, 22, FIRE)
        w1.move_to([-4.0, 1.9, 0])
        w2 = icon_card("webp/T_Head_Crossbow_Yemei.webp", "血染织羽", TXT2, 1.5, 22, CALAM)
        w2.move_to([4.0, 1.9, 0])

        self.at(self.T(1), FadeIn(w1, shift=RIGHT * 0.25), FadeIn(w2, shift=LEFT * 0.25))

        # 左：手法只是近战普攻
        hand = chip("手法 = 近战普攻", TXT3, size=22).move_to([-4.0, 0.42, 0])
        self.at(self.T(1, 0.6), FadeIn(hand, scale=0.88))

        # 中：真正的出伤路径——战技吃紊乱
        conv = mk("[战技]消耗敌人身上的[紊乱]", size=28, term=DISORDER).move_to([0, 0.42, 0])
        self.at(self.T(3), FadeIn(conv, shift=UP * 0.12))

        # 右：灾厄伤害由远程那把血染织羽打出
        dmg = chip("血染织羽 · [灾厄伤害]", CALAM, size=22).move_to([4.0, 0.42, 0])
        self.at(self.T(4), FadeIn(dmg, scale=0.88))

        # 收口：把灾厄伤害算成战技的账
        merge = mk("把**灾厄伤害**算成战技的账", size=32, strong=GOLD).move_to([0, -0.9, 0])
        self.at(self.T(5), FadeIn(merge, shift=UP * 0.12))

        verdict = mk("她是标准的**技能输出**", size=44, strong=CALAM).move_to([0, -2.1, 0])
        self.at(self.T(6), FadeIn(verdict, scale=0.9))

        self.outro()


# ================ 镜 3：我的元素爆发，她的战技 ================
class S03(Shot):
    shot_id = 3

    def construct(self):
        self.intro()

        # 中轴分隔线：左右并置「我的元素爆发」与「她的战技」
        axis = Line(UP * 3.0, DOWN * 3.0, stroke_color=PANEL_EDGE, stroke_width=2).move_to([0, -0.15, 0])
        self.at(self.T(0), FadeIn(axis), run_time=0.4)

        # 左：仆人 · 元素爆发，清空自己身上的生命之契
        l_head = mk("**我的元素爆发**", size=30, strong=FIRE).move_to([-3.6, 2.35, 0])
        l_row1 = mk("清空**自己身上**的生命之契", size=26, strong=BLOOD).move_to([-3.6, 1.2, 0])
        l_row2 = tx("→ 范围火伤 ＋ 回血", size=26, color=TXT2).move_to([-3.6, 0.25, 0])

        self.at(self.T(1), FadeIn(l_head, shift=RIGHT * 0.15), FadeIn(l_row1, shift=UP * 0.1))
        self.at(self.T(2), FadeIn(l_row2, shift=UP * 0.1))

        # 右：法露茜 · 战技，吃敌人身上的火属性紊乱
        r_head = mk("**她的战技**", size=30, strong=SKILL).move_to([3.6, 2.35, 0])
        r_row1 = mk("吃**敌人身上**的[火属性紊乱] ×3", size=26, term=DISORDER).move_to([3.6, 1.2, 0])
        r_row2 = mk("→ **660%** 生命 范围火伤 ＋ 回血", size=26, strong=GOLD).move_to([3.6, 0.25, 0])

        self.at(self.T(3), FadeIn(r_head, shift=LEFT * 0.15), FadeIn(r_row1, shift=UP * 0.1))
        self.at(self.T(4), FadeIn(r_row2, shift=UP * 0.1))

        # 底：同一个动作，资源归属相反
        hook = mk("同一个动作，**账记在对面**", size=40, strong=GOLD).move_to([0, -2.3, 0])
        self.at(self.T(5), FadeIn(hook, scale=0.9))

        self.outro()


# ================ 镜 4：核心资源——血（资源循环 HUD 演示） ================
# 布局对照游戏实机 UI：左上玩家血条、右上敌人血条（紊乱球挂血条底下），右下羽化层数。
# 紊乱口径：挂在敌人身上的[火属性紊乱]，叠满换出——不是掉血充能（掉血攒的是觉醒 / 羽化）。
# 掉血口径：近战自费顶格 14%/次（镜 05：「每秒最多扣 14% 生命，最低扣至 30%」），
# 5 次顶格正好撞 30% 地板；第 6 层紊乱由火属性 DoT 继续叠出，不再掉血。
# 动画口径：全镜只有一个进度源 prog（ValueTracker），环与计数都是它的函数。
LOOP_HP = (0.86, 0.72, 0.58, 0.44, 0.30)      # 每次掉血 −14% 的血量台阶，止于 30% 地板


class S04(Shot):
    shot_id = 4

    def construct(self):
        self.intro()

        # ---- 左上：法露茜面板（头像 + 当前生命条 + 百分比读数，读数是血量的实时函数） ----
        portrait = panel(1.0, 1.0, radius=0.14).move_to([-6.5, 2.5, 0])
        portrait_ic = icon("webp/T_Skill_Falu02.webp", height=0.72).move_to(portrait)
        hp_bar = HBar(width=3.5, height=0.36, color=BLOOD, value=1.0).move_to([-4.1, 2.35, 0])
        hp_name = tx("法露茜 · 当前生命", size=20, color=TXT2).move_to([-5.85, 2.82, 0], aligned_edge=LEFT)
        vis_hp = ValueTracker(0.0)
        pct_txt = always_redraw(lambda: num(f"{round(hp_bar.value.get_value() * 100)}%", size=28, color=BLOOD)
                                .set_opacity(vis_hp.get_value())
                                .move_to([-2.0, 2.35, 0], aligned_edge=LEFT))
        pct_txt.set_z_index(2)
        self.add(pct_txt)

        # ---- 左中：觉醒值（掉血同步充能，对应旁白「觉醒靠掉血攒」） ----
        wake_ic = icon("webp/T_Skill_Falu03.webp", height=0.5).move_to([-6.45, 1.3, 0])
        wake_name = tx("觉醒", size=20, color=GOLD).move_to([-6.05, 1.3, 0], aligned_edge=LEFT)
        wake_bar = HBar(width=2.1, height=0.2, color=GOLD, value=0.0).move_to([-4.15, 1.32, 0])

        # ---- 右上：敌人血条 + 血条底下的球形紊乱计数（整环由参数函数表达，单一进度源） ----
        # 环上任意点 P(t) = C + R·(cos θ, sin θ)，θ(t) = π/2 + t·p·2π，t∈[0,1]，p∈[0,1] 为进度。
        # 底环（整圆）、进度弧（单条参数曲线）没有第二件东西参与：p 由 prog 驱动，每帧重算一条曲线。
        m_name = tx("敌人", size=22, color=TXT).move_to([2.6, 2.82, 0], aligned_edge=LEFT)
        m_bar = HBar(width=3.5, height=0.36, color=CRIMSON, value=1.0).move_to([4.35, 2.35, 0])
        orb_c = np.array([4.35, 1.15, 0.0])
        RING_R = 0.68
        disc = Circle(radius=0.60, stroke_color=DISORDER, stroke_width=2, stroke_opacity=0.4,
                      fill_color="#241207", fill_opacity=0.92).move_to(orb_c)
        d_label = chip("紊乱 · 挂在敌人身上", DISORDER, 18).move_to([4.35, 0.08, 0])
        d_ic = icon("webp/T_Head_Attr_0004.webp", height=0.4).move_to(orb_c + UP * 0.16)

        prog = ValueTracker(0.0)          # 紊乱进度：p = 层数 / 6
        vis_orb = ValueTracker(0.0)       # 右栏进场淡入

        def ring_curve(p: float, opacity: float) -> ParametricCurve:
            sweep = max(p, 1e-4) * TAU

            def f(t: float) -> np.ndarray:
                ang = PI / 2 + t * sweep
                return orb_c + RING_R * np.array([np.cos(ang), np.sin(ang), 0.0])

            return ParametricCurve(f, t_range=(0, 1, 0.002), use_smoothing=False,
                                   stroke_color=DISORDER,
                                   stroke_width=9 if p > 1e-3 else 0,
                                   stroke_opacity=opacity)

        ring = always_redraw(lambda: ring_curve(prog.get_value(), vis_orb.get_value()))
        count = always_redraw(lambda: num(str(int(prog.get_value() * 6 + 0.5)), size=26, color=DISORDER)
                              .set_opacity(vis_orb.get_value()).move_to(orb_c + DOWN * 0.30))
        ring.set_z_index(2)
        count.set_z_index(3)
        self.add(ring, count)

        # ---- 右下：羽化层数计数器（读数同样是 tracker 的函数，无交叉淡变） ----
        ym_card = panel(2.0, 1.1, radius=0.14).move_to([5.35, -1.1, 0])
        ym_ic = icon("webp/T_Head_Crossbow_Yemei.webp", height=0.6).move_to([4.85, -1.1, 0])
        ym_v = ValueTracker(0.0)
        vis_ym = ValueTracker(0.0)
        ym_num = always_redraw(lambda: num(str(int(ym_v.get_value() + 0.5)), size=44, color=CALAM)
                               .set_opacity(vis_ym.get_value()).move_to([5.85, -1.1, 0]))
        ym_num.set_z_index(2)
        ym_label = tx("羽化层数", size=19, color=TXT3).move_to([5.35, -1.85, 0])
        self.add(ym_num)

        # ---- 底中：E 战技（触发时点亮） ----
        e_chip = chip("E · 强化战技", SKILL, 22).move_to([0.35, -1.5, 0])
        e_glow = glow("fire", height=1.7, opacity=0.5).move_to(e_chip)

        self.at(self.T(0, 0.3), FadeIn(portrait), FadeIn(portrait_ic), FadeIn(hp_bar),
                FadeIn(hp_name), FadeIn(wake_ic), FadeIn(wake_name),
                FadeIn(wake_bar), vis_hp.animate.set_value(1.0), run_time=0.4)
        self.at(self.T(0, 0.8), FadeIn(m_name), FadeIn(m_bar), FadeIn(disc),
                FadeIn(d_ic), FadeIn(d_label), vis_orb.animate.set_value(1.0), run_time=0.45)
        self.at(self.T(0, 1.35), FadeIn(ym_card), FadeIn(ym_ic),
                FadeIn(ym_label), FadeIn(e_chip), vis_ym.animate.set_value(1.0), run_time=0.45)

        # ---- 掉血 → 觉醒/羽化充能：5 次 −14% 顶格掉血撞 30% 地板，紊乱同期叠到 5 层 ----
        dmgs = [num("-14%", size=24, color=BLOOD).move_to([-2.0, 2.72, 0], aligned_edge=LEFT) for _ in range(5)]
        for k in range(5):
            t0 = self.T(1, 0.6 + k * 1.2)
            self.at(t0, prog.animate.set_value((k + 1) / 6),
                    hp_bar.anim_to(LOOP_HP[k]), wake_bar.anim_to((k + 1) / 5),
                    FadeIn(dmgs[k]), run_time=0.75)
            self.at(t0 + 0.85, FadeOut(dmgs[k], shift=UP * 0.35), run_time=0.3)
        # 第 6 层紊乱：血条已撞 30% 地板，火属性 DoT 继续叠出最后一层（环走满、无掉血）
        self.at(self.T(1, 0.6 + 5 * 1.2), prog.animate.set_value(1.0), run_time=0.75)

        # 口径小注：觉醒 / 羽化都吃这份掉血
        wake_note = tx("靠掉血攒", size=18, color=TXT3).move_to([-2.95, 1.3, 0], aligned_edge=LEFT)
        self.at(self.T(4, 0.1), FadeIn(wake_note), run_time=0.4)

        # ---- E 战技（[暗影奔袭]）：命中吃 3 层紊乱 → 回 50% 生命 → 羽化 +1 飞入右下角计数器 ----
        fly = icon("webp/T_Head_Crossbow_Yemei.webp", height=0.5).move_to(e_chip)
        consumed = num("-3", size=26, color=DISORDER).move_to([5.55, 1.15, 0])
        healed = num("+50%", size=30, color=SHARED).move_to([-2.55, 2.78, 0])
        pulse = Circle(radius=0.42, stroke_color=CALAM, stroke_width=3).move_to([5.85, -1.1, 0])

        self.at(self.T(4, 4.15), FadeIn(e_glow), FadeIn(e_chip),
                prog.animate.set_value(0.5), FadeIn(consumed), run_time=0.55)
        self.at(self.T(4, 4.8), FadeOut(e_glow), FadeOut(consumed, shift=UP * 0.3),
                FadeIn(healed), hp_bar.anim_to(0.80), run_time=0.7)
        self.at(self.T(5, 0.55), FadeOut(healed, shift=UP * 0.3), FadeIn(fly), run_time=0.25)
        self.at(self.T(5, 0.9), fly.animate.move_to(ym_ic).set_height(0.42), run_time=0.5)
        self.at(self.T(5, 1.5), FadeOut(fly), ym_v.animate.set_value(1.0),
                FadeIn(pulse), run_time=0.3)
        self.at(self.T(5, 1.9), FadeOut(pulse, scale=1.8), run_time=0.4)

        # ---- 收口：输出 ∝ 掉血速度 ----
        note = mk("输出 ∝ **掉血速度**", size=30, strong=BLOOD).move_to([0, 3.35, 0])
        self.at(self.T(5, 2.5), FadeIn(note, scale=0.94), run_time=0.45)

        self.outro()
# ================ 镜 6：紊乱——她真正的发动机 ================
class S06(Shot):
    shot_id = 6

    def construct(self):
        self.intro()

        # 屏一：紊乱的来源（持续伤害满层转化）与被战技消耗
        icon1 = icon("webp/T_Mod_Ifrit01.webp", height=1.15).move_to([0, 2.3, 0])
        glow1 = glow("fire", height=2.1, opacity=0.45).move_to(icon1)
        t1 = mk("[火属性紊乱] · 挂在**敌人身上**", size=28, term=DISORDER).move_to([0, 1.38, 0])
        t2 = mk("触发额外效果 → 叠[火属性]持续伤害，最多 **6 层**", size=24, term=DISORDER).move_to([0, 0.62, 0])
        t3 = mk("**满 6 层清空** → 换出 **1 层**[紊乱]", size=27, term=DISORDER).move_to([0, -0.08, 0])
        t4 = mk("[暗影奔袭] 命中 → 吃 **3 层**", size=28, term=SKILL).move_to([0, -0.98, 0])
        t5 = mk("= **660%** 生命 范围火伤 ＋ 回 **50%** 血", size=28, strong=GOLD).move_to([0, -1.78, 0])

        self.at(self.T(0), FadeIn(glow1, scale=1.15), FadeIn(icon1, scale=0.9), FadeIn(t1, shift=UP * 0.12))
        self.at(self.T(1), FadeIn(t2, shift=UP * 0.1))
        self.at(self.T(2), FadeIn(t3, shift=UP * 0.1))
        self.at(self.T(3), FadeIn(t4, shift=UP * 0.1))
        self.at(self.T(4), FadeIn(t5, shift=UP * 0.1))

        # 屏二：觉醒值撑起强化战技，一次判两下吃六层
        b1 = mk("觉醒值攒得住 ⇒ **战技几乎每次都是强化版**", size=30, strong=FIRE).move_to([0, 1.1, 0])
        b2 = mk("一次判两下 · 吃掉 **6 层**紊乱", size=28, strong=DISORDER).move_to([0, 0.1, 0])
        b3 = mk("= 触发 **2 次** [浴血]", size=32, strong=GOLD, term=BLOOD).move_to([0, -0.95, 0])

        self.at(self.T(5), FadeOut(icon1), FadeOut(glow1), FadeOut(t1), FadeOut(t2), FadeOut(t3), FadeOut(t4), FadeOut(t5),
                FadeIn(b1, shift=UP * 0.12), run_time=0.6)
        self.at(self.T(7), FadeIn(b2, shift=UP * 0.1))
        self.at(self.T(8), FadeIn(b3, scale=0.9))

        # 屏三：焚炎紊乱常驻满层
        c1 = tx("整套配装都在吃它", size=26, color=TXT2).move_to([0, 1.1, 0])
        c2 = mk("[焚炎紊乱] 每吃一次伤害 **+22%** · 最多 **5 层**", size=28, term=DISORDER, strong=GOLD).move_to([0, 0.1, 0])
        c3 = mk("消耗频率高到 **常驻满层**", size=32, strong=GOLD).move_to([0, -0.95, 0])

        self.at(self.T(9), FadeOut(b1), FadeOut(b2), FadeOut(b3), FadeIn(c1, shift=UP * 0.12), run_time=0.6)
        self.at(self.T(10), FadeIn(c2, shift=UP * 0.1))
        self.at(self.T(11), FadeIn(c3, scale=0.9))

        self.outro()


# ================ 镜 5：执行者与 30% 地板 ================
class S05(Shot):
    shot_id = 5

    def construct(self):
        self.intro()

        # 终结技与处决目标
        q_chip = chip("终结技 · [坠入黑渊]", SKILL, size=24).move_to([0, 2.78, 0])
        mark = mk("标记五名[处决目标]", size=26, term=SKILL).move_to([0, 2.1, 0])
        self.at(self.T(0), FadeIn(q_chip, scale=0.88), FadeIn(mark, shift=UP * 0.1))

        # 执行者状态：持续二十秒
        exec_chip = chip("执行者 · 20 秒", CRIMSON, size=26, pad=0.18).move_to([0, 1.32, 0])
        self.at(self.T(1), FadeIn(exec_chip, scale=0.88))

        # 核心数值：每 1.5 秒 攻击 −100 / 生命 +1000
        rate = Group(
            num("1.5", size=48, color=GOLD),
            tx("秒", size=24, color=TXT3),
            tx("：攻击 −100", size=28, color=TXT2),
            tx("·", size=24, color=TXT3),
            mk("生命 **+1000**", size=28, strong=BLOOD),
        ).arrange(RIGHT, buff=0.2).move_to([0, 0.5, 0])
        self.at(self.T(2), FadeIn(rate, lag_ratio=0.08))

        # 双刀每击自费生命并追加生命伤害
        cost = mk("双刀每击 **自费 5% 生命** → 追加生命伤害", size=28, strong=BLOOD).move_to([0, -0.4, 0])
        self.at(self.T(3), FadeIn(cost, shift=UP * 0.1))

        extra = tx("而且必定触发额外效果", size=24, color=TXT2).move_to([0, -0.98, 0])
        self.at(self.T(4), FadeIn(extra, shift=UP * 0.1))

        # 扣血节奏与速率封顶：画面只给数值卡，完整口径交给字幕
        pace = tx("这口血五秒内逐步扣", size=26, color=TXT2).move_to([0, -1.65, 0])
        self.at(self.T(5), FadeIn(pace, shift=UP * 0.1))

        rate_num = Group(
            num("14", size=52, color=BLOOD),
            tx("%/秒", size=26, color=BLOOD),
        ).arrange(RIGHT, buff=0.1)
        cap = Group(rate_num, tx("掉血速率封顶", size=22, color=TXT3)).arrange(RIGHT, buff=0.45)
        cap.move_to([0, -2.45, 0])
        self.at(self.T(6), FadeIn(cap, scale=0.9))

        self.outro()


# ================ 镜 7：充盈——触发率是可以溢出的 ================
def mod_row(rel: str, label: str, value: str, y: float) -> Group:
    """
    一行角色槽魔之楔卡片：图标 + 名称 + 充盈威力加成。
    @param rel 图标相对路径
    @param label 魔之楔名称
    @param value 加成数值文本
    @param y 行中心纵坐标
    @returns 三元素组成的 Group
    """
    ic = icon(rel, height=0.62).move_to([-2.6, y, 0])
    nm = tx(label, size=22, color=TXT2).move_to([-1.5, y, 0], aligned_edge=LEFT)
    vv = num(value, size=30, color=FULL).move_to([2.6, y, 0], aligned_edge=RIGHT)
    return Group(ic, nm, vv)


# 带 [充盈] 标签的伤害清单（S07 收口）。
# 字段出处：char.data.ts「坠入黑渊」（充盈伤害 / 附加伤害）、weapon.data.ts 血染织羽「羽化」（两个字段）。
# 倍率取推荐 BD 口径：角色技能 12 级 ⇒ 充盈伤害 0.49、附加伤害 0.15；羽化字段是固定值 5 / 0.8。
# 定位标签照用户口径：坠入黑渊的充盈伤害落在大招上，附加伤害是 [执行者] 双刀每段附伤。
FULL_TAGGED = (
    ("webp/T_Skill_Falu02.webp", "坠入黑渊", "强化开大", "充盈伤害", "49% 生命", FIRE),
    ("webp/T_Skill_Falu02.webp", "坠入黑渊", "强化普攻", "附加伤害", "15% 生命", FIRE),
    ("webp/T_Head_Crossbow_Yemei.webp", "羽化", "血染织羽", "[羽化]伤害", "500% 灾厄", CALAM),
    ("webp/T_Head_Crossbow_Yemei.webp", "羽化", "血染织羽", "[羽化]额外伤害", "80% 生命", CALAM),
)

FULL_ROW_X = (-6.45, -6.10, -4.85, -3.55, 6.60)


def full_dmg_row(rel: str, skill: str, tag: str, field: str, value: str, color: str, y: float) -> Group:
    """
    一行「带充盈标签的伤害」：技能图标 + 技能名 + 定位标签 + 字段名 + 倍率。
    @param rel 技能图标相对路径
    @param skill 技能名
    @param tag 定位标签（强化开大 / 强化普攻 / 武器名）
    @param field 字段名
    @param value "倍率 单位" 形式的文本，数字与单位分两段排版
    @param color 该行的强调色
    @param y 行中心纵坐标
    @returns 五元素组成的 Group
    """
    ix, nx, tx_x, fx, vx = FULL_ROW_X
    ic = icon(rel, height=0.42).move_to([ix, y, 0])
    nm = tx(skill, size=21, color=color, bold=True).move_to([nx, y, 0], aligned_edge=LEFT)
    tg = tx(tag, size=17, color=TXT3).move_to([tx_x, y, 0], aligned_edge=LEFT)
    fd = tx(field, size=19, color=TXT2).move_to([fx, y, 0], aligned_edge=LEFT)
    amount, unit = value.split(" ", 1)
    vv = VGroup(num(amount, size=23, color=color), tx(unit, size=17, color=TXT3)).arrange(RIGHT, buff=0.1)
    vv.move_to([vx, y, 0], aligned_edge=RIGHT)
    return Group(ic, nm, tg, fd, vv)


class S07(Shot):
    shot_id = 7

    def construct(self):
        self.intro()

        # 顶部：充盈威力与它的唯一入口
        name = mk("**充盈威力**", size=32, strong=FULL).move_to([-4.1, 2.35, 0])
        where = tx("唯一入口：武器触发率", size=21, color=TXT3).move_to([-4.1, 1.82, 0])

        self.at(self.T(0), FadeIn(name, scale=0.9), FadeIn(where))

        # 触发率允许溢出，以 204% 为满格画两条示意条
        head = mk("**允许溢出 100%**", size=28, strong=GOLD).move_to([2.1, 2.35, 0])
        self.at(self.T(1), FadeIn(head, shift=UP * 0.12))

        SPAN = 5.4
        BAR_X = -2.0
        ARMS = (("无声的嘶吼", 204), ("血染织羽", 180))
        labels, values, bars = [], [], []
        for i, (label, value) in enumerate(ARMS):
            y = 1.45 - i * 0.72
            labels.append(tx(label, size=22, color=TXT2).move_to([BAR_X - SPAN / 2 - 0.22, y, 0], aligned_edge=RIGHT))
            bar = HBar(width=SPAN, height=0.26, color=FULL, value=0.002).move_to([BAR_X, y, 0])
            values.append(num(f"{value}%", size=26, color=FULL).move_to([BAR_X + SPAN / 2 + 0.3, y, 0], aligned_edge=LEFT))
            bars.append(bar)

        tick_x = BAR_X - SPAN / 2 + SPAN * 100 / 204
        tick = DashedLine([tick_x, 1.82, 0], [tick_x, 0.40, 0],
                          stroke_color=GOLD, stroke_width=2, dash_length=0.07)
        tick_label = tx("100%", size=19, color=GOLD).next_to(tick, UP, buff=0.06)

        self.at(self.T(2), *[FadeIn(m) for m in labels + bars + values], run_time=0.4)
        self.at(self.T(2, 0.4), bars[0].anim_to(204 / 204), bars[1].anim_to(180 / 204), run_time=0.8)
        self.at(self.T(2, 1.2), FadeIn(tick), FadeIn(tick_label), run_time=0.3)

        # 屏二：溢出的那一截 × 充盈转化 = 武器侧贡献
        t3 = mk("溢出那一截 × [充盈转化]", size=26, term=FULL).move_to([0, -0.35, 0])
        t4 = mk("基础 **1** ＋ 一枚[缠缚·满溢] **+2** = **3**", size=26, term=FULL).move_to([0, -1.0, 0])
        t5 = mk("武器侧一共 **5.52**", size=28, strong=GOLD).move_to([0, -1.7, 0])

        self.at(self.T(3), FadeIn(t3, shift=UP * 0.1))
        self.at(self.T(4), FadeIn(t4, shift=UP * 0.1))
        self.at(self.T(5), FadeIn(t5, shift=UP * 0.1))

        # 屏三：角色槽两枚金魔之楔（各 +550%）分左右飞入，再离场让位给合计
        gate = mk("角色槽 · 两枚金魔之楔", size=27, strong=GOLD).move_to([0, -0.35, 0])
        r1 = mod_row("webp/T_Mod_Sphinx01.webp", "充盈·巧力", "+550%", -1.08)
        r2 = mod_row("webp/T_Mod_Ifrit01.webp", "焚炎紊乱", "+550%", -1.80)
        total = mk("合计 **11.0** ⇒ 面板 **16.52**", size=30, strong=GOLD).move_to([0, -2.56, 0])

        self.at(self.T(6), FadeOut(t3), FadeOut(t4), FadeOut(t5), FadeIn(gate, shift=UP * 0.1), run_time=0.5)
        self.at(self.T(7), FadeIn(r1, shift=RIGHT * 2.6), FadeIn(r2, shift=LEFT * 2.6), run_time=0.7)
        self.at(self.T(8), FadeOut(r1, shift=LEFT * 2.2), FadeOut(r2, shift=RIGHT * 2.2),
                FadeIn(total, scale=0.88), run_time=0.8)

        # 收口：先把「哪些伤害带 [充盈] 标签」摆出来，再落这道乘区
        cap = chip("带[充盈]标签的伤害", FULL, size=20, fill_opacity=0.14, pad=0.14).move_to([0, 0.00, 0])
        rows = [full_dmg_row(*spec, y=-0.60 - i * 0.54) for i, spec in enumerate(FULL_TAGGED)]

        self.at(self.T(9), FadeOut(gate), FadeOut(total), run_time=0.38)
        self.at(self.T(9, 0.40), FadeIn(cap, shift=UP * 0.1), run_time=0.32)
        for i, row in enumerate(rows):
            self.at(self.T(9, 0.78 + i * 0.38), FadeIn(row, shift=RIGHT * 0.3), run_time=0.36)

        # 清单外框与乘区一起落定：这四行伤害整体被 ×17.52 包住。
        # 小标签与乘区都在同一位置，必须先撤标签再落乘区，否则半秒内会叠成双影
        frame = RoundedRectangle(width=13.70, height=2.16, corner_radius=0.10,
                                 stroke_color=GOLD, stroke_width=2, fill_opacity=0).move_to([-0.05, -1.41, 0])
        hook = mk("整体 **×17.52**", size=40, strong=GOLD).move_to([0, 0.10, 0])
        self.at(self.T(9, 2.85), FadeOut(cap), run_time=0.22)
        self.at(self.T(9, 3.10), FadeIn(hook, scale=1.2), FadeIn(frame, scale=1.03), run_time=0.48)

        self.outro()


# ================ 镜 8：流水线 ================
class S08(Shot):
    shot_id = 8

    def construct(self):
        self.intro()

        # 流水线标题
        title = mk("伤害流水线", size=40, strong=GOLD).shift(UP * 2.6)
        self.at(self.T(0), FadeIn(title, shift=UP * 0.15), run_time=0.5)

        # 四个阶段：原料 → 灾厄值 → 羽化 → 充盈
        step1 = Group(icon("webp/T_Mod_Ifrit01.webp", height=1.15),
                      mk("[紊乱] · 血", size=22, term=DISORDER)).arrange(DOWN, buff=0.2)
        step2 = Group(mk("**灾厄值**", size=24, strong=CALAM),
                      tx("紊乱 4/层 · 血 10/1%", size=18, color=TXT3)).arrange(DOWN, buff=0.2)
        step3 = Group(chip("羽化", CALAM, size=22, pad=0.14),
                      tx("满 100", size=22, color=TXT3)).arrange(DOWN, buff=0.2)
        step4 = Group(icon("webp/T_Mod_Sphinx01.webp", height=1.15),
                      mk("[充盈]", size=22, term=FULL)).arrange(DOWN, buff=0.2)

        arrows = [tx("→", size=40, color=TXT3) for _ in range(3)]
        Group(step1, arrows[0], step2, arrows[1], step3, arrows[2], step4).arrange(RIGHT, buff=0.32).shift(UP * 1.15)

        self.at(self.T(1), FadeIn(step1, scale=0.9))
        self.at(self.T(2), FadeIn(arrows[0]), FadeIn(step2, scale=0.9))
        self.at(self.T(3), FadeIn(arrows[1]), FadeIn(step3, scale=0.9))
        self.at(self.T(4), FadeIn(arrows[2]), FadeIn(step4, scale=0.9))

        # 谁是大头：一条命掉完 vs 三层紊乱
        q = mk("**谁是大头？**", size=34, strong=GOLD).move_to([0, -0.4, 0])
        self.at(self.T(5), FadeIn(q, scale=0.9))

        SPAN = 3.6
        rows = (
            ("一条命掉完", 1.0, "**10 层**", CALAM),
            ("三层紊乱", 0.012, "**0.12 层**", DISORDER),
        )
        comp = Group()
        for i, (label, ratio, value, color) in enumerate(rows):
            y = -1.3 - i * 0.62
            lb = tx(label, size=22, color=TXT2).move_to([-4.3, y, 0], aligned_edge=RIGHT)
            bar = HBar(width=SPAN, height=0.26, color=color, value=ratio).move_to([-1.9, y, 0])
            val = mk(value, size=26, strong=color).move_to([0.25, y, 0], aligned_edge=LEFT)
            comp.add(lb, bar, val)

        self.at(self.T(6), FadeIn(comp[0]), FadeIn(comp[1]), FadeIn(comp[2]), run_time=0.5)
        self.at(self.T(7), FadeIn(comp[3]), FadeIn(comp[4]), FadeIn(comp[5]), run_time=0.5)

        # 金句
        hook = mk("紊乱和血是原料 · **充盈威力是换算率**", size=30, strong=GOLD).move_to([0, -2.6, 0])
        self.at(self.T(8), FadeOut(q), FadeIn(hook, scale=0.9), run_time=0.6)

        self.outro()


# ================ 镜 9：掉血的两条上限 · 羽化的两条路径 ================
class S09(Shot):
    shot_id = 9

    def construct(self):
        self.intro()

        # —— 数字计数器统一口径：ValueTracker 驱动 + always_redraw 每帧重建，从 0 涨到目标值 ——
        def counter(tr: ValueTracker, vis: ValueTracker, size: float, color: str,
                    pos, edge: str = LEFT, fmt: str = "{:.0f}", z: int = 4):
            """实时数字：数值由 tr 决定、淡入由 vis 决定，位置按 edge 对齐到固定点 pos。"""
            def build():
                m = num(fmt.format(tr.get_value()), size=size, color=color)
                m.move_to(pos, aligned_edge=edge)
                m.set_z_index(z)
                m.set_opacity(vis.get_value())
                return m
            return always_redraw(build)

        cap_title = mk("掉血上限", size=36, strong=BLOOD).move_to([0, 2.75, 0])
        self.at(self.T(0), FadeIn(cap_title, shift=UP * 0.12), run_time=0.5)

        # 上半：两条掉血上限（条从 0 充到封顶，数字同步从 0 涨）
        SPAN = 5.4
        BAR_X = -1.0
        UNIT_X = 2.15                              # “%/秒”单位左缘固定，计数器右缘贴其左侧
        CAPS = (("近战 · 每击自费 5%", 14, FIRE), ("远程 · [衰朽] 每次 10%", 10, COLD))
        caps = []                                  # (lb, bar, unit, value, color)
        cap_v, cap_vis = [], []
        for label, value, color in CAPS:
            y = 1.95 - len(caps) * 0.68
            lb = mk(label, size=23, term=COLD).move_to([BAR_X - SPAN / 2 - 0.25, y, 0], aligned_edge=RIGHT)
            bar = HBar(width=SPAN, height=0.3, color=color, value=0.0).move_to([BAR_X, y, 0])
            unit = tx("% / 秒", size=19, color=TXT3).move_to([UNIT_X, y, 0], aligned_edge=LEFT)
            caps.append((lb, bar, unit, value, color))
            v, vis = ValueTracker(0.0), ValueTracker(0.0)
            cap_v.append(v)
            cap_vis.append(vis)
            self.add(counter(v, vis, 34, color, unit.get_left() + LEFT * 0.12, edge=RIGHT))

        for i in range(2):
            lb, bar, unit, value, _color = caps[i]
            self.at(self.T(1 + i), FadeIn(lb), FadeIn(bar), FadeIn(unit),
                    cap_vis[i].animate.set_value(1),
                    bar.anim_to(value / 24), cap_v[i].animate.set_value(value), run_time=1.5)

        # 打满：24%/s（数字从 0 涨）
        tot_head = tx("打满就是", size=26, color=TXT2).move_to([-1.85, 0.6, 0], aligned_edge=RIGHT)
        tot_unit = tx("% / 秒", size=22, color=TXT3).move_to([-0.35, 0.44, 0], aligned_edge=LEFT)
        tot_v, tot_vis = ValueTracker(0.0), ValueTracker(0.0)
        self.add(counter(tot_v, tot_vis, 56, BLOOD, [-1.65, 0.6, 0], edge=LEFT))
        self.at(self.T(3), FadeIn(tot_head), FadeIn(tot_unit), tot_vis.animate.set_value(1),
                tot_v.animate.set_value(24), run_time=1.4)

        # 下半：羽化的两条消耗路径（直接射击 / 熔炼5特效）
        divider = Line(LEFT * 6.4, RIGHT * 6.4, stroke_color=PANEL_EDGE, stroke_width=2).move_to([0, -0.15, 0])
        plume_title = mk("[羽化] · 消耗的两条路径", size=30, strong=CALAM).move_to([0, -0.62, 0])

        CARD_Y, CARD_H, CARD_W = -1.68, 1.80, 5.95
        LX, RX = -3.42, 3.42
        card_l = panel(CARD_W, CARD_H, radius=0.12).move_to([LX, CARD_Y, 0])
        card_r = panel(CARD_W, CARD_H, radius=0.12).move_to([RX, CARD_Y, 0])
        chip_l = chip("直接射击", CALAM, size=22).move_to([LX - CARD_W / 2 + 0.26, -1.16, 0], aligned_edge=LEFT)
        note_l = tx("逐颗实时", size=18, color=TXT3).move_to([chip_l.get_right()[0] + 0.24, -1.16, 0], aligned_edge=LEFT)
        chip_r = chip("熔炼5特效", GOLD, size=22).move_to([RX - CARD_W / 2 + 0.26, -1.16, 0], aligned_edge=LEFT)
        note_r = tx("不打枪时", size=18, color=TXT3).move_to([chip_r.get_right()[0] + 0.24, -1.16, 0], aligned_edge=LEFT)
        self.at(self.T(4), FadeIn(divider), FadeIn(plume_title, shift=UP * 0.1), run_time=0.5)
        self.at(self.T(4, 0.55), FadeIn(card_l), FadeIn(card_r), FadeIn(chip_l), FadeIn(note_l),
                FadeIn(chip_r), FadeIn(note_r), run_time=0.55)

        IL = LX - CARD_W / 2 + 0.30                # 左卡内容左缘
        IR = RX - CARD_W / 2 + 0.30                # 右卡内容左缘

        # 路径一（cue5–7）：子弹命中就结算，每颗消耗 1 层
        la1 = tx("子弹命中 → 消耗", size=20, color=TXT2).move_to([IL, -1.64, 0], aligned_edge=LEFT)
        la1u = tx("层 [羽化]", size=20, color=TXT2).move_to([IL + 2.65, -1.64, 0], aligned_edge=LEFT)
        a1_v, a1_vis = ValueTracker(0.0), ValueTracker(0.0)
        self.add(counter(a1_v, a1_vis, 28, CALAM, la1u.get_left() + LEFT * 0.12, edge=RIGHT))
        self.at(self.T(5), FadeIn(la1), FadeIn(la1u), a1_vis.animate.set_value(1),
                a1_v.animate.set_value(1), run_time=0.9)

        la2 = tx("每颗命中，各算一次远程伤害", size=20, color=TXT2).move_to([IL, -2.04, 0], aligned_edge=LEFT)
        self.at(self.T(6), FadeIn(la2, shift=RIGHT * 0.1), run_time=0.5)

        la3 = mk("子弹越多叠得越多 · **多重直接吃进来**", size=20, strong=GOLD).move_to([IL, -2.42, 0], aligned_edge=LEFT)
        self.at(self.T(7), FadeIn(la3, shift=RIGHT * 0.1), run_time=0.5)

        # 路径二（cue8–9）：熔炼5特效 —— 消耗紊乱齐射
        rb1 = tx("消耗", size=20, color=TXT2).move_to([IR, -1.64, 0], aligned_edge=LEFT)
        rb1m = tx("层紊乱 → 齐射", size=20, color=TXT2).move_to([IR + 0.92, -1.64, 0], aligned_edge=LEFT)
        rb1e = tx("发", size=20, color=TXT2).move_to([IR + 3.42, -1.64, 0], aligned_edge=LEFT)
        b3_v, b3_vis = ValueTracker(0.0), ValueTracker(0.0)
        b9_v, b9_vis = ValueTracker(0.0), ValueTracker(0.0)
        self.add(counter(b3_v, b3_vis, 28, GOLD, [IR + 0.58, -1.64, 0], edge=LEFT))
        self.add(counter(b9_v, b9_vis, 28, GOLD, [IR + 3.06, -1.64, 0], edge=LEFT))
        self.at(self.T(8), FadeIn(rb1), FadeIn(rb1m), FadeIn(rb1e), b3_vis.animate.set_value(1),
                b9_vis.animate.set_value(1), b3_v.animate.set_value(3), b9_v.animate.set_value(9), run_time=1.3)

        rb2a = tx("周期：最短", size=20, color=TXT2).move_to([IR, -2.04, 0], aligned_edge=LEFT)
        rb2m = tx("秒 / 层 · 铺满", size=20, color=TXT2).move_to([IR + 1.98, -2.04, 0], aligned_edge=LEFT)
        rb2e = tx("秒", size=20, color=TXT2).move_to([IR + 4.42, -2.04, 0], aligned_edge=LEFT)
        b09_v, b27_v = ValueTracker(0.0), ValueTracker(0.0)
        row2_vis = ValueTracker(0.0)
        self.add(counter(b09_v, row2_vis, 24, GOLD, [IR + 1.42, -2.04, 0], edge=LEFT, fmt="{:.1f}"))
        self.add(counter(b27_v, row2_vis, 24, GOLD, [IR + 3.86, -2.04, 0], edge=LEFT, fmt="{:.1f}"))
        self.at(self.T(9), FadeIn(rb2a), FadeIn(rb2m), FadeIn(rb2e), row2_vis.animate.set_value(1),
                b09_v.animate.set_value(0.9), b27_v.animate.set_value(2.7), run_time=1.2)

        rb3 = tx("吃到", size=20, color=TXT2).move_to([IR, -2.42, 0], aligned_edge=LEFT)
        rb3m = mk("次 **[衰朽]**", size=20, strong=COLD).move_to([IR + 0.92, -2.42, 0], aligned_edge=LEFT)
        b2v, b2v_vis = ValueTracker(0.0), ValueTracker(0.0)
        self.add(counter(b2v, b2v_vis, 24, COLD, [IR + 0.58, -2.42, 0], edge=LEFT))
        self.at(self.T(9, 1.55), FadeIn(rb3), FadeIn(rb3m), b2v_vis.animate.set_value(1),
                b2v.animate.set_value(2), run_time=0.7)

        # 收口（cue10）：直接射击就是每循环的那一枪
        hl = RoundedRectangle(width=CARD_W + 0.16, height=CARD_H + 0.14, corner_radius=0.12,
                              stroke_color=GOLD, stroke_width=2.5, fill_opacity=0).move_to(card_l)
        self.at(self.T(10), FadeIn(hl, scale=1.04), run_time=0.6)

        self.outro()

# ================ 镜 11：两种玩法 ================
class S11(Shot):
    shot_id = 11

    def construct(self):
        self.intro()

        # 标题
        title = mk("换的是**后台**，不是武器", size=38, strong=GOLD).move_to([0, 2.75, 0])
        self.at(self.T(0), FadeIn(title, shift=UP * 0.12), run_time=0.5)

        # 先破误会：两套用的武器完全一样
        same = Group(
            tx("武器完全一样", size=24, color=TXT2),
            icon("webp/T_Head_Dualblade_Wusheng.webp", height=0.62),
            icon("webp/T_Head_Crossbow_Yemei.webp", height=0.62),
        ).arrange(RIGHT, buff=0.32).move_to([0, 2.0, 0])
        self.at(self.T(1), FadeIn(same, shift=UP * 0.1))

        # 换的是辅助：技能流 / 武器流
        team_s = Group(
            chip("技能流", SKILL, size=22),
            icon("webp/T_Head_Baiheng.webp", height=0.68),
            icon("webp/T_Head_Kami.webp", height=0.68),
        ).arrange(RIGHT, buff=0.24).move_to([-3.6, 1.15, 0])
        team_w = Group(
            chip("武器流", WEAPON, size=22),
            icon("webp/T_Head_Feina.webp", height=0.68),
            icon("webp/T_Head_Songlu.webp", height=0.68),
        ).arrange(RIGHT, buff=0.24).move_to([3.6, 1.15, 0])

        self.at(self.T(3), FadeIn(team_s, lag_ratio=0.08))
        self.at(self.T(4), FadeIn(team_w, lag_ratio=0.08))

        # 技能流喂的是四项技能向加成
        four = Group(
            Group(chip("技能伤害", SKILL, size=20, pad=0.14),
                  chip("技能威力", SKILL, size=20, pad=0.14)).arrange(RIGHT, buff=0.24),
            Group(chip("技能速度", SKILL, size=20, pad=0.14),
                  chip("技能无视防御", SKILL, size=20, pad=0.14)).arrange(RIGHT, buff=0.24),
        ).arrange(DOWN, buff=0.24).move_to([-4.0, -0.25, 0])

        self.at(self.T(6), FadeIn(four[0], shift=RIGHT * 0.12), run_time=0.4)
        self.at(self.T(7), FadeIn(four[1], shift=RIGHT * 0.12), run_time=0.4)

        # 武器流这边要分清：只有武器伤害是专属，其余是通用乘区
        only_weapon = mk("**[武器伤害]** 是武器专属", size=25, strong=WEAPON).move_to([0.7, 0.35, 0], aligned_edge=LEFT)
        shared = mk("**增伤 · 属性穿透 · 背水** 是通用乘区", size=25, strong=SHARED).move_to([0.7, -0.45, 0], aligned_edge=LEFT)
        note = tx("技能伤害同样全额吃，不是武器专属", size=22, color=TXT2).move_to([0.7, -1.2, 0], aligned_edge=LEFT)

        self.at(self.T(9), FadeIn(only_weapon, shift=RIGHT * 0.12))
        self.at(self.T(10), FadeIn(shared, shift=RIGHT * 0.12))
        self.at(self.T(11), FadeIn(note, shift=RIGHT * 0.12))

        self.outro()


# ================ 镜 12：配装——基础模板 + 两套流派差异 ================
# 品质 → 魔之楔卡片描边色
QUALITY_EDGE = {"金": GOLD, "紫": "#B07CFF", "蓝": "#5B9BFF"}
# 配装板布局：对齐态 / 聚拢态等距，合并态同系列聚拢（组内 GROUP_GAP、跨系列让出 EXTRA_GAP）
MOD_ICON_H = 0.56
MOD_NAME_SIZE = 14
# 单行名称的宽度权重上限：8 格共用 1.42 的格距，超出的名称（如「羽翼·鼓舞·昂扬」）折成两行
NAME_MAX_WEIGHT = 5.3
RAW_PITCH = 1.42
GROUP_PITCH = 1.36
GROUP_GAP = 1.34
EXTRA_GAP = 0.44
# 三排魔之楔的行中心纵坐标：上排给折行名称多让 0.06，下排名称与字幕带之间留 0.34
MOD_ROW_Y = (1.06, -0.32, -1.70)
# 武器流原始配装（线上 BD 槽位顺序，每槽 8 格）：槽位 → [(系列, 贴图名, 名称, 品质), ...]
# 槽位内顺序无机制含义（同系列可任意互换），画面按「对齐 → 同系列聚拢 → 同名合并」三拍推进
LOADOUT_RAW = (
    ("角色槽", (
        ("百首", "Typhon01_Red", "全盛·追袭", "金"),
        ("焰灵", "Ifrit01", "焚炎紊乱", "金"),
        ("契约者", "Mephisto01_Red", "决断", "金"),
        ("契约者", "Mephisto01_Red", "涅槃·决断", "金"),
        ("人面狮", "Sphinx01", "充盈·巧力", "金"),
        ("海妖", "Siren01_Red", "羽翼·鼓舞·昂扬", "金"),
        ("契约者", "Mephisto01_Red", "涅槃·决断", "金"),
        ("契约者", "Mephisto01_Red", "涅槃·决断", "金"),
    )),
    ("近战槽", (
        ("冥犬", "Cerberus01", "盛怒·缠缚", "金"),
        ("冥犬", "Cerberus01", "透析·缠缚", "金"),
        ("囚狼", "Fenrir01", "时运", "蓝"),
        ("冥犬", "Cerberus01", "缠缚", "紫"),
        ("冥犬", "Cerberus01", "专注·迅捷", "金"),
        ("冥犬", "Cerberus01", "迅捷", "金"),
        ("囚狼", "Fenrir01", "缠缚·满溢", "金"),
        ("囚狼", "Fenrir01", "连环·缠缚", "金"),
    )),
    ("远程槽", (
        ("夜魔", "Lilith01", "专注·威压", "金"),
        ("夜魔", "Lilith01", "盛怒·聚焦", "金"),
        ("夜魔", "Lilith01", "盛怒", "紫"),
        ("夜魔", "Lilith01", "专注", "紫"),
        ("夜魔", "Lilith01", "攻势·专注", "金"),
        ("夜魔", "Lilith01", "盛怒·缠缚", "金"),
        ("邪龙", "Fafnir01", "衰朽", "紫"),
        ("邪龙", "Fafnir01", "缠缚·满溢", "金"),
    )),
)


def weapon_pill(rel: str, edge: str) -> Group:
    """
    武器卡：只含底板与图标，名称由调用方另行创建。
    分开持有是因为整板缩放会对 board 的整族做插值，被淡出的嵌套 Text 会随父级重入场景而复原。
    @param rel 贴图相对路径
    @param edge 描边色
    @returns Group(底, 图标)
    """
    base = panel(0.84, 0.84, radius=0.18, edge=edge, stroke=2)
    return Group(base, icon(rel, height=0.62).move_to(base))


def name_weight(label: str) -> float:
    """
    名称的排版宽度权重：汉字计 1、间隔号计 0.55，用来判断单行放不放得下。
    @param label 魔之楔名称
    @returns 权重和
    """
    return sum(0.55 if ch in "·・" else 1.0 for ch in label)


def mod_name(label: str) -> VGroup:
    """
    魔之楔名称：单行放得下就一行，放不下则优先在间隔号处折成两行（间隔号留在行尾）。
    对齐态 8 格只有 1.42 的格距，长名称不折行会与邻格串成一团。
    @param label 魔之楔名称
    @returns 一或两段文字组成的 VGroup
    """
    if name_weight(label) <= NAME_MAX_WEIGHT:
        return VGroup(tx(label, size=MOD_NAME_SIZE, color=TXT2))
    chunks = label.split("·")
    head = chunks[0]
    for chunk in chunks[1:]:
        if name_weight(f"{head}·{chunk}") > NAME_MAX_WEIGHT:
            break
        head = f"{head}·{chunk}"
    tail = label[len(head) + 1:]
    return VGroup(tx(head, size=MOD_NAME_SIZE, color=TXT2),
                  tx(tail, size=MOD_NAME_SIZE, color=TXT2)).arrange(DOWN, buff=0.03)


def loadout_cell(icon_name: str, label: str, quality: str) -> tuple[Group, VGroup]:
    """
    配装板单元格：品质描边底框 ＋ 魔之楔图标；名称单独返回，便于整板缩小时一并淡出。
    @param icon_name 贴图名（不含 `T_Mod_` 前缀与扩展名）
    @param label 魔之楔名称
    @param quality 品质（金 / 紫 / 蓝）
    @returns (图标格, 名称)
    """
    base = panel(MOD_ICON_H + 0.14, MOD_ICON_H + 0.14, radius=0.08,
                 edge=QUALITY_EDGE.get(quality, PANEL_EDGE), stroke=1.7)
    ic = icon(f"webp/T_Mod_{icon_name}.webp", height=MOD_ICON_H).move_to(base)
    return Group(base, ic), mod_name(label)


def count_badge(n: int) -> VGroup:
    """
    重复魔之楔的数量角标（×N）：同名只出一张卡，压在格子右上角标携带枚数。
    @param n 该魔之楔在槽内携带的枚数
    @returns VGroup(底, 文本)
    """
    t = tx(f"×{n}", size=17, color=GOLD, bold=True)
    box = RoundedRectangle(width=t.get_width() + 0.20, height=t.get_height() + 0.08,
                           corner_radius=0.06, fill_color="#241A06", fill_opacity=0.96,
                           stroke_color=GOLD, stroke_width=1.5)
    t.move_to(box)
    return VGroup(box, t)


def series_rank(raw: tuple) -> dict:
    """
    各系列在槽内的首次出现次序，用于同系列聚拢时保持稳定。
    @param raw [(系列, 贴图名, 名称, 品质), ...]
    @returns {系列: 次序}
    """
    rank: dict = {}
    for series, *_rest in raw:
        rank.setdefault(series, len(rank))
    return rank


def equal_xs(n: int, pitch: float) -> list:
    """
    等距且整体居中的横坐标序列。
    @param n 格数
    @param pitch 相邻格距
    @returns n 个横坐标
    """
    return [(i - (n - 1) / 2) * pitch for i in range(n)]


def merge_slots(raw: tuple) -> list:
    """
    把一槽的 8 个物位按同名合并：同名只留首次出现的那一件并记下枚数，再按系列聚拢排序。
    @param raw [(系列, 贴图名, 名称, 品质), ...]
    @returns [(系列, 贴图名, 名称, 品质, 枚数), ...]
    """
    rank = series_rank(raw)
    kept, counts = [], {}
    for series, icon_name, label, quality in raw:
        if label in counts:
            counts[label] += 1
        else:
            counts[label] = 1
            kept.append((series, icon_name, label, quality))
    kept.sort(key=lambda m: rank[m[0]])
    return [(s, ic, lb, q, counts[lb]) for s, ic, lb, q in kept]


def merged_row_xs(merged_rows: list) -> list:
    """
    合并态各分组的横坐标：以「间隔最多的一排」定基准跨度，其余排把富余量摊回各间隔，
    这样三排左右边缘与槽位标签才会对齐（合并重复项后角色槽只剩 6 格，天然比另两排窄）。
    @param merged_rows 每排合并后的分组列表
    @returns 每排一组横坐标（与各排分组等长）
    """
    span_ratio = 1 + EXTRA_GAP / GROUP_GAP
    weights = []
    for merged in merged_rows:
        crossings = sum(1 for i in range(1, len(merged)) if merged[i][0] != merged[i - 1][0])
        weights.append((len(merged) - 1 - crossings) + crossings * span_ratio)
    span_target = GROUP_GAP * max(weights)

    rows = []
    for merged, weight in zip(merged_rows, weights):
        gap = span_target / weight
        xs, cur, prev = [], 0.0, None
        for series, *_rest in merged:
            if prev is not None:
                cur += gap * (span_ratio if series != prev else 1.0)
            xs.append(cur)
            prev = series
        rows.append([x - xs[-1] / 2 for x in xs])
    return rows


class S12(Shot):
    shot_id = 12

    # 技能流相对武器流要换掉的三个物位：(槽位, 旧贴图, 旧名, 新贴图, 新名, 右侧说明)
    SWAPS = (
        ("角色槽", "Typhon01_Red", "全盛·追袭", "Typhon01_Red", "全盛·背水", "−50% 技能伤害 → 换背水"),
        ("角色槽", "Siren01_Red", "羽翼·鼓舞·昂扬", "Mephisto01_Red", "涅槃·决断", "技能威力 → 574%"),
        ("近战槽", "Fenrir01", "时运", "Fenrir01", "穿花刺骨", "双刀滑铲招式 · 威力 +100%"),
    )

    def construct(self):
        self.intro()

        # 顶部：这是两套流派的共同基础模板
        banner = mk("**基础配装** · 武器流", size=28, strong=WEAPON).move_to([0, 3.10, 0])
        self.at(self.T(0), FadeIn(banner, shift=DOWN * 0.12), run_time=0.5)

        # 上排武器：近战 无声的嘶吼 / 远程 血染织羽
        # 卡高 0.84、中心 2.34 —— 卡顶 2.76 距横幅底边 3.00 留 0.24，
        # 名称底边 1.66 距角色槽图标顶边 1.35 留 0.31。
        # 名称单独持有（不进 board）：整板缩小时它要独立退场，否则会被父级重入场景而复原
        wp0 = weapon_pill("webp/T_Head_Dualblade_Wusheng.webp", FIRE)
        wp1 = weapon_pill("webp/T_Head_Crossbow_Yemei.webp", CALAM)
        weap = Group(wp0, wp1).arrange(RIGHT, buff=1.8).move_to([0, 2.34, 0])
        weap_labels = VGroup(
            tx("近战 · 无声的嘶吼", size=19, color=TXT2).next_to(wp0, DOWN, buff=0.12),
            tx("远程 · 血染织羽", size=19, color=TXT2).next_to(wp1, DOWN, buff=0.12),
        )
        self.at(self.T(1), FadeIn(weap, lag_ratio=0.12), FadeIn(weap_labels), run_time=0.8)

        # 三排魔之楔：三拍推进 —— 按 BD 顺序等距排开全 8 格 → 同系列聚拢 → 同名合并成一张 ×N。
        # 卡片与名称都留在场景顶层、逐对象驱动：一旦塞进父组，父级的 Transform 会把已淡出的文字拉回场景
        merged_rows = [merge_slots(raw) for _slot, raw in LOADOUT_RAW]
        merged_xs = merged_row_xs(merged_rows)

        cells, names, tags, badges = [], [], [], []
        raw_xs, grp_xs, mrg_xs, group_of, keeper = [], [], [], [], []
        for row, (slot, raw) in enumerate(LOADOUT_RAW):
            y = MOD_ROW_Y[row]
            rank = series_rank(raw)
            merged = merged_rows[row]

            # 对齐态：BD 原顺序等距
            raw_xs.append(equal_xs(len(raw), RAW_PITCH))
            # 聚拢态：按系列首次出现次序稳定重排后等距（仍是 8 格，只换位置）
            gx = equal_xs(len(raw), GROUP_PITCH)
            gpos = [0.0] * len(raw)
            for pos, i in enumerate(sorted(range(len(raw)), key=lambda i: (rank[raw[i][0]], i))):
                gpos[i] = gx[pos]
            grp_xs.append(gpos)
            # 合并态：同名的若干格共用第一张卡的位置
            slot_of_label = {m[2]: k for k, m in enumerate(merged)}
            mpos, gidx, keep = [], [], {}
            for i, (_s, _ic, label, _q) in enumerate(raw):
                k = slot_of_label[label]
                mpos.append(merged_xs[row][k])
                gidx.append(k)
                keep.setdefault(k, i)
            mrg_xs.append(mpos)
            group_of.append(gidx)
            keeper.append(keep)

            row_cells, row_names = [], []
            for i, (_series, icon_name, label, quality) in enumerate(raw):
                cell, nm = loadout_cell(icon_name, label, quality)
                cell.move_to([raw_xs[row][i], y, 0])
                nm.next_to(cell, DOWN, buff=0.05)
                row_cells.append(cell)
                row_names.append(nm)
            cells.append(row_cells)
            names.append(row_names)

            # 槽位标签贴在本行左端（对齐态与合并态左边缘几乎重合，取更左的那个）
            tag = chip(slot, TXT3, size=19, fill_opacity=0.09, text_color=TXT2)
            left = min(raw_xs[row][0], merged_xs[row][0]) - MOD_ICON_H / 2 - 0.07
            tag.move_to([left - 0.5 - tag.get_width() / 2, y, 0])
            tags.append(tag)

            for k, m in enumerate(merged):
                if m[4] > 1:
                    badges.append(count_badge(m[4]).move_to(
                        [merged_xs[row][k] + MOD_ICON_H / 2 + 0.07, y + MOD_ICON_H / 2 + 0.07, 0],
                        aligned_edge=UR).shift([-0.015, -0.015, 0]))

        # 第 2 句「各八格」：三排按 BD 顺序等距排开，逐排浮出
        for row in range(len(LOADOUT_RAW)):
            anims = [FadeIn(tags[row])]
            for cell, nm in zip(cells[row], names[row]):
                anims += [FadeIn(cell), FadeIn(nm)]
            self.at(self.T(2, row * 1.15), *anims, run_time=0.62)

        # 聚拢与合并都是「置换」：文字在交叉处必然叠成一团，所以先撤下名称，只让卡片走位
        all_names = VGroup(*[nm for row_names in names for nm in row_names])
        self.at(self.E(2, -2.26), FadeOut(all_names), run_time=0.26)

        # 第 2 句收尾：同系列聚拢（8 格只换位置）
        gather = []
        for row in range(len(LOADOUT_RAW)):
            for i in range(len(LOADOUT_RAW[row][1])):
                dx = grp_xs[row][i] - raw_xs[row][i]
                if abs(dx) > 1e-6:
                    gather.append(cells[row][i].animate.shift([dx, 0, 0]))
        self.at(self.E(2, -2.20), *gather, run_time=0.80)

        # 第 3 句前：同名合并 —— 多出来的卡片并到第一张上淡出，留下的滑到合并态位置，×N 角标压上去
        merge = []
        for row in range(len(LOADOUT_RAW)):
            for i in range(len(LOADOUT_RAW[row][1])):
                dx = mrg_xs[row][i] - grp_xs[row][i]
                if keeper[row][group_of[row][i]] == i:
                    merge.append(cells[row][i].animate.shift([dx, 0, 0]))
                else:
                    merge.append(FadeOut(cells[row][i], shift=[dx, 0, 0]))
        self.at(self.E(2, -1.20), *merge, *[FadeIn(b, shift=DOWN * 0.08) for b in badges], run_time=0.66)

        # 第 3 句「这三排就是基础配装」：说明文字与横幅先退场，配装主体缩小上移成为模板。
        # 逐对象缩放平移（不借助父组）：目标是让整块的形心落到 [0, 1.8] 并等比缩到 0.52；
        # 横幅不留进模板 —— 缩到 0.52 后它会与镜头条落在同一行，看上去像条头文字。
        shrink_pool = [weap, *tags, *[c for row_cells in cells for c in row_cells]]
        pivot = Group(*shrink_pool).get_center()
        target = np.array([0.0, 1.80, 0.0])

        def to_template(m: Mobject) -> Animation:
            """把对象等比缩到 0.52 并落到模板态坐标。"""
            return m.animate.scale(0.52).move_to(target + (m.get_center() - pivot) * 0.52)

        self.at(self.T(3, -0.25), FadeOut(banner), FadeOut(weap_labels),
                *[FadeOut(b) for b in badges], run_time=0.32)
        self.at(self.T(3, 0.15), *[to_template(m) for m in shrink_pool], run_time=0.85)

        # 下半屏：技能流只换三处
        head = mk("技能流只换 **3 处**", size=26, strong=SKILL).move_to([0, 0.28, 0])
        self.at(self.T(4), FadeIn(head, shift=UP * 0.1), run_time=0.5)

        for k, (slot, o_icon, o_name, n_icon, n_name, note) in enumerate(self.SWAPS):
            y = -0.32 - k * 0.60
            tg = chip(slot, TXT3, size=17, fill_opacity=0.08, text_color=TXT3).move_to([-6.5, y, 0])
            oi = icon(f"webp/T_Mod_{o_icon}.webp", height=0.46).move_to([-5.78, y, 0])
            on = tx(o_name, size=19, color=TXT3).move_to([-5.4, y, 0], aligned_edge=LEFT)
            ar = tx("→", size=26, color=TXT3).move_to([-2.3, y, 0])
            ni = icon(f"webp/T_Mod_{n_icon}.webp", height=0.46).move_to([-1.72, y, 0])
            nn = tx(n_name, size=19, color=SKILL).move_to([-1.34, y, 0], aligned_edge=LEFT)
            nv = tx(note, size=17, color=TXT2).move_to([6.6, y, 0], aligned_edge=RIGHT)
            self.at(self.T(5 + k), FadeIn(tg), FadeIn(oi, shift=RIGHT * 0.18), FadeIn(on),
                    FadeIn(ar), FadeIn(ni, shift=RIGHT * 0.18), FadeIn(nn), FadeIn(nv), run_time=0.5)

        # 收口：两套的循环与数值对照
        s1 = mk("技能流 · 循环 **1.5s** · 技能侧 **65%**", size=22, strong=SKILL).move_to([-3.3, -2.14, 0])
        s2 = mk("武器流 · 循环 **2.7s** · 羽化 **82%**", size=22, strong=WEAPON).move_to([3.3, -2.14, 0])
        s3 = mk("本体数值：技能流 **61 亿**（48＋13） ｜ 武器流 **66 亿**", size=22, strong=GOLD).move_to([0, -2.66, 0])

        self.at(self.T(8), FadeIn(s1, shift=RIGHT * 0.1), run_time=0.4)
        self.at(self.T(9), FadeIn(s2, shift=LEFT * 0.1), run_time=0.4)
        self.at(self.T(10), FadeIn(s3, shift=UP * 0.08), run_time=0.4)

        # 旁白收在「卖点在 1.5 秒的循环」——把技能流循环那句圈出来
        hl = RoundedRectangle(width=s1.get_width() + 0.36, height=s1.get_height() + 0.26,
                              corner_radius=0.08, stroke_color=GOLD, stroke_width=2,
                              fill_opacity=0).move_to(s1)
        self.at(self.T(12), FadeIn(hl, scale=1.06), run_time=0.5)

        self.outro()


# ================ 镜 13：队友——四个人，六种搭法 ================
class S13(Shot):
    shot_id = 13

    # (组合名, 本体输出亿, 是否带菲娜)
    COMBOS = (
        ("菲娜+松露", 66.0, True),
        ("菲娜+扶疏", 63.8, True),
        ("菲娜+卡米拉", 54.7, True),
        ("松露+扶疏", 49.3, False),
        ("扶疏+卡米拉", 48.4, False),
        ("松露+卡米拉", 41.1, False),
    )
    MAXV = 66.0
    BAR_X = -1.9
    SPAN = 6.4
    TOP_Y = 2.3
    ROW_H = 0.6
    SOLO_Y = -1.75
    SOLO_V = 17.4

    def _row(self, y: float, name: str, value: float, on_team: bool) -> tuple:
        """
        构造一条排名行：左侧组合名、中部条槽与填充、右侧数值。
        @param y 行中心纵坐标
        @param name 组合名
        @param value 本体输出（亿）
        @param on_team 是否带菲娜
        @returns (名称, 槽, 填充, 数值文本)
        """
        color = WEAPON if on_team else COLD
        label = tx(name, size=23, color=TXT if on_team else TXT2)
        label.move_to([self.BAR_X - self.SPAN / 2 - 0.28, y, 0], aligned_edge=RIGHT)
        # 条槽与填充都用直角矩形：圆角矩形横向拉伸会把圆角一起拉长，变成菱形
        track = Rectangle(width=self.SPAN, height=0.34, fill_color="#1C2230", fill_opacity=1,
                          stroke_color=PANEL_EDGE, stroke_width=1)
        track.move_to([self.BAR_X, y, 0])
        fill = Rectangle(width=0.02, height=0.34, fill_color=color, fill_opacity=1, stroke_width=0)
        fill.move_to(track.get_left(), aligned_edge=LEFT)
        val = num(f"{value:.1f}", size=27, color=color)
        val.move_to([self.BAR_X + self.SPAN / 2 + 0.3, y, 0], aligned_edge=LEFT)
        return label, track, fill, val

    def _grow(self, fill: Mobject, track: Mobject, value: float) -> Animation:
        """
        @param fill 填充条
        @param track 条槽
        @param value 目标输出（亿）
        @returns 填充按 MAXV 归一生长到目标宽度的动画
        """
        target = fill.copy()
        target.set_width(max(0.02, self.SPAN * value / self.MAXV), stretch=True)
        target.move_to(track.get_left(), aligned_edge=LEFT)
        return Transform(fill, target)

    def construct(self):
        self.intro()

        # 标题：队友槽只有两个，四个人凑出六种搭法
        title = mk("队友槽只有 **2 个** ⇒ **6 种搭法**", size=32, strong=GOLD).move_to([0, 3.05, 0])
        self.at(self.T(0), FadeIn(title, shift=DOWN * 0.1), run_time=0.5)

        rows = []
        for i, (name, value, on_team) in enumerate(self.COMBOS):
            y = self.TOP_Y - i * self.ROW_H
            rows.append((value,) + self._row(y, name, value, on_team))

        self.at(self.T(1), *[FadeIn(r[1]) for r in rows], *[FadeIn(r[2]) for r in rows], run_time=0.6)

        # 前三名依次生长（旁白逐个报数）
        for k in range(3):
            t = self.T(2 + k)
            self.at(t, FadeIn(rows[k][3]), run_time=0.2)
            self.at(t + 0.2, self._grow(rows[k][3], rows[k][2], rows[k][0]), run_time=0.8)
            self.at(t + 0.6, FadeIn(rows[k][4]), run_time=0.3)

        # 前三名全带菲娜：整体框出
        box = RoundedRectangle(width=self.SPAN + 2.6, height=self.ROW_H * 3 + 0.34, corner_radius=0.12,
                               stroke_color=WEAPON, stroke_width=2, fill_opacity=0)
        box.move_to([self.BAR_X + 0.05, self.TOP_Y - self.ROW_H, 0])
        self.at(self.T(5), FadeIn(box, scale=1.04), run_time=0.4)

        # 没有菲娜：最好的松露+扶疏（第 4 名）
        t = self.T(6)
        self.at(t, FadeIn(rows[3][3]), run_time=0.2)
        self.at(t + 0.2, self._grow(rows[3][3], rows[3][2], rows[3][0]), run_time=0.8)
        self.at(t + 0.6, FadeIn(rows[3][4]), run_time=0.3)

        # 剩下两组没有菲娜的搭法
        t = self.T(7)
        self.at(t, FadeIn(rows[4][3]), FadeIn(rows[5][3]), run_time=0.2)
        self.at(t + 0.2, self._grow(rows[4][3], rows[4][2], rows[4][0]),
                self._grow(rows[5][3], rows[5][2], rows[5][0]), run_time=0.8)
        self.at(t + 0.6, FadeIn(rows[4][4]), FadeIn(rows[5][4]), run_time=0.3)

        # 一个都不带：只剩 17.4 亿
        solo_lb, solo_track, solo_fill, solo_val = self._row(self.SOLO_Y, "不带队友", self.SOLO_V, False)
        self.at(self.T(8), FadeIn(solo_lb), FadeIn(solo_track), run_time=0.4)
        self.at(self.T(8, 0.4), FadeIn(solo_fill), self._grow(solo_fill, solo_track, self.SOLO_V), run_time=0.8)
        self.at(self.T(8, 1.0), FadeIn(solo_val), run_time=0.3)

        # 收口：七成半是队友给的
        hook = mk("这 66 亿里，**七成半是队友给的**", size=32, strong=SHARED).move_to([0, -2.55, 0])
        self.at(self.T(9), FadeIn(hook, scale=0.9))

        self.outro()


# ================ 镜 14：实战变体 ================
class S14(Shot):
    shot_id = 14

    def construct(self):
        self.intro()

        # 标题：共斗场景，窗口是碎的
        scene_chip = chip("共斗速切", FIRE, size=26, pad=0.16).move_to([-4.3, 2.62, 0])
        scene_desc = tx("BOSS 换得快，窗口是碎的", size=24, color=TXT2).move_to([-0.5, 2.62, 0], aligned_edge=LEFT)
        self.at(self.T(0), FadeIn(scene_chip, scale=0.88), FadeIn(scene_desc, shift=RIGHT * 0.12), run_time=0.5)

        # 比的是战技出手速度
        race = mk("比的就是谁的战技 **出得更快**", size=32, strong=FIRE).move_to([0, 1.8, 0])
        self.at(self.T(2), FadeIn(race, shift=UP * 0.1))

        # 换人：松露 → 扶疏
        swap = Group(
            icon("webp/T_Head_Songlu.webp", height=0.95),
            tx("→", size=34, color=TXT3),
            icon("webp/T_Head_Baiheng.webp", height=0.95),
        ).arrange(RIGHT, buff=0.3).move_to([-3.3, 0.75, 0])
        swap_label = chip("松露 ⇄ 扶疏", COLD, size=24).move_to([3.1, 0.75, 0])
        self.at(self.T(3), FadeIn(swap, lag_ratio=0.1), FadeIn(swap_label, scale=0.88))

        # 扶疏给的是技能速度，直接乘在出手频率上
        why = mk("扶疏给的是 **技能速度**，直接乘在出手频率上", size=28, strong=GOLD).move_to([0, -0.05, 0])
        self.at(self.T(4), FadeIn(why, shift=UP * 0.1))

        speed = Group(
            tx("技能速度", size=24, color=TXT2),
            num("+60%", size=30, color=TXT3),
            tx("→", size=26, color=TXT3),
            num("+101%", size=34, color=GOLD),
        ).arrange(RIGHT, buff=0.22).move_to([0, -0.85, 0])
        speed[-1].align_to(speed[-2], DOWN)
        self.at(self.T(5), FadeIn(speed, lag_ratio=0.08))

        # 松露的持续增伤在碎窗口里吃不满
        cons = mk("松露给的是持续增伤，碎窗口里 **吃不满**", size=24, color=TXT2).move_to([0, -1.6, 0])
        self.at(self.T(6), FadeIn(cons, shift=UP * 0.1))

        # 代价：数值小幅下降
        cost = mk("**66.04 亿 → 63.85 亿**（−3.3%）", size=30, strong=BLOOD).move_to([0, -2.4, 0])
        self.at(self.T(7), FadeIn(cost, scale=0.9))

        # 收口：两种场合各用一套
        concl = mk("**单体长桩用松露** · **共斗碎窗口用扶疏**", size=34, strong=GOLD).move_to([0, -0.05, 0])
        self.at(self.T(9), FadeOut(why), FadeOut(speed), FadeOut(cons), FadeIn(concl, scale=0.9), run_time=0.6)

        self.outro()


# ================ 镜 15：月阶 · 卡米拉定制怪 ================
class S15(Shot):
    shot_id = 15

    # (阵容名, 综合 DPS 亿, 减防比例, 是否满破防)
    TEAMS = (
        ("扶疏 + 卡米拉", 12.795, "100%", True),
        ("扶疏 + 菲娜", 10.490, "70%", False),
        ("卡米拉 + 菲娜", 8.835, "70%", False),
        ("扶疏 + 松露", 8.419, "70%", False),
        ("菲娜 + 松露", 7.923, "40%", False),
        ("卡米拉 + 松露", 6.972, "70%", False),
        ("不带队友", 4.593, "40%", False),
    )
    MAXV = 12.795
    BAR_X = -0.6
    SPAN = 4.6
    TOP_Y = 1.40
    ROW_H = 0.50
    DIS_Y = -2.05

    def _row(self, y: float, name: str, value: float, ignore: str, full: bool) -> tuple:
        """
        构造一条阵容行：左阵容名、中部条槽与填充、右侧综合 DPS 与减防比例。
        @param y 行中心纵坐标
        @param name 阵容名
        @param value 综合 DPS（亿）
        @param ignore 减防比例文本
        @param full 是否满破防
        @returns (名称, 槽, 填充, 数值, 减防)
        """
        color = GOLD if full else (COLD if value >= 5 else TXT3)
        label = tx(name, size=21, color=TXT if full else TXT2)
        label.move_to([self.BAR_X - self.SPAN / 2 - 0.3, y, 0], aligned_edge=RIGHT)
        # 条槽与填充都用直角矩形：圆角矩形横向拉伸会把圆角一起拉长
        track = Rectangle(width=self.SPAN, height=0.28, fill_color="#1C2230", fill_opacity=1,
                          stroke_color=PANEL_EDGE, stroke_width=1)
        track.move_to([self.BAR_X, y, 0])
        fill = Rectangle(width=0.02, height=0.28, fill_color=color, fill_opacity=1, stroke_width=0)
        fill.move_to(track.get_left(), aligned_edge=LEFT)
        val = VGroup(num(f"{value:.2f}", size=24, color=color), tx("亿", size=15, color=TXT3))
        val.arrange(RIGHT, buff=0.06)
        val[-1].align_to(val[0], DOWN)
        val.move_to([track.get_right()[0] + 0.24, y, 0], aligned_edge=LEFT)
        ig = tx(f"减防 {ignore}", size=16, color=GOLD if full else TXT3)
        ig.move_to([val.get_right()[0] + 0.5, y, 0], aligned_edge=LEFT)
        return label, track, fill, val, ig

    def _grow(self, fill: Mobject, track: Mobject, value: float) -> Animation:
        """
        @param fill 填充条
        @param track 条槽
        @param value 目标输出（亿）
        @returns 填充按 MAXV 归一生长到目标宽度的动画
        """
        target = fill.copy()
        target.set_width(max(0.02, self.SPAN * value / self.MAXV), stretch=True)
        target.move_to(track.get_left(), aligned_edge=LEFT)
        return Transform(fill, target)

    def construct(self):
        self.intro()

        # 顶部：月阶定制怪的战场信息
        mon = Group(
            chip("月阶 · 分组赛定制怪", FIRE, size=21),
            tx("防御", size=20, color=TXT2),
            num("1000", size=28, color=BLOOD),
            tx("无属性 · 抗性 0", size=20, color=TXT2),
        ).arrange(RIGHT, buff=0.28).move_to([0, 2.92, 0])
        self.at(self.T(0), FadeIn(mon, shift=DOWN * 0.12), run_time=0.5)

        # 防御公式：先通用式，再代入数值
        generic = mk("减伤 = **防御** ÷（300 + **防御**）", size=22, strong=FIRE).move_to([0, 2.42, 0])
        self.at(self.T(2), FadeIn(generic, shift=DOWN * 0.1), run_time=0.45)

        subst = Group(
            num("1000", size=24, color=BLOOD),
            tx(" ÷ 1300 = ", size=21, color=TXT2),
            num("77%", size=27, color=GOLD),
            tx("　　伤害只剩", size=19, color=TXT3),
            num("23%", size=22, color=TXT3),
        ).arrange(RIGHT, buff=0.06).move_to([0, 2.02, 0])
        self.at(self.T(3), FadeIn(subst, shift=DOWN * 0.1), run_time=0.45)

        # 阵容表
        rows = []
        for i, (name, value, ignore, full) in enumerate(self.TEAMS):
            rows.append((value, full) + self._row(self.TOP_Y - i * self.ROW_H, name, value, ignore, full))

        self.at(self.T(4), *[FadeIn(r[2]) for r in rows], *[FadeIn(r[3]) for r in rows], run_time=0.55)

        for lo, hi, t in ((0, 4, self.T(5)), (4, 7, self.T(6))):
            self.at(t, *[FadeIn(rows[k][4]) for k in range(lo, hi)], run_time=0.2)
            self.at(t + 0.2, *[self._grow(rows[k][4], rows[k][3], rows[k][0]) for k in range(lo, hi)], run_time=0.6)
            self.at(t + 0.6, *[FadeIn(rows[k][5]) for k in range(lo, hi)],
                    *[FadeIn(rows[k][6]) for k in range(lo, hi)], run_time=0.3)

        # 满破防那一行整体框出
        row0 = Group(rows[0][2], rows[0][3], rows[0][5], rows[0][6])
        box = RoundedRectangle(width=row0.get_width() + 0.5, height=self.ROW_H, corner_radius=0.1,
                               stroke_color=GOLD, stroke_width=2, fill_opacity=0).move_to(row0)
        self.at(self.T(6, 1.0), FadeIn(box, scale=1.02), run_time=0.4)

        # 减防拆解的三个来源
        d_head = tx("减防来源", size=18, color=TXT3)
        d1 = chip("月阶 40%", FULL, size=18)
        d2 = chip("卡米拉 7 溯 30%", GOLD, size=18)
        d3 = chip("扶疏 1 溯 30%", GOLD, size=18)
        plus1, plus2 = tx("+", size=18, color=TXT3), tx("+", size=18, color=TXT3)
        d_sum = Group(num("100%", size=26, color=GOLD), tx("满破", size=17, color=TXT3)).arrange(RIGHT, buff=0.12)
        # 先整体排布定好各段锚点，再逐段淡入，避免出现位置跳动
        Group(d_head, d1, plus1, d2, plus2, d3, d_sum).arrange(RIGHT, buff=0.2).move_to([0, self.DIS_Y, 0])
        self.at(self.T(7), FadeIn(d_head), FadeIn(d1, scale=0.9), run_time=0.45)
        self.at(self.T(8), FadeIn(plus1), FadeIn(d2, scale=0.9), FadeIn(plus2), FadeIn(d3, scale=0.9), run_time=0.5)
        self.at(self.T(9), FadeIn(d_sum, scale=0.9), run_time=0.4)

        # 断档第一
        best = chip("断档第一", GOLD, size=18).move_to([row0.get_right()[0] + 0.8, self.TOP_Y, 0])
        self.at(self.T(10), FadeIn(best, scale=0.85), run_time=0.4)

        # 卡米拉是这套阵容的门槛
        self.at(self.T(11), Indicate(rows[0][2], color=GOLD, scale_factor=1.12), run_time=0.9)

        self.outro()


# ================ 镜 16：魔灵与潜质 ================
# 四条潜质：贴图名 / 名称 / 效果 / 单条收益（撤下该条后重算综合 DPS 的变化，与前端槽位收益同口径）
TRAITS = (
    ("Battle_Gold", "振奋", "暴击伤害 +30%", "4.8%"),
    ("Battle_Gold", "激进", "暴击率 +24%", "2.3%"),
    ("Battle_Gold", "激昂", "昂扬 +7.2%", "1.8%"),
    ("Battle_Gold", "老道", "魔灵支援与被动等级 +1", "4.4%"),
)


class S16(Shot):
    shot_id = 16

    def construct(self):
        self.intro()

        # 左：魔灵本体 —— 被动与主动两条收益
        pet_title = mk("魔灵", size=26, strong=GOLD).move_to([-4.55, 2.62, 0])
        pet_icon = icon("webp/T_Head_Pet_Manao.webp", height=1.5).move_to([-4.55, 1.72, 0])
        pet_name = tx("玛瑙艾尔芙", size=25, color=TXT).move_to([-4.55, 0.80, 0])
        pet_sub = tx("lv3 · 主动覆盖率 60%", size=18, color=TXT3).move_to([-4.55, 0.45, 0])

        p_group = Group(tx("被动 · 火属性攻击", size=20, color=TXT2),
                        num("+5.7%", size=30, color=GOLD)).arrange(DOWN, buff=0.1).move_to([-4.55, -0.35, 0])
        a_group = Group(tx("主动 · 多重射击", size=20, color=TXT2),
                        num("+1.6%", size=30, color=GOLD)).arrange(DOWN, buff=0.1).move_to([-4.55, -1.45, 0])

        divider = Line([-1.78, 2.9, 0], [-1.78, -2.3, 0], stroke_color=PANEL_EDGE, stroke_width=2)
        self.at(self.T(0), FadeIn(pet_title, shift=UP * 0.1), FadeIn(divider), run_time=0.4)
        self.at(self.T(0, 0.3), FadeIn(pet_icon, scale=0.9), FadeIn(pet_name), FadeIn(pet_sub))
        self.at(self.T(1), FadeIn(p_group, shift=RIGHT * 0.12))
        self.at(self.T(2), FadeIn(a_group, shift=RIGHT * 0.12))

        # 右：四条潜质一次性亮出名称、效果与收益（旁白不逐条念）
        head = mk("潜质 **4 条** · 单条收益", size=24, strong=DISORDER).move_to([2.35, 2.62, 0])
        self.at(self.T(3), FadeIn(head, shift=DOWN * 0.1), run_time=0.45)

        trait_rows = []
        for k, (rel, name, desc, income) in enumerate(TRAITS):
            y = 1.72 - k * 0.82
            ic = icon(f"webp/T_Armory_Pet_Attr_{rel}.webp", height=0.6).move_to([-1.36, y, 0])
            nm = tx(name, size=23, color=TXT).move_to([-0.92, y, 0], aligned_edge=LEFT)
            ds = tx(desc, size=19, color=TXT2).move_to([0.85, y, 0], aligned_edge=LEFT)
            iv = num(income, size=30, color=GOLD).move_to([6.6, y, 0], aligned_edge=RIGHT)
            trait_rows.append(Group(ic, nm, ds, iv))
        self.at(self.T(3, 0.4), *[FadeIn(r, shift=RIGHT * 0.14) for r in trait_rows], run_time=0.5)

        rule = tx("单条收益 = 撤下该条后重算综合输出的变化", size=16, color=TXT3).move_to([2.35, -1.72, 0])
        self.at(self.T(3, 1.0), FadeIn(rule), run_time=0.4)

        total = mk("四条合计 → **+12.6%**", size=27, strong=GOLD).move_to([2.35, -2.28, 0])
        self.at(self.T(4, 0.2), FadeIn(total, scale=0.9))

        self.outro()


# ================ 镜 16：溯源收益 ================
class S17(Shot):
    shot_id = 17

    # (溯数, 累加输出亿, 边际提升, 是否重点溯)
    STEPS = (
        (0, 43.6, "", False),
        (1, 48.8, "+12.1%", True),
        (2, 49.2, "+0.8%", False),
        (3, 49.7, "+1.0%", False),
        (4, 53.7, "+8.1%", True),
        (5, 54.2, "+0.9%", False),
        (6, 71.0, "+31.0%", True),
    )
    # 关键溯（金色）/ 其余溯（冷色）：两批一次性展示，不做逐根递进
    KEY = (1, 4, 6)
    REST = (2, 3, 5)
    BAR_W = 0.95
    PITCH = 1.8
    BASE_Y = -1.05
    LOW, HIGH = 43.6, 71.0

    def _bar(self, idx: int, step: tuple) -> Group:
        """
        构造一根溯源阶梯条：柱体 + 顶部累加数值 + 底部溯数标签（关键溯另带边际提升）。
        @param idx 溯数
        @param step (溯数, 累加输出亿, 边际提升, 是否关键溯)
        @returns 该条的组合
        """
        _, value, margin, key = step
        height = 0.6 + 3.05 * (value - self.LOW) / (self.HIGH - self.LOW)
        x = (idx - 3) * self.PITCH
        color = GOLD if key else COLD
        rect = Rectangle(width=self.BAR_W, height=height, fill_color=color,
                         fill_opacity=0.88 if key else 0.5, stroke_color=color,
                         stroke_width=1.8 if key else 1.2)
        rect.move_to([x, self.BASE_Y + height / 2, 0])
        val = VGroup(num(f"{value:.1f}", size=25 if key else 21, color=color),
                     tx("亿", size=15 if key else 13, color=TXT3))
        val.arrange(RIGHT, buff=0.05)
        val[-1].align_to(val[0], DOWN)
        val.move_to([x, self.BASE_Y + height + 0.34, 0])
        label = tx(f"{idx} 溯", size=22, color=TXT if key else TXT2).move_to([x, self.BASE_Y - 0.46, 0])
        group = Group(rect, val, label)
        if margin:
            group.add(tx(margin, size=21 if key else 18, color=GOLD if key else TXT3).move_to([x, self.BASE_Y - 0.96, 0]))
        return group

    def construct(self):
        self.intro()

        # 这一镜不留顶部标题：信息全在柱上
        axis = Line([-6.3, self.BASE_Y, 0], [6.3, self.BASE_Y, 0], stroke_color=PANEL_EDGE, stroke_width=2)
        self.at(self.T(0), FadeIn(axis), run_time=0.35)

        steps = [self._bar(i, s) for i, s in enumerate(self.STEPS)]

        # 0 溯是打底基准，先单独立住
        self.at(self.T(0, 0.4), *[FadeIn(m, shift=UP * 0.1) for m in steps[0]], run_time=0.4)
        # 关键溯：一次性展示
        self.at(self.T(0, 0.85), *[FadeIn(steps[i], shift=UP * 0.12) for i in self.KEY], run_time=0.6)

        # 6 溯是这一镜的落点
        hl = RoundedRectangle(width=self.BAR_W + 0.3, height=steps[6][0].get_height() + 0.34,
                              corner_radius=0.08, stroke_color=GOLD, stroke_width=2.4,
                              fill_opacity=0).move_to(steps[6][0])
        self.at(self.T(1), FadeIn(hl, scale=1.05), run_time=0.4)
        self.at(self.T(1, 0.47), steps[6][3].animate.scale(1.32).set_color(GOLD), run_time=0.55)

        # 其余溯：一次性展示
        self.at(self.T(1, 1.07), *[FadeIn(steps[i], shift=UP * 0.12) for i in self.REST], run_time=0.55)

        foot = Group(chip("关键溯 1 / 4 / 6", GOLD, size=20),
                     chip("其余 2 / 3 / 5 · 小步", COLD, size=20)).arrange(RIGHT, buff=0.34)
        foot.move_to([0, -2.85, 0])
        self.at(self.T(1, 1.72), FadeIn(foot, shift=UP * 0.1), run_time=0.5)

        self.outro()


# ================ 镜 10：手法——推荐循环与收益 ================
class S10(Shot):
    shot_id = 10

    # (手法短名, 综合输出亿)，按输出升序；最后一根是推荐手法。
    # 纵轴自 58 亿起，否则 60.6 与 71.0 的差距在图上几乎看不出来。
    ROTATIONS = (
        ("1234×3 射1", 60.619),
        ("1234×1 射1", 66.013),
        ("1234×2 不射", 66.037),
        ("1234×2 射2", 67.201),
        ("1234×1+123 射1", 69.934),
        ("1234×1+1 奔2", 70.437),
        ("1234×1+12 射1", 70.562),
        ("1234×1+1 射1", 71.016),
    )
    FLOOR, CEIL = 58.0, 72.0
    BAR_X0, BAR_PITCH = -5.0, 1.42
    BASE_Y, TOP_H = -0.95, 2.75

    def _h(self, value: float) -> float:
        """@returns 该输出值对应的条高（世界坐标）"""
        return self.TOP_H * (value - self.FLOOR) / (self.CEIL - self.FLOOR)

    def construct(self):
        self.intro()

        # 顶部只给口径：这是全片的落点
        title = mk("核心目标：卡[衰朽]掉血上限 · 穿插远程射击",
                   size=27, term=COLD, strong=GOLD).move_to([0, 3.05, 0])
        self.at(self.T(0), FadeIn(title, shift=DOWN * 0.12), run_time=0.5)

        # 图表：横轴八种手法，纵轴综合输出
        right = self.BAR_X0 + (len(self.ROTATIONS) - 1) * self.BAR_PITCH + 0.62
        left = self.BAR_X0 - 0.62
        axis = Line([left, self.BASE_Y, 0], [right, self.BASE_Y, 0], stroke_color=PANEL_EDGE, stroke_width=2)
        grid = VGroup()
        for tick in (60, 65, 70):
            yy = self.BASE_Y + self._h(tick)
            grid.add(DashedLine([left, yy, 0], [right, yy, 0], stroke_color="#232A38",
                                stroke_width=1.4, dash_length=0.09))
            grid.add(tx(f"{tick}", size=15, color=TXT3).move_to([left - 0.36, yy, 0]))
        note = tx("纵轴自 58 亿起 · 单位 亿", size=14, color=TXT3).move_to([left + 1.05, self.BASE_Y - 0.62, 0])

        bars, vals, labs, chart = [], [], [], VGroup(axis, grid)
        for i, (name, value) in enumerate(self.ROTATIONS):
            x = self.BAR_X0 + i * self.BAR_PITCH
            key = i == len(self.ROTATIONS) - 1
            color = GOLD if key else WEAPON
            bar = Rectangle(width=0.62, height=self._h(value), fill_color=color,
                            fill_opacity=0.9 if key else 0.45, stroke_color=color, stroke_width=1.2)
            bar.move_to([x, self.BASE_Y, 0], aligned_edge=DOWN)
            val = num(f"{value:.1f}", size=15, color=color).next_to(bar, UP, buff=0.1)
            lab = tx(name, size=14, color=GOLD if key else TXT2).move_to([x, self.BASE_Y - 0.3, 0])
            bars.append(bar)
            vals.append(val)
            labs.append(lab)
            chart.add(bar, val, lab)

        self.at(self.T(1), FadeIn(axis), FadeIn(grid, lag_ratio=0.06), FadeIn(note), run_time=0.5)
        # 每根条的动画必须比排布间隔短，否则调度会一路落后
        for i, bar in enumerate(bars):
            self.at(self.T(1, 0.45 + i * 0.36), GrowFromEdge(bar, DOWN), FadeIn(vals[i], shift=UP * 0.08),
                    FadeIn(labs[i]), run_time=0.32)

        # 最高的那一根就是推荐手法
        top = bars[-1]
        hl = RoundedRectangle(width=0.92, height=top.get_height() + 0.34, corner_radius=0.08,
                              stroke_color=GOLD, stroke_width=2.4, fill_opacity=0).move_to(top)
        crown = mk("**推荐手法**", size=21, strong=GOLD).next_to(vals[-1], UP, buff=0.12)
        self.at(self.T(2), FadeIn(hl, scale=1.05), FadeIn(crown, shift=DOWN * 0.1), run_time=0.5)

        # 图看完了就退场，把画面让给结论
        self.at(self.T(3), FadeOut(chart), FadeOut(hl), FadeOut(crown), FadeOut(note), run_time=0.55)

        steps = Group(
            chip("一轮完整连招", SKILL, size=23),
            tx("→", size=28, color=TXT3),
            chip("补一下平砍", SKILL, size=23),
            tx("→", size=28, color=TXT3),
            chip("一枪", CALAM, size=23),
            tx("→", size=28, color=TXT3),
            chip("一次奔袭", SKILL, size=23),
        ).arrange(RIGHT, buff=0.22).move_to([0, 1.35, 0])
        self.at(self.T(3, 0.55), FadeIn(steps, lag_ratio=0.07), run_time=0.8)

        dur = Group(tx("循环", size=24, color=TXT2), num("2.73", size=40, color=GOLD),
                    tx("秒", size=22, color=TXT3)).arrange(RIGHT, buff=0.16)
        bleed = Group(tx("掉血", size=24, color=TXT2), num("24", size=40, color=BLOOD),
                      tx("% / 秒", size=22, color=TXT3)).arrange(RIGHT, buff=0.16)
        Group(dur, bleed).arrange(RIGHT, buff=1.3).move_to([0, 0.18, 0])
        cap = tx("两条掉血上限全部打满", size=20, color=TXT3).move_to([0, -0.52, 0])
        self.at(self.T(4), FadeIn(dur, scale=0.92), FadeIn(bleed, scale=0.92), run_time=0.5)
        self.at(self.T(4, 0.8), FadeIn(cap, shift=UP * 0.08), run_time=0.4)

        once = mk("远程[衰朽]：**一枪就到上限**", size=27, term=COLD, strong=GOLD).move_to([0, -1.35, 0])
        self.at(self.T(5), FadeIn(once, shift=UP * 0.1), run_time=0.5)

        result = Group(num("71.0", size=50, color=GOLD), tx("亿", size=27, color=TXT3),
                       mk("（比不射击高 **7.5%**）", size=25, strong=SHARED)).arrange(RIGHT, buff=0.2)
        result[-1].align_to(result[-2], DOWN)
        result.move_to([0, -2.25, 0])
        self.at(self.T(6), FadeIn(result, scale=0.9))

        self.outro()


# ================ 镜 17：结尾 ================
class S18(Shot):
    shot_id = 18

    # 全片公式回顾：左边是原料 / 投入，右边是它换出来的东西
    LEDGER = (
        ("血", "觉醒"),
        ("紊乱", "灾厄"),
        ("充盈", "换算率"),
        ("掉血", "上限"),
        ("队友", "天花板"),
    )

    def construct(self):
        self.intro()

        # 开场那句账本比喻，在结尾收回
        head = icon("webp/T_Head_Falu.webp", height=1.8).move_to([-1.15, 2.42, 0])
        skin = icon("webp/T_Head_Falu01.webp", height=1.8).move_to([1.15, 2.42, 0])
        g1 = glow("fire", height=2.8, opacity=0.45).move_to(head)
        g2 = glow("fire", height=2.8, opacity=0.45).move_to(skin)
        self.at(self.T(0), FadeIn(g1, scale=1.1), FadeIn(g2, scale=1.1),
                FadeIn(head, scale=0.95), FadeIn(skin, scale=0.95), run_time=0.6)

        lead = mk("回到开头那句：**我的账记在自己身上，她的账记在敌人身上**",
                  size=25, strong=GOLD).move_to([0, 1.02, 0])
        self.at(self.T(0, 0.6), FadeIn(lead, shift=UP * 0.12))

        # 五条公式一屏排开
        pairs = VGroup()
        for left, right in self.LEDGER:
            pairs.add(VGroup(tx(left, size=22, color=TXT2), tx("→", size=20, color=TXT3),
                             mk(f"**{right}**", size=24, strong=GOLD)).arrange(RIGHT, buff=0.13))
        pairs.arrange(RIGHT, buff=0.5).move_to([0, 0.12, 0])
        self.at(self.T(1), *[FadeIn(pairs[k], shift=UP * 0.1) for k in range(3)], run_time=0.55)
        self.at(self.T(2), FadeIn(pairs[3], shift=UP * 0.1), FadeIn(pairs[4], shift=UP * 0.1), run_time=0.45)

        take = mk("**配装不用动，手法只改一处：一轮连招加一枪**", size=31, strong=FIRE).move_to([0, -0.95, 0])
        self.at(self.T(3), FadeIn(take, scale=0.92), run_time=0.6)

        credit = mk("记在**敌人**身上的账，就是这么算的", size=25, strong=DISORDER).move_to([0, -1.85, 0])
        self.at(self.T(4), FadeIn(credit, shift=UP * 0.1), run_time=0.5)

        self.outro()


# ================ 镜 19：参考文献（静音页） ================
# 全片引用的四份线上构筑，作者均为盲目吃鱼；右侧是站内构筑编号，可在 DNA Builder 上按编号找到原稿
REFS = (
    ("法露茜 扶疏卡米拉对单DPS估算", "LfeqJIQP0l"),
    ("法露茜 菲娜卡米拉对单DPS估算 精细对轴", "Ma7XFD2dWr"),
    ("法露茜 菲娜松露对单DPS估算 精细对轴", "ZaVADWb19J"),
    ("法露茜 菲娜扶疏对单DPS估算 精细对轴", "tEiOGGd_rI"),
)


class S19(Shot):
    """静音页：这一幕没有旁白，节奏按阅读速度排。"""

    shot_id = 19

    ROW_W = 11.0
    ROW_H = 0.52
    ROW_Y = 1.36
    ROW_GAP = 0.60

    def construct(self):
        # 静音页没有 cue 可挂，所有时刻都是镜内绝对秒数；intro() 先吃掉 0.5 秒，故从 0.55 起排
        self.intro()

        head = Group(tx("参考文献", size=36, color=TXT, bold=True),
                     tx("REFERENCES", size=15, color=TXT3, font=NUM)).arrange(RIGHT, buff=0.26)
        head.move_to([0, 2.74, 0])
        self.at(0.55, FadeIn(head, shift=DOWN * 0.1), run_time=0.5)

        src = Group(chip("来源 · DNA Builder 线上构筑", FULL, size=18),
                    chip("作者 盲目吃鱼", GOLD, size=18)).arrange(RIGHT, buff=0.3)
        src.move_to([0, 2.06, 0])
        self.at(1.0, FadeIn(src, shift=DOWN * 0.08), run_time=0.5)

        # 四份引用，一行一份：序号 · 标题 · 站内编号
        rows = []
        for i, (title, code) in enumerate(REFS):
            y = self.ROW_Y - i * self.ROW_GAP
            base = panel(self.ROW_W, self.ROW_H, radius=0.09, opacity=0.8).move_to([0, y, 0])
            no = num(f"{i + 1:02d}", size=17, color=TXT3)
            no.move_to([-self.ROW_W / 2 + 0.34, y, 0], aligned_edge=LEFT)
            name = tx(title, size=21, color=TXT if i == 0 else TXT2)
            name.move_to([-self.ROW_W / 2 + 0.96, y, 0], aligned_edge=LEFT)
            bid = num(code, size=16, color=TXT3)
            bid.move_to([self.ROW_W / 2 - 0.28, y, 0], aligned_edge=RIGHT)
            rows.append(Group(base, no, name, bid))

        self.at(1.7, *[FadeIn(rows[k], shift=RIGHT * 0.1) for k in (0, 1)], run_time=0.55)
        self.at(2.5, *[FadeIn(rows[k], shift=RIGHT * 0.1) for k in (2, 3)], run_time=0.55)

        use = Group(chip("减防叠加", FULL, size=17), chip("防御乘区", FULL, size=17),
                    chip("阵容比对", FULL, size=17)).arrange(RIGHT, buff=0.24)
        tip = tx("全部在站内复现", size=17, color=TXT3)
        Group(use, tip).arrange(RIGHT, buff=0.3).move_to([0, -1.30, 0])
        self.at(3.35, FadeIn(tip), *[FadeIn(c, scale=0.9) for c in use], run_time=0.55)

        foot = Group(tx("数据与计算", size=19, color=TXT3),
                     num("DNA Builder", size=22, color=FULL),
                     tx("·", size=18, color=TXT3),
                     num("dna-builder.cn", size=22, color=FULL)).arrange(RIGHT, buff=0.24)
        foot.move_to([0, -2.15, 0])
        self.at(4.2, FadeIn(foot, shift=DOWN * 0.08), run_time=0.55)

        self.outro()


# ================ 镜 20：DNA Builder · 搜索演示 ================
# 品牌收尾：官方应用图标 + 品牌名 + 网址 + 搜索栏（打字 → 悬停 → 点击 → 水波纹）
LOGO = "E:/dev/dna-builder/public/app-icon.png"


class S20(Shot):
    shot_id = 20

    QUERY = "二重螺旋dob"
    BOX_W, BOX_H, BOX_Y = 8.8, 0.96, 0.02
    BTN_W, BTN_H = 1.52, 0.64
    TYPE_STEP = 0.12                      # 每个字的打字时间
    # 鼠标指针多边形：尖端在原点，向右下张开（屏幕坐标 y 向下，这里已翻成 y 向上）
    CURSOR_PTS = ((0.0, 0.0), (0.0, -1.0), (0.25, -0.75), (0.44, -1.13),
                  (0.56, -1.06), (0.38, -0.69), (0.69, -0.69))

    def _pointer(self, tip, scale: float = 0.62) -> Polygon:
        """
        鼠标指针图形（尖端落在 tip 上）。
        @param tip 尖端位置
        @param scale 缩放
        @returns Polygon
        """
        return Polygon(*[[tip[0] + x * scale, tip[1] + y * scale, 0] for x, y in self.CURSOR_PTS],
                       fill_color="#F3F5F9", fill_opacity=1, stroke_color=BG, stroke_width=3)

    def construct(self):
        self.intro()
        t0 = self.T(0)

        # —— 品牌区 ——
        logo = icon(LOGO, height=1.02)
        brand = tx("DNA Builder", size=42, color=TXT, bold=True, font=NUM)
        tag = tx("二重螺旋 构筑与配装计算站", size=20, color=TXT3)
        block = Group(logo, VGroup(brand, tag).arrange(DOWN, aligned_edge=LEFT, buff=0.1))
        block.arrange(RIGHT, buff=0.34).move_to([0, 2.42, 0])
        self.at(t0, FadeIn(glow("full", height=2.6, opacity=0.32).move_to(block), scale=1.15),
                FadeIn(block, shift=DOWN * 0.12), run_time=0.6)

        site = chip("dna-builder.cn", FULL, size=20).move_to([0, 1.26, 0])
        self.at(t0 + 0.6, FadeIn(site, scale=0.9), run_time=0.45)

        # —— 搜索栏：放大镜 + 输入区 + 搜索按钮 ——
        box = panel(self.BOX_W, self.BOX_H, radius=0.14, opacity=0.95, stroke=2).move_to([0, self.BOX_Y, 0])
        lens = Circle(radius=0.135, stroke_color=TXT3, stroke_width=2.6, fill_opacity=0)
        lens.move_to([-self.BOX_W / 2 + 0.52, self.BOX_Y, 0])
        stem = Line(lens.get_center() + DR * 0.095, lens.get_center() + DR * 0.21,
                    stroke_color=TXT3, stroke_width=2.6)
        TIP_X = -self.BOX_W / 2 + 0.88
        btn_cx = self.BOX_W / 2 - 0.17 - self.BTN_W / 2
        btn = RoundedRectangle(width=self.BTN_W, height=self.BTN_H, corner_radius=0.13,
                               fill_color=FIRE, fill_opacity=0.92, stroke_width=0)
        btn.move_to([btn_cx, self.BOX_Y, 0])
        btn_txt = tx("搜索", size=23, color=BG, bold=True).move_to(btn)
        BTN = VGroup(btn, btn_txt)
        BTN.set_z_index(6)

        # 打字动画：已打出的字数由 typed_n 决定、整体可见度由 typed_vis 决定（双 tracker 定式）；
        # 两者都只驱动「裸 Text / 裸 Rectangle」，避免 VGroup 子对象数量变化让 become 对错位
        typed_n = ValueTracker(1.0)
        typed_vis = ValueTracker(0.0)

        def build_typed() -> Text:
            t = tx(self.QUERY[:int(round(typed_n.get_value()))], size=26, color=TXT)
            t.move_to([TIP_X, self.BOX_Y, 0], aligned_edge=LEFT)
            t.set_opacity(typed_vis.get_value())
            t.set_z_index(5)
            return t

        def build_caret() -> Rectangle:
            probe = tx(self.QUERY[:int(round(typed_n.get_value()))], size=26)
            c = Rectangle(width=0.03, height=0.38, fill_color=FULL, stroke_width=0)
            c.set_fill(FULL, 0.9 * typed_vis.get_value())
            c.move_to([TIP_X + probe.get_width() + 0.06, self.BOX_Y, 0], aligned_edge=LEFT)
            c.set_z_index(6)
            return c

        typed, caret = always_redraw(build_typed), always_redraw(build_caret)
        self.add(typed, caret)
        self.at(t0 + 1.0, FadeIn(box, scale=0.98), FadeIn(lens), FadeIn(stem), FadeIn(BTN, scale=0.94),
                typed_vis.animate.set_value(1), run_time=0.5)

        self.at(t0 + 1.3, typed_n.animate.set_value(len(self.QUERY)),
                run_time=self.TYPE_STEP * len(self.QUERY), rate_func=linear)
        # 打字结束后把两个 always_redraw 收干：先对齐到终态再摘掉更新器，省掉后续每帧重建文本
        typed.become(build_typed())
        caret.become(build_caret())
        typed.clear_updaters()
        caret.clear_updaters()

        # —— 鼠标移入 → 悬停 → 点击 → 水波纹 ——
        tip_from = [btn_cx + 2.6, self.BOX_Y - 1.9, 0]
        tip_to = [btn_cx + 0.30, self.BOX_Y - 0.30, 0]
        self.until(t0 + 2.4)
        cur = self._pointer(tip_from)
        cur.set_z_index(20)
        self.add(cur)
        self.play(cur.animate.shift(np.array(tip_to) - np.array(tip_from)), run_time=0.6)
        self.play(FadeIn(glow("full", height=1.8, opacity=0.5).move_to(btn), scale=1.1),
                  BTN.animate.scale(1.06), run_time=0.22)
        self.play(BTN.animate.scale(0.94), run_time=0.09)

        ripple_p = ValueTracker(0.0)

        def build_ripple() -> VGroup:
            """三圈相位错开的同心圆，从按钮中心外扩并淡出。"""
            p = ripple_p.get_value()
            rings = VGroup()
            for k in range(3):
                ph = (p + k / 3.0) % 1.0
                c = Circle(radius=0.18 + 0.62 * ph, stroke_color=FULL,
                           stroke_width=0.6 + 3.0 * (1 - ph), fill_opacity=0)
                c.set_stroke(opacity=0.85 * (1 - ph) ** 1.4)
                c.move_to(btn.get_center())
                rings.add(c)
            rings.set_z_index(3)
            return rings

        wave = always_redraw(build_ripple)
        self.add(wave)
        # 回弹恢复悬停态（0.94 → 1/0.94），三圈水波同时在 0.85 秒里走完一个相位
        self.play(BTN.animate.scale(1.0 / 0.94), ripple_p.animate.set_value(1.0),
                  run_time=0.85, rate_func=linear)
        self.remove(wave)

        use = Group(chip("构筑计算", FULL, size=17), chip("数值估算", FULL, size=17),
                    chip("共享构筑", FULL, size=17)).arrange(RIGHT, buff=0.26).move_to([0, -1.28, 0])
        self.at(self.T(1) + 0.25, *[FadeIn(c, scale=0.9) for c in use], run_time=0.55)

        self.outro()
