---
name: douyin-finance-video-polisher
description: Use when creating or polishing vertical Chinese finance/stock short videos from scripts, voiceovers, cloned voices, book covers, or HyperFrames projects for Douyin/TikTok style publishing.
---

# Douyin Finance Video Polisher

## Purpose

Turn finance narration into a polished 9:16 short video with semantic audio-video sync, Douyin-safe layout, richer visual density, dynamic motion review, and deterministic verification.

Use this together with `hyperframes`, `hyperframes-cli`, `ffmpeg`, `audio-transcribe`, and `ai-auto-video-editing` when available.

## Capability Bootstrap

Do not assume every Codex environment can see or play video. At the start of a video task, quickly check what is available:

- HyperFrames render/inspect commands.
- FFmpeg/ffprobe for muxing, metadata, frame extraction, and motion strips.
- Browser or media-preview capability for opening local HTML/MP4 and watching motion.
- Speech transcription or word timestamps for voiceover alignment.

If this skill includes `scripts/check_capabilities.py`, run it first with:

```bash
python scripts/check_capabilities.py
# If python is not on PATH, try:
py scripts/check_capabilities.py
python3 scripts/check_capabilities.py
```

Use its output as the capability report. If Python is unavailable, do the same checks manually.

If a capability is missing, use the best fallback and tell the user what level of verification was possible. For example, if direct playback is unavailable, create dynamic review artifacts with FFmpeg instead of relying on one static screenshot.

After the check, guide the user. Do not merely say a dependency is missing. Explain what is missing, what it unlocks, what quality problem remains without it, and the next install/setup action.

Use this short report shape when anything important is missing:

```text
Current capability level: [minimal / recommended / full]
Available:
- ...
Missing:
- FFmpeg: needed for muxing voiceover, extracting motion strips, checking duration/audio streams.
- HyperFrames CLI: needed for rendering and layout inspection of HTML video projects.
- Browser/media preview: needed for direct dynamic review of transitions and audio-video timing.
- Transcription/word timestamps: needed for precise semantic scene boundaries.
Impact:
- Without ..., I can still ..., but I cannot reliably verify ...
Suggested next step:
- Install/configure ... first because it gives the biggest quality gain.
```

Capability levels:

- **Minimal:** can write/edit a composition and inspect static files, but cannot render or dynamically verify. Must ask the user to install missing video tools before claiming quality.
- **Recommended:** has FFmpeg plus either HyperFrames render/inspect or another renderer. Can create final MP4 and motion-review artifacts.
- **Full:** has renderer, FFmpeg, transcription/word timestamps, and direct browser/media preview. Can do semantic sync plus true dynamic review.

Install guidance:

| Missing | Why it matters | Suggested fix |
| --- | --- | --- |
| FFmpeg | Required for muxing voiceover, extracting frames/motion strips, trimming review clips, and checking audio/video streams. | Install FFmpeg or use a bundled FFmpeg path if the environment provides one. |
| Node/npm or npx | Needed to run HyperFrames CLI. | Install Node.js LTS. |
| HyperFrames CLI | Needed to render HTML compositions and run layout inspection. | Use `npx hyperframes@latest ...` or install/configure the HyperFrames plugin/CLI. |
| Browser/media preview | Needed to actually watch motion, transitions, and sync. | Use the Codex Browser plugin, local browser preview, or generate short MP4 review clips for the user. |
| Transcription/word timestamps | Needed for precise semantic timing and cloned-voice sync. | Use an installed transcription skill/tool such as Whisper or ElevenLabs Scribe, or ask for a timed transcript. |

## Non-Negotiables

- Do not make a landing page or a static slide deck. Build the actual short-video experience.
- Do not add full subtitles unless the user asks. Leave room for platform captions.
- Do not use one sentence plus one image as the whole scene. Each main scene needs a headline plus 2-4 supporting visual elements: cards, chips, table rows, chart strokes, callouts, book/product card, or comparison panels.
- Keep a Douyin bottom safe zone. Avoid important text below roughly `y=1540` on a 1080x1920 canvas; keep final content above the player/caption area.
- Text must be large enough for mobile: hero `76-88px`, card text `28-38px`, tiny labels `22px+`.
- The video may speak during page transitions, but do not let the next semantic idea start while the previous page is still visually dominant.
- Never apply one fixed timing rule to every section. Sync to the actual narration meaning.
- Do not approve a video from one static frame. Motion, transition timing, and audio-video sync must be reviewed dynamically.

## Workflow

1. Inspect inputs:
   - Audio duration and waveform.
   - Transcript with timestamps when possible.
   - Script, book cover, reference video, existing HyperFrames project, and target output name.
   - Local capability level. If below recommended, explain missing parts and ask/guide before doing production work.

2. Segment by meaning:
   - Group narration into 5-8 scenes for a 45-70 second video.
   - Scene starts should follow major idea boundaries, not arbitrary equal cuts.
   - Add delayed beats inside each scene so supporting cards appear when that phrase is spoken.
   - Book/product pages should appear only when the narration actually introduces the book/product.
   - Before authoring visuals, build a scene plan using `references/production_patterns.md`.

