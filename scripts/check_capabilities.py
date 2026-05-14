#!/usr/bin/env python3
"""Report local capabilities for the Douyin finance video workflow."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys


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


def home_candidates() -> list[Path]:
    homes = [Path.home()]
    cwd_parts = Path.cwd().parts
    if len(cwd_parts) >= 3 and cwd_parts[1].lower() == "users":
        workspace_home = Path(cwd_parts[0], cwd_parts[1], cwd_parts[2])
        if workspace_home not in homes:
            homes.append(workspace_home)
    return homes


def find_ffmpeg_tool(tool: str) -> str | None:
    path_name = f"{tool}.exe" if not tool.endswith(".exe") else tool
    cwd = Path.cwd()
    candidates = [
        cwd / "node_modules" / "@ffmpeg-installer" / "win32-x64" / path_name,
        cwd / "node_modules" / "@ffmpeg-installer" / "ffmpeg" / path_name,
        cwd / "node_modules" / "ffmpeg-static" / path_name,
    ]
    for home in home_candidates():
        candidates.extend(
            [
                home / "node_modules" / "@ffmpeg-installer" / "win32-x64" / path_name,
                home / "node_modules" / "@ffmpeg-installer" / "ffmpeg" / path_name,
                home / "node_modules" / "ffmpeg-static" / path_name,
            ]
        )
    if tool.replace(".exe", "").lower() == "ffprobe":
        candidates.extend(
            [
                cwd / "node_modules" / "@ffprobe-installer" / "win32-x64" / path_name,
                cwd / "node_modules" / "ffprobe-static" / "bin" / "win32" / "x64" / path_name,
                cwd / "node_modules" / "ffprobe-static" / "bin" / "win32" / "ia32" / path_name,
            ]
        )
        for home in home_candidates():
            candidates.extend(
                [
                    home / "node_modules" / "@ffprobe-installer" / "win32-x64" / path_name,
                    home / "node_modules" / "ffprobe-static" / "bin" / "win32" / "x64" / path_name,
                    home / "node_modules" / "ffprobe-static" / "bin" / "win32" / "ia32" / path_name,
                ]
            )
    return find_command([tool, path_name]) or existing_path(candidates)


def install_hint(name: str) -> str:
    hints = {
        "FFmpeg": "Install FFmpeg or add a bundled ffmpeg-static path to PATH.",
        "ffprobe": "Install ffprobe with FFmpeg or add @ffprobe-installer/ffprobe-static to PATH.",
        "Node.js": "Install Node.js LTS so HyperFrames and browser tooling can run.",
        "npm": "Install Node.js LTS; npm is normally bundled with it.",
        "npx": "Install Node.js LTS; npx is normally bundled with npm.",
        "HyperFrames CLI": "Install/configure HyperFrames CLI or rerun this check with --network to test npx hyperframes@latest.",
        "Browser/media preview": "Install Chrome/Edge or use a Codex/browser preview tool; otherwise generate review clips.",
    }
    return hints.get(name, "Install or configure this capability before production.")


def rank(level: str) -> int:
    return {"minimal": 0, "recommended": 1, "full": 2}[level]


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
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable JSON instead of the human setup report.",
    )
    parser.add_argument(
        "--require",
        choices=["minimal", "recommended", "full"],
        default=None,
        help="Exit with code 2 when the machine is below this capability level.",
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
    missing = [(name, purpose, install_hint(name)) for name, ok, purpose, _ in checks if not ok]

    has_renderer = hyperframes_ok
    has_motion_review = ffmpeg_ok
    has_preview = bool(browser_found)
    if has_renderer and has_motion_review and ffprobe_ok and has_preview:
        level = "full"
    elif has_motion_review and ffprobe_ok and has_renderer:
        level = "recommended"
    else:
        level = "minimal"

    if not ffmpeg_ok:
        next_step = "Install/configure FFmpeg first; it gives the biggest quality gain for muxing and motion review."
    elif not ffprobe_ok:
        next_step = "Install/configure ffprobe so durations and audio/video streams can be verified."
    elif not hyperframes_ok:
        next_step = "Configure HyperFrames CLI next so HTML compositions can be rendered and inspected."
    elif not has_preview:
        next_step = "Add a browser/media preview path or generate short MP4 review clips for the user."
    else:
        next_step = "Add transcription/word timestamps if precise semantic sync is needed."

    if level == "full":
        impact = "This machine can render, mux, and dynamically review video."
    elif level == "recommended":
        impact = "This machine can produce video and motion-review artifacts, but may still need direct playback or transcription for best sync review."
    else:
        impact = "This machine cannot reliably render or dynamically verify final video yet."

    result = {
        "capabilityLevel": level,
        "meetsRequiredLevel": args.require is None or rank(level) >= rank(args.require),
        "requiredLevel": args.require,
        "checks": [
            {
                "name": name,
                "ok": ok,
                "purpose": purpose,
                "detail": detail,
                "fix": install_hint(name) if not ok else None,
            }
            for name, ok, purpose, detail in checks
        ],
        "unconfirmed": [
            {"name": name, "purpose": purpose, "detail": hint}
            for name, purpose, hint in unconfirmed
        ],
        "impact": impact,
        "suggestedNextStep": next_step,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Current capability level: {level}")
        print("Available:")
        for name in available:
            print(f"- {name}")
        print("Missing or unconfirmed:")
        for name, purpose, fix in missing:
            print(f"- {name}: needed for {purpose}. Fix: {fix}")
        for name, purpose, hint in unconfirmed:
            print(f"- {name}: needed for {purpose}. {hint}.")
        print("Impact:")
        print(f"- {impact}")
        print("Suggested next step:")
        print(f"- {next_step}")
        if args.require and not result["meetsRequiredLevel"]:
            print(f"Gate: required level '{args.require}' was not met.")

    if args.require and not result["meetsRequiredLevel"]:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
