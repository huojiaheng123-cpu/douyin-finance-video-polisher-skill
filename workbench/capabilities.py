import os
import shutil
import subprocess
from pathlib import Path
from typing import Iterable

from workbench.models import CapabilityLevel, ToolStatus


REPO_ROOT = Path(__file__).resolve().parents[1]


def find_command(names: str | Iterable[str]) -> str | None:
    command_names = [names] if isinstance(names, str) else list(names)
    for name in command_names:
        found = shutil.which(name)
        if found:
            return found
    return None


def existing_path(candidates: Iterable[str | Path]) -> str | None:
    for candidate in candidates:
        path = Path(candidate).expanduser()
        if path.exists():
            return str(path)
    return None


def find_ffmpeg_tool(tool: str) -> str | None:
    env_name = f"{tool.upper()}_PATH"
    env_path = os.environ.get(env_name)
    if env_path and Path(env_path).expanduser().exists():
        return str(Path(env_path).expanduser())
    return find_command([tool, f"{tool}.exe"])


def find_hyperframes_cli() -> str | None:
    direct = find_command(["hyperframes", "hyperframes.cmd"])
    if direct:
        return direct

    local_bin = existing_path(
        [
            REPO_ROOT / "node_modules" / ".bin" / "hyperframes",
            REPO_ROOT / "node_modules" / ".bin" / "hyperframes.cmd",
        ]
    )
    return local_bin


def find_browser() -> str | None:
    env_browser = os.environ.get("BROWSER")
    if env_browser:
        browser_value = env_browser.strip()
        if browser_value and not any(char.isspace() for char in browser_value):
            browser_path = Path(browser_value).expanduser()
            if browser_path.is_absolute() or browser_path.parent != Path("."):
                if browser_path.exists():
                    return str(browser_path)
            else:
                found_browser = shutil.which(browser_value)
                if found_browser:
                    return found_browser

    browser_path = existing_path(
        [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            "/Applications/Google Chrome.app",
            "/Applications/Microsoft Edge.app",
        ]
    )
    if browser_path:
        return browser_path

    return find_command(
        [
            "chrome",
            "google-chrome",
            "chromium",
            "msedge",
            "firefox",
            "chromium-browser",
        ]
    )


def try_command(args: list[str], timeout: int = 10) -> tuple[bool, str]:
    try:
        completed = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except FileNotFoundError:
        return False, "command not found"
    except subprocess.TimeoutExpired:
        return False, f"timed out after {timeout}s"
    except OSError as exc:
        return False, str(exc)

    output = (completed.stdout or completed.stderr or "").strip()
    detail = output.splitlines()[0] if output else f"exit code {completed.returncode}"
    return completed.returncode == 0, detail


def _probe_version(command: str | None, version_args: list[str]) -> tuple[bool, str]:
    if not command:
        return False, "not found on PATH"

    available, detail = try_command([command, *version_args])
    if available:
        return True, detail
    return False, f"{command}: {detail}"


def _probe_hyperframes_cli() -> tuple[bool, str]:
    hyperframes = find_hyperframes_cli()
    if not hyperframes:
        return False, "local command not found"

    available, detail = try_command([hyperframes, "--version"], timeout=5)
    if available:
        return True, detail
    return False, f"{hyperframes}: {detail}"


def collect_capabilities() -> list[ToolStatus]:
    ffmpeg = find_ffmpeg_tool("ffmpeg")
    ffprobe = find_ffmpeg_tool("ffprobe")
    node = find_command(["node", "node.exe"])
    npm = find_command(["npm", "npm.cmd"])
    npx = find_command(["npx", "npx.cmd"])
    ffmpeg_available, ffmpeg_detail = _probe_version(ffmpeg, ["-version"])
    ffprobe_available, ffprobe_detail = _probe_version(ffprobe, ["-version"])
    node_available, node_detail = _probe_version(node, ["--version"])
    npm_available, npm_detail = _probe_version(npm, ["--version"])
    npx_available, npx_detail = _probe_version(npx, ["--version"])
    hyperframes_available, hyperframes_detail = _probe_hyperframes_cli()
    browser = find_browser()

    return [
        ToolStatus(
            name="FFmpeg",
            available=ffmpeg_available,
            purpose="音视频转码、混流、合成音频",
            detail=ffmpeg_detail,
        ),
        ToolStatus(
            name="ffprobe",
            available=ffprobe_available,
            purpose="读取媒体时长、编码和轨道信息",
            detail=ffprobe_detail,
        ),
        ToolStatus(
            name="Node.js",
            available=node_available,
            purpose="运行前端渲染与脚本工具链",
            detail=node_detail,
        ),
        ToolStatus(
            name="npm",
            available=npm_available,
            purpose="安装和运行 Node.js 包脚本",
            detail=npm_detail,
        ),
        ToolStatus(
            name="npx",
            available=npx_available,
            purpose="按需执行 Node.js CLI 工具",
            detail=npx_detail,
        ),
        ToolStatus(
            name="HyperFrames CLI",
            available=hyperframes_available,
            purpose="渲染 HyperFrames 视频工程",
            detail=hyperframes_detail,
        ),
        ToolStatus(
            name="Browser/media preview",
            available=browser is not None,
            purpose="预览本地页面和渲染结果",
            detail=browser or "browser command or known install path not found",
        ),
        ToolStatus(
            name="Transcription timestamps",
            available=False,
            purpose="生成逐词或分段时间戳用于字幕与剪辑对齐",
            detail="manual or environment-specific",
        ),
    ]


def assess_level(tools: list[ToolStatus]) -> CapabilityLevel:
    available = {tool.name: tool.available for tool in tools}
    has_ffmpeg = available.get("FFmpeg", False)
    has_hyperframes = available.get("HyperFrames CLI", False)
    has_browser = available.get("Browser/media preview", False)
    has_node = available.get("Node.js", False)

    if has_ffmpeg and has_hyperframes and has_browser:
        return "full"
    if has_ffmpeg and (has_hyperframes or has_node):
        return "recommended"
    return "minimal"


def build_guidance(tools: list[ToolStatus]) -> list[dict[str, str]]:
    guidance_by_tool = {
        "FFmpeg": {
            "name": "FFmpeg",
            "impact": "无法可靠完成转码、混流和合成音频，视频输出可能停在中间产物。",
            "suggested_fix": "先安装 FFmpeg，并确认 ffmpeg 可在 PATH 中运行。",
        },
        "HyperFrames CLI": {
            "name": "HyperFrames CLI",
            "impact": "无法直接渲染 HyperFrames 工程，需要改用手动预览或其他渲染路径。",
            "suggested_fix": "先安装或配置 HyperFrames CLI，并确认 hyperframes --version 可运行。",
        },
        "Transcription timestamps": {
            "name": "Transcription timestamps",
            "impact": "无法自动获得精确字幕时间戳，口播、画面和字幕可能需要人工校准。",
            "suggested_fix": "先安装带时间戳的转写工具，或在当前环境中配置可用的转写服务。",
        },
    }

    guidance: list[dict[str, str]] = []
    for tool in tools:
        if not tool.available:
            guidance.append(
                guidance_by_tool.get(
                    tool.name,
                    {
                        "name": tool.name,
                        "impact": f"{tool.purpose} 不可用，相关流程会降级或需要手动处理。",
                        "suggested_fix": f"先安装或配置 {tool.name}，然后重新检测能力。",
                    },
                )
            )
    return guidance
