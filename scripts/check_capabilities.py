#!/usr/bin/env python3
"""Report local capabilities for the Douyin finance video workflow."""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import subprocess


def find_command(names: list[str]) -> str | None:
    for name in names:
        found = shutil.which(name)
        if found:
            return found
    return None


def existing_path(candidates: list[Path]) -> str | None:
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)
    return None


def find_ffmpeg_tool(tool: str) -> str | None:
    path_name = f"{tool}.exe" if not tool.endswith(".exe") else tool
    home = Path.home()
    candidates = [
        home / "node_modules" / "@ffmpeg-installer" / "win32-x64" / path_name,
        home / "node_modules" / "@ffmpeg-installer" / "ffmpeg" / path_name,
        Path.cwd() / "node_modules" / "@ffmpeg-installer" / "win32-x64" / path_name,
    ]
    return find_command([tool, path_name]) or existing_path(candidates)


def find_hyperframes_cli() -> str | None:
    return find_command([
        "hyperframes",
        "hyperframes.cmd",
        str(Path.cwd() / "node_modules" / ".bin" / "hyperframes.cmd"),
        str(Path.cwd() / "node_modules" / ".bin" / "hyperframes"),
    ])


def find_browser() -> str | None:
    command_found = find_command(["chrome", "msedge", "google-chrome", "chromium", "firefox"])
    if command_found:
        return command_found

    home = Path.home()
    candidates = [
        Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
        Path("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"),
        Path("C:/Program Files/Microsoft/Edge/Application/msedge.exe"),
        Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"),
        home / "AppData" / "Local" / "Google" / "Chrome" / "Application" / "chrome.exe",
        home / "AppData" / "Local" / "Microsoft" / "Edge" / "Application" / "msedge.exe",
    ]
    return existing_path(candidates)


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
    parser = argparse.ArgumentParser(description="Check local capabilities for the Douyin finance video workflow.")
    parser.add_argument(
        "--network",
        action="store_true",
        help="Allow npx to resolve hyperframes@latest. Default is local-only and will not download packages.",
    )
    args = parser.parse_args()

    checks = []
    unconfirmed = []

    ffmpeg_cmd = find_ffmpeg_tool("ffmpeg")
    ffmpeg_ok, ffmpeg_msg = try_command([ffmpeg_cmd, "-version"]) if ffmpeg_cmd else (False, "not found")
    checks.append(("FFmpeg", ffmpeg_ok, "mux audio, extract motion strips, check media streams", ffmpeg_msg))

    ffprobe_cmd = find_ffmpeg_tool("ffprobe")
    ffprobe_ok, ffprobe_msg = try_command([ffprobe_cmd, "-version"]) if ffprobe_cmd else (False, "not found")
    checks.append(("ffprobe", ffprobe_ok, "inspect duration and audio/video streams", ffprobe_msg))

    node_cmd = find_command(["node", "node.exe"])
    node_ok, node_msg = try_command([node_cmd, "--version"]) if node_cmd else (False, "not found")
    checks.append(("Node.js", node_ok, "run HyperFrames and browser tooling", node_msg))

    npm_cmd = find_command(["npm", "npm.cmd"])
    npm_ok, npm_msg = try_command([npm_cmd, "--version"]) if npm_cmd else (False, "not found")
    checks.append(("npm", npm_ok, "install or execute HyperFrames CLI", npm_msg))

    npx_cmd = find_command(["npx", "npx.cmd"])
    npx_ok, npx_msg = try_command([npx_cmd, "--version"]) if npx_cmd else (False, "not found")
    checks.append(("npx", npx_ok, "run HyperFrames without global install", npx_msg))

    hyperframes_cmd = find_hyperframes_cli()
    hyperframes_ok, hyperframes_msg = (
        try_command([hyperframes_cmd, "--version"]) if hyperframes_cmd else (False, "local command not found")
    )
    if not hyperframes_ok and args.network and npx_ok:
        hyperframes_ok, hyperframes_msg = try_command([npx_cmd, "--yes", "hyperframes@latest", "--version"], timeout=45)
    elif not hyperframes_ok and npx_ok:
        hyperframes_msg = "local command not found; rerun with --network to test npx hyperframes@latest"
    checks.append(("HyperFrames CLI", hyperframes_ok, "render HTML video and inspect layouts", hyperframes_msg))

    browser_found = find_browser()
    checks.append(("Browser/media preview", bool(browser_found), "watch motion and audio-video sync", browser_found or "not found"))

    transcription_hint = "manual check: Whisper/ElevenLabs/audio-transcribe skill may be environment-specific"
    unconfirmed.append(("Transcription timestamps", "precise semantic scene boundaries", transcription_hint))

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
    for name, purpose, hint in unconfirmed:
        print(f"- {name}: needed for {purpose}. {hint}.")
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
