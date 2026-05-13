# Douyin Finance Video Polisher Skill

根据配音制作/优化中文金融短视频的 Codex Skill。它会先检查本地视频生产环境，再按模板生成 9:16 金融新媒体风格视频，重点解决配音同步、封面首帧、版式一致性和动态复查。

## 核心能力

- 根据配音、脚本、书封或已有成片制作金融短视频。
- 使用环境门禁检查 FFmpeg、ffprobe、Node/npm/npx、HyperFrames CLI、浏览器预览能力。
- 缺环境时先引导补齐，避免不同电脑做出不一致的效果。
- 内置两个视频模板和一个可编辑 HyperFrames 工程脚手架。
- 两个视频模板都强制生成封面，并把封面作为最终 MP4 的 0.6 秒首帧。

## 使用流程

1. 先运行环境检查：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/check_capabilities.ps1 -Require recommended
```

2. 选择模板并初始化工程：

```powershell
# 模板1：长版，多页论证
powershell -ExecutionPolicy Bypass -File scripts/init_finance_template.ps1 -OutDir <project-dir> -Template tanlun-ma-false-signal-final

# 模板2：短版，指标验证/书籍 CTA
powershell -ExecutionPolicy Bypass -File scripts/init_finance_template.ps1 -OutDir <project-dir> -Template reference-1-short-finance
```

3. 替换工程里的配音、文案、书封、时间轴。

4. 生成 `cover.png`，渲染正片后拼接封面首帧：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/prepend_cover.ps1 -Cover cover.png -Video rendered.mp4 -Output final.mp4
```

5. 用 ffprobe、抽帧、motion strip 或直接播放复查最终成片。

## 模板

模板清单在 `assets/templates/templates.manifest.json`。

| 模板 | ID | 适合场景 |
| --- | --- | --- |
| 模板1：弹论1 均线假信号长版 | `tanlun-ma-false-signal-final` | 2-3 分钟金融口播长版、多页论证、完整讲清一个交易误区 |
| 模板2：指标验证短版 | `reference-1-short-finance` | 60 秒以内观点短视频、指标验证、书籍/工具 CTA |
| 标准工程脚手架 | `finance-narration-standard` | 新建可编辑 HyperFrames 工程 |

两个模板都必须有封面。模板选择只看内容结构和时长，不看是否需要封面。

## 环境要求

推荐环境至少包含：

- FFmpeg + ffprobe
- Node.js + npm/npx
- HyperFrames CLI
- Chrome/Edge 或可用浏览器预览能力

如果没有 Python，Windows 用户可以使用 PowerShell 版 doctor：`scripts/check_capabilities.ps1`。Python 可用时也可以运行 `scripts/check_capabilities.py`。

## Skill 结构

```text
SKILL.md
agents/openai.yaml
scripts/
  check_capabilities.py
  check_capabilities.ps1
  init_finance_template.ps1
  prepend_cover.ps1
references/
  environment_setup.md
  production_patterns.md
assets/templates/
  finance-narration-standard/
  tanlun-ma-false-signal-final/
  reference-1-short-finance/
  templates.manifest.json
```

## 安装

把本仓库放到 Codex skills 目录，例如：

```text
C:\Users\<user>\.codex\skills\douyin-finance-video-polisher
```

然后在 Codex 中调用 `douyin-finance-video-polisher`，或直接说“根据配音做金融短视频”。
