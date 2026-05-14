---
name: douyin-finance-video-polisher
description: Use when creating or polishing vertical Chinese finance/stock information-animation videos from voiceovers, scripts, PDFs, book covers, reference videos, or HyperFrames projects for Douyin/TikTok style publishing.
---

# Douyin Finance Video Polisher

## Purpose

Turn finance narration into a polished 9:16 short video with semantic audio-video sync, Douyin-safe layout, richer visual density, dynamic motion review, and deterministic verification.

Use this together with `hyperframes`, `hyperframes-cli`, `ffmpeg`, `audio-transcribe`, and `ai-auto-video-editing` when available.

## First-Run Environment Gate

Always run the environment check before planning scenes, writing HyperFrames code, rendering, or promising video quality. A missing renderer, FFmpeg, or preview path changes the output quality and verification standard, so do not skip this gate.

From the skill root, run:

```bash
python scripts/check_capabilities.py --require recommended
# If python is not on PATH, try:
py scripts/check_capabilities.py --require recommended
python3 scripts/check_capabilities.py --require recommended
# On Windows without Python, use:
powershell -ExecutionPolicy Bypass -File scripts/check_capabilities.ps1 -Require recommended
```

Rules:

- If the check reaches `recommended` or `full`, continue production.
- If the check is below `recommended`, pause production work and guide setup first. Read `references/environment_setup.md`, name the missing capability, explain the quality impact, and give the smallest useful fix.
- Only continue in degraded mode when the user explicitly asks to proceed without fixing the environment. In that case, state which verification claims cannot be made.
- Use `--network` only after the user allows dependency/network checks. The default doctor is local-only and must not download packages.
- Use `--json` when you need machine-readable results for an automation or wrapper script.

Do not merely say a dependency is missing. Explain what is missing, what it unlocks, what quality problem remains without it, and the next install/setup action.

Environment gotchas:

- On Windows, `python` may be missing even when `py` exists; use the PowerShell doctor if Python cannot start.
- In sandboxed Codex sessions, the process home may differ from the user's real home. The doctor checks both `Path.home()` and the current workspace's `C:\Users\<name>` owner directory so bundled FFmpeg tools are not missed.
- FFmpeg/ffprobe can be available as bundled Node packages without being on `PATH`; prefer detected absolute paths over telling the user to reinstall.

## House-Style Memory Gate

If the user asks for a voiceover-based finance information animation, the previous satisfactory style, VA/CDVA videos, endorsement/book-cover lead videos, ranking/blackhorse videos, or "make it like the reference", read `references/house_style_memory.md` before planning. Inspect `assets/style-references/reference-manifest.json`, then inspect the closest bundled standard videos or at least their motion sheets under `assets/style-references/`. The 7 bundled standards are the quality target, not optional examples. Do not rely on memory alone.

When screen text, VA/CDVA terminology, 带鱼/短鱼, author names, or ASR corrections matter, read `references/text_and_terms.md`. ASR is timing evidence only; final on-screen copy must come from the user's script, PDF, or approved draft.

If the video ends with a book, course, tool, QR, private-domain prompt, or other lead-generation element, read the "Ending Hook And Book Cover" section in `references/production_patterns.md`. Treat the book cover as a trust/continuation asset, not decoration.

Before delivering any final MP4, read `references/final_review.md` and perform the required layout review. The review must include frame-by-frame or high-frequency frame inspection for layout, text, transitions, safe zones, and book/lead endings.

## Template-First Production

