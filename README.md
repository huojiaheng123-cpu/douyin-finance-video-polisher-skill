# Douyin Finance Video Polisher Skill

This is a Codex skill for making and polishing vertical Chinese finance/stock short videos, especially Douyin/TikTok-style videos built from voiceovers, scripts, book covers, or HyperFrames projects.

## What It Does

- Turns finance narration into a 9:16 short-video plan.
- Splits voiceover by meaning instead of cutting scenes evenly.
- Designs richer finance visuals: charts, comparison cards, rule lists, backtest tables, metrics, and book/product CTA pages.
- Keeps layouts inside mobile/Douyin safe areas.
- Checks whether the machine can render, mux audio, extract motion review frames, and preview video.
- Verifies motion and audio-video sync instead of relying on one static screenshot.

## Main Use Cases

- Make a short video from a cloned voiceover.
- Polish an existing HyperFrames finance video.
- Fix problems like small text, empty bottom space, hard cuts, early book pages, or audio-video mismatch.
- Help a teammate diagnose missing local video tooling before production work.

## Files

- `SKILL.md`: Core skill instructions.
- `references/production_patterns.md`: Scene recipes, visual vocabulary, motion rules, and quality rubric.
- `scripts/check_capabilities.py`: Local capability checker for FFmpeg, Node/npm/npx, HyperFrames, browser preview, and transcription support.
- `agents/openai.yaml`: UI metadata for Codex skill display.

## Quick Start

Install or copy this folder into your Codex skills directory, then invoke it with a prompt like:

```text
Use $douyin-finance-video-polisher to make this finance voiceover into a polished 9:16 Douyin-style video.
```

Before creating video, run the capability check:

```bash
python scripts/check_capabilities.py
```

If Python is not on PATH, try:

```bash
py scripts/check_capabilities.py
python3 scripts/check_capabilities.py
```

By default, the checker is local-only and does not download packages. To allow an online `npx hyperframes@latest` check:

```bash
python scripts/check_capabilities.py --network
```

## Capability Levels

- `minimal`: Can inspect/edit files, but cannot reliably render or dynamically verify video.
- `recommended`: Can produce final videos and motion-review artifacts.
- `full`: Can render, mux, and directly review motion/audio-video sync.

## Recommended Tooling

- FFmpeg / ffprobe
- Node.js with npm/npx
- HyperFrames CLI or HyperFrames plugin
- Browser or media preview access
- Optional transcription with word timestamps for tighter semantic sync

## Quality Standard

The skill aims for videos that are readable on mobile, visually rich, semantically synced to narration, and dynamically reviewed before delivery.
