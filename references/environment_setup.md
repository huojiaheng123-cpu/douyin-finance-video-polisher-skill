# Environment Setup

Use this reference when `scripts/check_capabilities.py` reports missing or unconfirmed capabilities. The goal is to fix the production environment before making the video, because missing tools change the final quality and what can be verified.

## Setup Decision Tree

1. Run the doctor from the skill root:

```bash
python scripts/check_capabilities.py --require recommended
```

On Windows without Python, run:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check_capabilities.ps1 -Require recommended
```

2. If the gate fails, fix capabilities in this order:

| Priority | Capability | Why it matters | Minimum acceptable fallback |
| --- | --- | --- | --- |
| 1 | FFmpeg + ffprobe | Required for audio muxing, duration checks, stream checks, frame extraction, and motion review. | None for final delivery. Do not claim final MP4 quality without it. |
| 2 | Node.js + npm/npx | Required for HyperFrames CLI and most browser/render tooling. | Existing pre-rendered MP4 can be polished with FFmpeg only, but no HTML render can be produced. |
| 3 | HyperFrames CLI | Required to render/inspect HyperFrames compositions. | Use an existing renderer only if the project already provides one. |
| 4 | Browser/media preview | Required to watch motion, transitions, and audio-video sync. | Generate short review MP4 clips and motion strips with FFmpeg. |
| 5 | Transcription timestamps | Required for precise semantic timing against a voiceover. | Use a script transcript or rough timing, but flag sync as lower precision. |

3. Rerun the doctor after each fix. Continue production only after `recommended` or `full`, unless the user explicitly accepts degraded mode.

## Windows Fixes

Prefer existing bundled tools before asking the user to install globally.

Common FFmpeg locations:

```text
C:\Users\<user>\node_modules\ffmpeg-static\ffmpeg.exe
C:\Users\<user>\node_modules\@ffmpeg-installer\win32-x64\ffmpeg.exe
<workspace>\node_modules\ffmpeg-static\ffmpeg.exe
```

Common ffprobe locations:

```text
C:\Users\<user>\node_modules\@ffprobe-installer\win32-x64\ffprobe.exe
C:\Users\<user>\node_modules\ffprobe-static\bin\win32\x64\ffprobe.exe
<workspace>\node_modules\ffprobe-static\bin\win32\x64\ffprobe.exe
```

If these exist but commands are not on `PATH`, use the absolute path in FFmpeg commands or add the directory to the session `PATH`.

## User Guidance Template

When something is missing, respond with this shape:

```text
Current capability level: [minimal / recommended / full]
Missing: [tool]
Why it matters: [specific video-quality or verification consequence]
I can fix/check next by: [one command or one small setup step]
If we continue without it: [exact limitation]
```

Do not provide a long menu. Pick the next highest-impact fix.

## Degraded Mode Rules

Only continue below `recommended` when the user explicitly asks to proceed. Then:

- Do not claim dynamic sync was verified unless playback or motion strips were actually reviewed.
- Do not claim final MP4 correctness without FFmpeg/ffprobe stream checks.
- Save work in a clearly named draft directory, not the final product area.
- List the missing verification in the final answer.

## Quality Consistency Notes

- A machine with no FFmpeg may produce a visual draft, but audio muxing and stream verification will vary.
- A machine with no HyperFrames CLI may edit source files, but render output may differ on another machine.
- A machine with no browser/media preview may miss transition timing, overlap, or animation glitches.
- A machine with no word timestamps may place scene changes near the right sentence but not the right phrase.
