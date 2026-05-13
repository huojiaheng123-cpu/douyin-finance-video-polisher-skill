# 抖音财经短视频精修 Skill

这是一个给 Codex 使用的本地 skill，用来制作和精修竖屏财经/股票类短视频，尤其适合抖音、TikTok、小红书这类 9:16 短视频。

它适合处理：配音、克隆音频、文案、书籍封面、HyperFrames 项目，以及已经生成但需要继续优化的视频。

## 主要功能

- 根据配音语义拆分视频段落，不是平均切页。
- 自动规划 9:16 财经短视频结构。
- 设计更丰富的画面：图表、对比卡片、规则清单、回测表格、指标数据、书籍/产品推荐页。
- 控制抖音安全区，避免字幕区、按钮区遮挡核心内容。
- 检测本机是否具备视频制作能力：渲染、合成音频、抽动态帧、视频预览等。
- 强制做动态复审，不只看一张静态截图。
- 用质量评分表检查：音画同步、信息密度、手机可读性、金融相关性、CTA 时机。

## 适用场景

- 给一段财经配音自动做竖屏视频。
- 把克隆音频做得更像完整短视频成片。
- 精修 HyperFrames 生成的视频。
- 修复常见问题：
  - 字太小
  - 底部空白太多
  - 画面太单调
  - 硬切不自然
  - 书籍页出现太早
  - 配音和画面不同步
- 帮同事检查电脑缺少哪些视频制作工具。

## 文件说明

- `SKILL.md`：核心 skill 说明，Codex 会读取这里的工作流程。
- `references/production_patterns.md`：做片方法，包括场景配方、金融视觉元素、动效规则、质量评分表。
- `scripts/check_capabilities.py`：本机能力检测脚本，用来检查 FFmpeg、Node、HyperFrames、浏览器预览等能力。
- `agents/openai.yaml`：Codex skill 的界面信息。

## 快速使用

把这个文件夹安装或复制到 Codex 的 skills 目录后，可以这样调用：

```text
用 douyin-finance-video-polisher 帮我把这段财经配音做成 9:16 抖音风格短视频。
```

或者：

```text
Use $douyin-finance-video-polisher to make this finance voiceover into a polished 9:16 Douyin-style video.
```

## 先检测电脑能力

制作视频前，建议先运行：

```bash
python scripts/check_capabilities.py
```

如果电脑里 `python` 命令不可用，可以试：

```bash
py scripts/check_capabilities.py
python3 scripts/check_capabilities.py
```

默认检测不会联网，也不会下载依赖。  
如果允许检测在线 HyperFrames，可以运行：

```bash
python scripts/check_capabilities.py --network
```

## 能力等级说明

- `minimal`：只能看文件、改文件，不能可靠渲染或动态复审视频。
- `recommended`：可以生成视频，并能抽动态帧做复审。
- `full`：可以渲染、合成音频、动态预览视频，并检查音画同步。

## 推荐工具

为了获得更好的效果，建议安装或配置：

- FFmpeg / ffprobe
- Node.js、npm、npx
- HyperFrames CLI 或 HyperFrames 插件
- 浏览器或本地视频预览能力
- 可选：带时间戳的语音转写工具，用于更精准的音画同步

## 质量目标

这个 skill 的目标不是简单生成“PPT 式视频”，而是做出：

- 手机上清晰可读
- 画面信息更丰富
- 财经内容表达准确
- 配音和画面语义同步
- 书籍/产品推荐出现时机自然
- 经过动态复审的竖屏短视频

