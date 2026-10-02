# 法露茜攻略视频（ManimGL 管线）

用 ManimGL 程序化渲染的《二重螺旋》法露茜机制攻略视频，约 8 分钟 / 20 个分镜。
画面全部由代码生成（无外部视频素材），旁白由 GPT-SoVITS 按口播文本合成。

## 管线总览

```
narration.py   唯一口径源：旁白 / 字幕 / 镜标题（20 镜逐行定义）
   │
   ├─► tts/synth.py        按口播文本合成并缓存 TTS → tts/wav/*.wav + manifest.json
   │      （--only N 单镜重跑 · --force 强制 · --speed 1.32 变速，音高不变）
   │
   └─► plan.py             生成全片时间轴 timing.json（镜头时长、每行字幕起止，对齐到帧）
          │
          ├─► render_video_only.py --hd   渲染 20 镜 1080p 视频并拼接（无音轨）
          │
          └─► build_audio.py --check      按时间轴合成音轨并校验对位
                 │
                 └─► make_final.py        画面 + 音轨 → renders/falu_guide_hd.mp4
                        │
                        └─► check_sync.py 成片音画同步校验（ASR 比对字幕）
```

## 目录结构

| 路径 | 说明 |
| --- | --- |
| `narration.py` | 全片文案唯一口径（改文案只改这里） |
| `shots.py` | 20 个镜头的 ManimGL 实现（`Shot` 基类 + `S01`–`S20`） |
| `common.py` | 视觉规范与工具函数（配色 / panel / chip / 文本 / HUD / 进度条） |
| `plan.py` | 时间轴编排（句间停顿、镜首尾留白） |
| `render_video_only.py` / `make_final.py` / `build_audio.py` / `check_sync.py` | 渲染、拼接、音轨、校验 |
| `tts/` | GPT-SoVITS 合成器封装（`synth.py` / `asr.py` / `qc.py`）+ 参考音频 |
| `assets/` | 背景、辉光纹理等素材（`icon()` 使用的应用图标等） |
| `custom_config.yml` | manimgl 输出配置 |
| `renders/` `frames/` `cache/` `timing.json` `tts/wav/` | 生成产物，已忽略，管线可重建 |

## 环境依赖

- **ManimGL v1.7.2**（本机 `D:/dev/manim`，含 Cairo / OpenGL 渲染后端）
- **GPT-SoVITS v2** 推理环境（`E:/soft/GPT-SoVITS-v2`，其 runtime 自带 ffmpeg 与 Python 3.9）
- 项目 venv：`.venv`（Python 3.12，跑 ManimGL 与管线脚本）

## 常用命令

```bash
# 1) 改完 narration.py 后合成音频（换音色/参考音频必须 --force）
cd tts && "E:/soft/GPT-SoVITS-v2/runtime/python.exe" synth.py --force --speed 1.32 && cd ..

# 2) 重排时间轴
.venv/Scripts/python.exe plan.py

# 3) 全量高清渲染（单镜可 manimgl shots.py S17 -w --hd）
.venv/Scripts/python.exe render_video_only.py --hd

# 4) 音轨 → 成片 → 校验
.venv/Scripts/python.exe build_audio.py --check
.venv/Scripts/python.exe make_final.py
.venv/Scripts/python.exe check_sync.py
```

## 注意事项

- **HUD 镜号与底部进度条刻度烘在每一帧里**：任何时长 / 镜序变化都要全量重渲。
- 镜头类名必须零填充两位（`S07`），否则 manimgl 卡在交互菜单。
- Noto Sans SC 个别字形在特定字号下路径畸形（bbox 撑大 + 杂线），`common.py`
  统一以 48 号字生成再等比缩放规避，勿直接改回逐字号构造。
- TTS 按口播文本缓存：只改镜头画面不动文案时无需重合成。