3. Use this visual system by default:
   - Canvas: `1080x1920`, white/warm editorial background, faint grid.
   - Palette: ink `#11141b`, warm gold `#d7aa55`, signal green `#2c9675`, warning red `#f05a4f`.
   - Layout: `padding: 226px 92px 310px`, `headline max-width: 896px`.
   - Transitions: short light/gold-green wipe, not a large black slab.
   - Background ghost words are allowed but must stay faint and inside the canvas.
   - Use at least 3 different scene recipes across the video, such as hook contrast, false-opponent comparison, verification workflow, result table, market chart, and book CTA.

4. HyperFrames implementation checks:
   - Root must have `data-composition-id`, `data-duration`, `data-width="1080"`, `data-height="1920"`.
   - Audio element must have a stable `id`, e.g. `<audio id="voice" ...>`.
   - Build final layout in CSS first; animate with `gsap.from()` into that layout.
   - Use `data-delay` or per-scene timing offsets for semantic beats.
   - Animate support elements sequentially inside each scene. Headline, then evidence, then result/CTA; avoid all cards appearing at once.

5. Render and mux:
   - Render the visual with HyperFrames.
   - If HyperFrames audio is unreliable or silent, mux the original voiceover with FFmpeg:
     `ffmpeg -y -i visual.mp4 -i voice.wav -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 160k -shortest final.mp4`

6. Verify before delivering:
   - Run `hyperframes inspect <project> --samples 28`.
   - Review the video dynamically:
     - Best: open/play the final MP4 or HyperFrames preview and watch the full video, then scrub suspected spans.
     - Fallback: generate motion contact sheets at `2-4fps` for every scene or suspected span.
     - Fallback: generate short review clips/GIF/WebP previews for transitions and the final CTA.
   - Extract a full contact sheet only as a map of the whole video, not as the main quality check.
   - Extract extra motion contact sheets for suspected sync spans and the last 10-20 seconds.
   - Confirm: 9:16, audio present, no layout issues, no text in unsafe bottom zone, book cover fully visible, no giant black transition, and narration meaning matches the current page.
   - Score the video with the quality rubric in `references/production_patterns.md`. Fix anything below "good enough" before delivery.

## Production Patterns

For actual video creation, load `references/production_patterns.md`. It contains the scene recipes, finance visual vocabulary, motion rules, and scoring rubric that turn a basic text-on-slide video into a richer short-video composition.

## Dynamic Review Commands

Use direct playback when available. When it is not available, create motion evidence:

```bash
# Whole-video map, useful but not enough by itself.
ffmpeg -y -i final.mp4 -vf "fps=1/8,scale=270:480,tile=3x3" contact.jpg

# Motion strip for a suspected sync span.
ffmpeg -y -ss 35.5 -t 12 -i final.mp4 -vf "fps=3,scale=180:320,tile=6x6" motion_35_47.jpg

# Short preview clip for real playback in the user's media viewer.
ffmpeg -y -ss 35.5 -t 12 -i final.mp4 -c copy review_35_47.mp4
```

Use motion strips to catch problems a single static frame hides:

- A page turn that pauses half a syllable and restarts speech awkwardly.
- The next sentence starting while the previous page is still on screen.
- A book card entering before the narration introduces the book.
- Text that looks fine in one frame but overlaps during entrance animation.
- Black/large transition shapes covering too much of the frame.

## Timing Heuristics

- Let page changes land near clause boundaries.
- It is okay for narration to begin slightly before a page finishes animating if the page's core meaning is already visible.
- Avoid a hard pause before every page. It feels robotic on short-video platforms.
- Prefer overlapping speech with the end of a transition only when the new page's main headline is already visible.
- If a scene has two semantic ideas, split the scene or delay the second visual cluster.
- When the user reports "the next sentence is being said on the previous page", move the scene boundary earlier or delay the next narration visual cluster; do not globally slow every scene.

## Output Defaults

- Output names should be Chinese and descriptive, e.g. `AI炒股_精修增强版.mp4`.
- Provide final files as absolute local Markdown links.
- Summarize only the important changes: typography, safe zone, content richness, sync fixes, verification.
- State whether the final review used direct playback, motion strips, or static-only fallback.

## Common Fixes

- **Too much bottom blank:** increase usable vertical area while preserving the bottom safe zone; move ghost words lower, not core text.
- **Text too small:** raise headline/card/table sizes before adding more decorative elements.
- **Book cover outside frame:** use a bounded book card, keep cover around `335-410px`, and verify by frame extraction.
- **Hard cuts feel awkward:** use a short light wipe or content fade, but keep it subtle.
- **Final page appears too early:** delay the book/product card until the narration reaches the recommendation or CTA.
- **Agent cannot see video playback:** generate motion strips and short review clips; never pretend a static contact sheet proves timing.
- **User's machine lacks required tooling:** give a capability report, name the missing tool, explain its purpose in this workflow, and recommend the smallest useful install path before continuing.