For videos that should match the owner's house style, start from the bundled template instead of building a composition from scratch:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/init_finance_template.ps1 -OutDir <project-dir>
# Or start from one of the two registered video templates:
powershell -ExecutionPolicy Bypass -File scripts/init_finance_template.ps1 -OutDir <project-dir> -Template tanlun-ma-false-signal-final
powershell -ExecutionPolicy Bypass -File scripts/init_finance_template.ps1 -OutDir <project-dir> -Template reference-1-short-finance
```

Read `assets/templates/templates.manifest.json` before choosing a template. The registered video templates are:

- `tanlun-ma-false-signal-final`: long 1080x1920 finance explainer with multi-page argument.
- `reference-1-short-finance`: short 720x1280 finance explainer with compact indicator-validation and book CTA structure.

Cover rule: both registered video templates require a cover. Always create `cover.png`, then prepend it as a 0.6s first frame in the final MP4. Do not use "needs cover" as a template-selection criterion.

Use `assets/templates/finance-narration-standard/` as the editable scaffold:

- `DESIGN.md`: exact visual identity, typography, safe zones, and motion rules.
- `template.config.json`: canvas, palette, layout, and verification expectations.
- `video-spec.template.json`: six-scene finance narration structure.
- `cover-spec.template.json`: cover layout inputs.
- `index.html`: HyperFrames composition template.
- `reference-cover.png`: visual reference for the expected cover style.
- `environment.lock.json`: production environment expectations.

When initializing from a registered template, the script also creates `template-reference/` containing `template-reference.mp4`, `contact-sheet.jpg`, and `template.profile.json`. Use those as the visual matching target.

After copying the template, replace only the task-specific inputs first: voiceover, book/product cover, transcript timings, titles, and beats. Keep `DESIGN.md` and `template.config.json` unchanged unless the user intentionally changes the style.

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
- **Full:** has renderer, FFmpeg, and direct browser/media preview. Can render and dynamically review. Transcription/word timestamps are an extra precision layer for semantic sync.

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
- Do not use production labels as screen text: `书名登场`, `背书推荐`, `行动指令`, `第一篇`, `信息动画素材`, `同步预览`, `静音版`, `素材区`, `成品区`, or similar internal labels.
- Do not use ASR text as final screen text. Use ASR only for timing; correct screen copy against the user's draft, PDF, or `references/text_and_terms.md`.
- If the ending has lead generation, reserve a real final beat for it: problem recap, trust proof/book cover, and a light viewer-facing action. Do not just flash the book cover in the last second.
- Keep a Douyin bottom safe zone. Avoid important text below roughly `y=1540` on a 1080x1920 canvas; keep final content above the player/caption area.
- Text must be large enough for mobile: hero `76-88px`, card text `28-38px`, tiny labels `22px+`.
- The video may speak during page transitions, but do not let the next semantic idea start while the previous page is still visually dominant.
- Never apply one fixed timing rule to every section. Sync to the actual narration meaning.
- Do not approve a video from one static frame. Motion, transition timing, and audio-video sync must be reviewed dynamically.

## Workflow

1. Inspect inputs:
   - Run the first-run environment gate and resolve missing core tooling before production.
   - Run the house-style memory gate for voiceover-driven finance information animation.
   - If matching the owner's style matters, initialize from `assets/templates/finance-narration-standard/` before writing new composition code.
   - Audio duration and waveform.
   - Transcript with timestamps when possible.
   - Script/PDF/approved draft for final screen text.
   - Book cover/lead asset if the ending has hook, trust proof, or traffic guidance. Store it as `assets/book-cover.png` in template projects.
   - Reference video, existing HyperFrames project, and target output name.
   - Local capability level. If below recommended, do setup guidance first unless the user explicitly accepts degraded output.

2. Segment by meaning:
   - Group narration into 5-8 scenes for a 45-70 second video.
   - Scene starts should follow major idea boundaries, not arbitrary equal cuts.
   - Add delayed beats inside each scene so supporting cards appear when that phrase is spoken.
   - Book/product pages should appear only when the narration actually introduces the book/product.
   - For lead-generation endings, reserve the final 6-12 seconds for: "why this matters now" hook, book/tool proof, 2-3 useful tags, and a soft action phrase if the narration contains one.
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
   - Generate `cover.png` for the selected template, then prepend it to the final MP4 with `scripts/prepend_cover.ps1` when the output is intended for Douyin publishing.

6. Verify before delivering:
   - Read `references/final_review.md` and create review artifacts outside the final-output folder.
   - Run `hyperframes inspect <project> --samples 28`.
   - Review the video dynamically:
     - Best: open/play the final MP4 or HyperFrames preview and watch the full video, then scrub suspected spans.
     - Fallback: generate motion contact sheets at `2-4fps` for every scene or suspected span.
     - Fallback: generate short review clips/GIF/WebP previews for transitions and the final CTA.
   - Do a frame-by-frame or high-frequency frame pass:
     - Under 90 seconds: export every frame or at least every 2nd frame.
     - Longer videos: export every frame around transitions and every 4th-6th frame elsewhere.
     - Always export every frame for the final 10-15 seconds when it contains a book cover, ranking, QR, or traffic guidance.
   - Extract a full contact sheet only as a map of the whole video, not as the main quality check.
   - Extract extra motion contact sheets for suspected sync spans and the last 10-20 seconds.
   - Search source files and scene plans for banned production labels before final render.
   - Confirm: 9:16, audio present, first frame is the designed cover, no layout issues, no text in unsafe bottom zone, book cover fully visible, ending hook/lead beat is not rushed, no giant black transition, and narration meaning matches the current page.
   - Score the video with the quality rubric in `references/production_patterns.md`. Fix anything below "good enough" before delivery.

## Production Patterns

For actual video creation, load `references/production_patterns.md`. It contains the scene recipes, finance visual vocabulary, motion rules, and scoring rubric that turn a basic text-on-slide video into a richer short-video composition.

For house style and reference-asset matching, load `references/house_style_memory.md`.

For VA/CDVA terminology, banned screen labels, and ASR correction rules, load `references/text_and_terms.md`.

For delivery QA, layout inspection, frame-by-frame checking, and final review commands, load `references/final_review.md`.

## Environment Setup Reference

When the doctor reports missing or unconfirmed capabilities, load `references/environment_setup.md`. It contains the setup decision tree, common Windows paths, and the quality impact of each missing dependency. Use it before asking broad setup questions.

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
- **Weak ending/lead:** add a final hook line, book/tool proof, 2-3 concrete benefit tags, and a soft action phrase tied to the narration; keep it viewer-facing.
- **Hard cuts feel awkward:** use a short light wipe or content fade, but keep it subtle.
- **Final page appears too early:** delay the book/product card until the narration reaches the recommendation or CTA.
- **Agent cannot see video playback:** generate motion strips and short review clips; never pretend a static contact sheet proves timing.
- **User's machine lacks required tooling:** give a capability report, name the missing tool, explain its purpose in this workflow, and recommend the smallest useful install path before continuing.
