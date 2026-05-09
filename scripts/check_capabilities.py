#!/usr/bin/env python3
"""Report local capabilities for the Douyin finance video workflow."""

from __future__ import annotations

import shutil
import subprocess


def has_command(name: str) -> bool:
    return shutil.which(name) is not None


def try_command(args: list[str], timeout: int = 10) -> tuple[bool, str]:
    try:
        proc = subprocess.run(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=timeout,
            check=False,
        )
    except Exception as exc:
        return False, str(exc)
    output = (proc.stdout or "").strip().splitlines()
    first_line = output[0] if output else ""
    return proc.returncode == 0, first_line


def main() -> int:
    checks = []

    ffmpeg_ok, ffmpeg_msg = try_command(["ffmpeg", "-version"]) if has_command("ffmpeg") else (False, "not found")
    checks.append(("FFmpeg", ffmpeg_ok, "mux audio, extract motion strips, check media streams", ffmpeg_msg))

    ffprobe_ok, ffprobe_msg = try_command(["ffprobe", "-version"]) if has_command("ffprobe") else (False, "not found")
    checks.append(("ffprobe", ffprobe_ok, "inspect duration and audio/video streams", ffprobe_msg))

    node_ok, node_msg = try_command(["node", "--version"]) if has_command("node") else (False, "not found")
    checks.append(("Node.js", node_ok, "run HyperFrames and browser tooling", node_msg))

    npm_ok, npm_msg = try_command(["npm", "--version"]) if has_command("npm") else (False, "not found")
    checks.append(("npm", npm_ok, "install or execute HyperFrames CLI", npm_msg))

    npx_ok, npx_msg = try_command(["npx", "--version"]) if has_command("npx") else (False, "not found")
    checks.append(("npx", npx_ok, "run HyperFrames without global install", npx_msg))

    hyperframes_ok = False
    hyperframes_msg = "not checked"
    if npx_ok:
        hyperframes_ok, hyperframes_msg = try_command(["npx", "--yes", "hyperframes@latest", "--version"], timeout=45)
    checks.append(("HyperFrames CLI", hyperframes_ok, "render HTML video and inspect layouts", hyperframes_msg))

    browser_candidates = ["chrome", "msedge", "google-chrome", "chromium", "firefox"]
    browser_found = next((name for name in browser_candidates if has_command(name)), None)
    checks.append(("Browser/media preview", bool(browser_found), "watch motion and audio-video sync", browser_found or "not found"))

    transcription_hint = "manual check: Whisper/ElevenLabs/audio-transcribe skill may be environment-specific"
    checks.append(("Transcription timestamps", False, "precise semantic scene boundaries", transcription_hint))

    available = [name for name, ok, _, _ in checks if ok]
    missing = [(name, purpose) for name, ok, purpose, _ in checks if not ok]

    has_renderer = hyperframes_ok
    has_motion_review = ffmpeg_ok
    has_preview = bool(browser_found)
    if has_renderer and has_motion_review and has_preview:
        level = "full"
    elif has_motion_review and (has_renderer or node_ok):
        level = "recommended"
    else:
        level = "minimal"

    print(f"Current capability level: {level}")
    print("Available:")
    for name in available:
        print(f"- {name}")
    print("Missing or unconfirmed:")
    for name, purpose in missing:
        print(f"- {name}: needed for {purpose}.")
    print("Impact:")
    if level == "full":
        print("- This machine can render, mux, and dynamically review video.")
    elif level == "recommended":
        print("- This machine can produce video and motion-review artifacts, but may still need direct playback or transcription for best sync review.")
    else:
        print("- This machine cannot reliably render or dynamically verify final video yet.")
    print("Suggested next step:")
    if not ffmpeg_ok:
        print("- Install/configure FFmpeg first; it gives the biggest quality gain for muxing and motion review.")
    elif not hyperframes_ok:
        print("- Configure HyperFrames CLI next so HTML compositions can be rendered and inspected.")
    elif not has_preview:
        print("- Add a browser/media preview path or generate short MP4 review clips for the user.")
    else:
        print("- Add transcription/word timestamps if precise semantic sync is needed.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
