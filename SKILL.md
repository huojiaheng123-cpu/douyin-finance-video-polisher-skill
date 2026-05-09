---
name: douyin-finance-video-polisher
description: Use when creating or polishing vertical Chinese finance/stock short videos from scripts, voiceovers, cloned voices, book covers, or HyperFrames projects for Douyin/TikTok style publishing.
---

# Douyin Finance Video Polisher

## Purpose

Turn finance narration into a polished 9:16 short video with semantic audio-video sync, Douyin-safe layout, richer visual density, and deterministic verification.

Use this together with `hyperframes`, `hyperframes-cli`, `ffmpeg`, `audio-transcribe`, and `ai-auto-video-editing` when available.

## Non-Negotiables

- Do not make a landing page or a static slide deck. Build the actual short-video experience.
- Do not add full subtitles unless the user asks. Leave room for platform captions.
- Do not use one sentence plus one image as the whole scene. Each main scene needs a headline plus 2-4 supporting visual elements: cards, chips, table rows, chart strokes, callouts, book/product card, or comparison panels.
- Keep a Douyin bottom safe zone. Avoid important text below roughly `y=1540` on a 1080x1920 canvas; keep final content above the player/caption area.
- Text must be large enough for mobile: hero `76-88px`, card text `28-38px`, tiny labels `22px+`.
- The video may speak during page transitions, but do not let the next semantic idea start while the previous page is still visually dominant.
- Never apply one fixed timing rule to every section. Sync to the actual narration meaning.

## Workflow

1. Inspect inputs:
   - Audio duration and waveform.
   - Transcript with timestamps when possible.
   - Script, book cover, reference video, existing HyperFrames project, and target output name.

2. Segment by meaning:
   - Group narration into 5-8 scenes for a 45-70 second video.
   - Scene starts should follow major idea boundaries, not arbitrary equal cuts.
   - Add delayed beats inside each scene so supporting cards appear when that phrase is spoken.
   - Book/product pages should appear only when the narration actually introduces the book/product.

3. Use this visual system by default:
   - Canvas: `1080x1920`, white/warm editorial background, faint grid.
   - Palette: ink `#11141b`, warm gold `#d7aa55`, signal green `#2c9675`, warning red `#f05a4f`.
   - Layout: `padding: 226px 92px 310px`, `headline max-width: 896px`.
   - Transitions: short light/gold-green wipe, not a large black slab.
   - Background ghost words are allowed but must stay faint and inside the canvas.

4. HyperFrames implementation checks:
   - Root must have `data-composition-id`, `data-duration`, `data-width="1080"`, `data-height="1920"`.
   - Audio element must have a stable `id`, e.g. `<audio id="voice" ...>`.
   - Build final layout in CSS first; animate with `gsap.from()` into that layout.
   - Use `data-delay` or per-scene timing offsets for semantic beats.

5. Render and mux:
   - Render the visual with HyperFrames.
   - If HyperFrames audio is unreliable or silent, mux the original voiceover with FFmpeg:
     `ffmpeg -y -i visual.mp4 -i voice.wav -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 160k -shortest final.mp4`

6. Verify before delivering:
   - Run `hyperframes inspect <project> --samples 28`.
   - Extract a full contact sheet.
   - Extract extra contact sheets for suspected sync spans and the last 10-20 seconds.
   - Confirm: 9:16, audio present, no layout issues, no text in unsafe bottom zone, book cover fully visible, no giant black transition, and narration meaning matches the current page.

## Timing Heuristics

- Let page changes land near clause boundaries.
- It is okay for narration to begin slightly before a page finishes animating if the page's core meaning is already visible.
- Avoid a hard pause before every page. It feels robotic on short-video platforms.
- If a scene has two semantic ideas, split the scene or delay the second visual cluster.
- When the user reports "the next sentence is being said on the previous page", move the scene boundary earlier or delay the next narration visual cluster; do not globally slow every scene.

## Output Defaults

- Output names should be Chinese and descriptive, e.g. `AI炒股_精修增强版.mp4`.
- Provide final files as absolute local Markdown links.
- Summarize only the important changes: typography, safe zone, content richness, sync fixes, verification.

## Common Fixes

- **Too much bottom blank:** increase usable vertical area while preserving the bottom safe zone; move ghost words lower, not core text.
- **Text too small:** raise headline/card/table sizes before adding more decorative elements.
- **Book cover outside frame:** use a bounded book card, keep cover around `335-410px`, and verify by frame extraction.
- **Hard cuts feel awkward:** use a short light wipe or content fade, but keep it subtle.
- **Final page appears too early:** delay the book/product card until the narration reaches the recommendation or CTA.
