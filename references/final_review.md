# Final Review

Use this before delivering any final MP4. The goal is to catch layout and motion problems that a single screenshot hides.

## Required Review Artifacts

For every final video, create review artifacts outside the final-output folder:

- `ffprobe` report: width, height, duration, video stream, audio stream.
- First frame: proves the designed cover is prepended.
- Whole-video contact sheet: quick map of all pages.
- Motion sheets for the full video or every major span.
- Frame-by-frame or high-frequency frame folder for layout inspection.

The final-output folder should contain only the final MP4 unless the user explicitly asks otherwise.

## Frame-By-Frame Layout Inspection

Do a frame-level pass before claiming the video is ready.

Default rule:

- For videos under 90 seconds, export every frame or at least every 2nd frame.
- For longer videos, export every frame around transitions and every 4th-6th frame elsewhere.
- Always export every frame for the final 10-15 seconds if it contains a book cover, CTA, QR, ranking, or traffic guidance.

Inspect the exported frames for:

- Text cropped by the canvas or safe-zone boundary.
- Text overlapping with cards, charts, book covers, or bottom navigation.
- A headline or table row that is readable on one frame but overlaps during entrance animation.
- Book cover outside the frame, too small, too large, or visible for too short a time.
- Black or dark transition shapes covering too much of the frame.
- Banned production labels on screen.
- Empty pages or pages that look like static PPT.
- Ranking/table numbers jumping, occluding, or becoming unreadable.
- Bottom Douyin caption/player zone containing important text.

## Minimum Pass/Fail Standard

Do not deliver if any of these are true:

- Any important text is below the safe zone.
- Any screen has production labels such as `书名登场`, `背书推荐`, `工具书推荐`, `行动指令`, `CTA`, `静音版`, or `素材区`.
- Book/lead ending is rushed, off-frame, or appears before narration introduces it.
- A transition covers the key visual while the next sentence is already being spoken.
- The audio track is missing or duration is mismatched.

## Commands

Use direct playback when available, then create frame evidence.

```powershell
# Export every frame for a short final video.
powershell -ExecutionPolicy Bypass -File scripts/extract_review_frames.ps1 -Input final.mp4 -OutDir review\frames -Mode all

# Export every 2nd frame.
powershell -ExecutionPolicy Bypass -File scripts/extract_review_frames.ps1 -Input final.mp4 -OutDir review\frames -Mode every-n -Every 2

# Export a high-frequency span around a risky transition or final CTA.
powershell -ExecutionPolicy Bypass -File scripts/extract_review_frames.ps1 -Input final.mp4 -OutDir review\ending_frames -Start 50 -Duration 12 -Mode all
```

Useful FFmpeg fallbacks:

```bash
ffmpeg -y -i final.mp4 -vf "fps=1/8,scale=270:480,tile=3x3" review/contact.jpg
ffmpeg -y -i final.mp4 -vf "fps=4,scale=180:320,tile=6x6" review/motion_full.jpg
ffmpeg -y -ss 50 -t 12 -i final.mp4 -vf "fps=8,scale=180:320,tile=8x8" review/ending_motion.jpg
```

## Delivery Note

When delivering, state which review was used:

- Direct playback: yes/no.
- Frame-by-frame or high-frequency frame pass: all / every N / risky spans only.
- Checked: safe zone, text overlap, book cover, banned labels, audio stream, duration.
