from workbench.capabilities import assess_level, build_guidance
from workbench.models import ToolStatus


def tool(name, available):
    return ToolStatus(name=name, available=available, purpose="", detail="")


def test_assess_level_is_minimal_without_ffmpeg_and_renderer():
    tools = [
        tool("FFmpeg", False),
        tool("HyperFrames CLI", False),
        tool("Browser/media preview", False),
        tool("Node.js", False),
    ]

    assert assess_level(tools) == "minimal"


def test_assess_level_is_full_with_ffmpeg_hyperframes_and_browser():
    tools = [
        tool("FFmpeg", True),
        tool("ffprobe", True),
        tool("HyperFrames CLI", True),
        tool("Browser/media preview", True),
        tool("Node.js", True),
    ]

    assert assess_level(tools) == "full"


def test_assess_level_is_recommended_with_ffmpeg_and_node_without_hyperframes():
    tools = [
        tool("FFmpeg", True),
        tool("HyperFrames CLI", False),
        tool("Browser/media preview", False),
        tool("Node.js", True),
    ]

    assert assess_level(tools) == "recommended"


def test_guidance_for_missing_ffmpeg_mentions_audio_and_installation():
    tools = [
        tool("FFmpeg", False),
        tool("HyperFrames CLI", True),
        tool("Transcription timestamps", False),
    ]

    guidance = build_guidance(tools)
    ffmpeg_items = [item for item in guidance if item["name"] == "FFmpeg"]

    assert ffmpeg_items
    assert "合成音频" in ffmpeg_items[0]["impact"]
    assert "先安装" in ffmpeg_items[0]["suggested_fix"]
