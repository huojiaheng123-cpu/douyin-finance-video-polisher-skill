# 抖音财经信息动画视频 Skill

这是一个给 Codex 使用的本地 skill，用来根据配音、文案或 PDF 准稿制作和精修竖屏财经/股票类信息动画视频，尤其适合抖音、TikTok、小红书这类 9:16 短视频。

它适合处理：配音、克隆音频、文案、PDF 准稿、书籍封面、参考视频、HyperFrames 项目，以及已经生成但需要继续优化的视频。

## 主要功能

- 根据配音语义拆分视频段落，不是平均切页。
- 自动规划 9:16 财经短视频结构。
- 读取 7 条内置标准片、动态联系图、首帧和全片联系图，尽量复刻满意版本的审美和节奏。
- 强制用用户文案/PDF 校正文案，避免把 ASR 错字直接放到画面上。
- 专门处理书封结尾、钩子收束和轻引流，不把书封当普通装饰。
- 做好视频后按规范逐帧/高频抽帧复查排版、安全区、转场、书封和禁用词。
- 设计更丰富的画面：图表、对比卡片、规则清单、回测表格、指标数据、书籍/产品推荐页。
- 控制抖音安全区，避免字幕区、按钮区遮挡核心内容。
- 检测本机是否具备视频制作能力：渲染、合成音频、抽动态帧、视频预览等。
- 强制做动态复审，不只看一张静态截图。
- 用质量评分表检查：音画同步、信息密度、手机可读性、金融相关性、CTA 时机。

## 适用场景

- 给一段财经配音自动做竖屏视频。
- 按内置满意参考片的风格做“白底金融信息动画”。
- 把克隆音频做得更像完整短视频成片。
- 精修 HyperFrames 生成的视频。
- 做 VA/CDVA/带鱼系统/《概率的朋友》相关短视频时校正术语。
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
- `references/house_style_memory.md`：满意版本的审美、节奏、禁忌和参考资产索引。
- `references/text_and_terms.md`：屏幕文案、禁用制作词、VA/CDVA/带鱼系统术语校正规则。
- `references/final_review.md`：成片交付前的逐帧/高频抽帧复查规范。
- `references/environment_setup.md`：缺少 FFmpeg、HyperFrames、预览能力时的处理方式。
- `assets/style-references/`：7 条内置标准视频、动态联系图、全片联系图、首帧和标准清单。
- `assets/templates/`：可复制的 HyperFrames 风格模板、参考模板和默认书封占位图。
- `scripts/check_capabilities.py`：本机能力检测脚本，用来检查 FFmpeg、Node、HyperFrames、浏览器预览等能力。
- `scripts/extract_review_frames.ps1`：交付前抽取全帧或高频复查帧。
- `agents/openai.yaml`：Codex skill 的界面信息。

## 快速使用

这个仓库本身就是完整 skill。不要只下载 `SKILL.md`，必须保留 `references/`、`assets/`、`scripts/` 和 `agents/`，否则同事无法复刻同样的视频效果。

推荐安装方式：把 GitHub 仓库 clone 到 Codex skills 目录。

```powershell
cd $env:USERPROFILE\.codex\skills
git clone https://github.com/huojiaheng123-cpu/douyin-finance-video-polisher-skill.git douyin-finance-video-polisher
```

如果不用 git，也可以在 GitHub 页面点 `Code -> Download ZIP`，解压后把整个文件夹改名为 `douyin-finance-video-polisher`，放到：

```text
C:\Users\<你的用户名>\.codex\skills\douyin-finance-video-polisher
```

安装后，在 Codex 里可以这样调用：

```text
用 douyin-finance-video-polisher 按内置参考片风格，把这段财经配音做成 9:16 抖音信息动画视频。
```

或者：

```text
Use $douyin-finance-video-polisher to make this finance voiceover into a polished 9:16 Douyin-style information-animation video matching the bundled references.
```

## GitHub 发布要求

为了让同事从 GitHub 下载后达到同样效果，仓库必须包含这些文件，不要只发布压缩包：

- `SKILL.md`
- `agents/openai.yaml`
- `references/*.md`
- `scripts/*.py` 和 `scripts/*.ps1`
- `assets/templates/`
- `assets/style-references/` 里的 7 条标准视频、动态联系图、首帧、全片联系图和 `reference-manifest.json`

`dist/` 只是本地打包产物，不需要提交到 GitHub。

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

