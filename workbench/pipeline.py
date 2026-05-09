import json
import re
import subprocess
from dataclasses import asdict
from pathlib import Path

from workbench.capabilities import find_ffmpeg_tool
from workbench.models import JobRecord, PipelinePaths, Scene


BAD_FILENAME_CHARS = re.compile(r'[<>:"/\\|?*]+')
SENTENCE_BREAKS = re.compile(r"[。！？.!?\r\n]+")


def needs_script(record: JobRecord) -> bool:
    return not record.script.strip()


def normalize_output_name(name: str) -> str:
    safe_name = BAD_FILENAME_CHARS.sub("_", name.strip()).strip(" ._")
    if not safe_name:
        safe_name = "output"
    if not safe_name.lower().endswith(".mp4"):
        safe_name = f"{safe_name}.mp4"
    return safe_name


def split_script(script: str) -> list[str]:
    sentences = [part.strip() for part in SENTENCE_BREAKS.split(script) if part.strip()]
    return sentences or ["请补充文案后重新生成"]


def _chunk_sentences(sentences: list[str], scene_count: int) -> list[list[str]]:
    chunks: list[list[str]] = []
    for index in range(scene_count):
        start = index * len(sentences) // scene_count
        end = (index + 1) * len(sentences) // scene_count
        chunk = sentences[start:end]
        if not chunk:
            chunk = [sentences[min(index, len(sentences) - 1)]]
        chunks.append(chunk)
    return chunks


def build_scene_plan(record: JobRecord, duration_seconds: float) -> list[Scene]:
    sentences = split_script(record.script)
    scene_count = min(7, max(3, len(sentences)))
    chunks = _chunk_sentences(sentences, scene_count)
    duration = max(float(duration_seconds), 1.0)

    scenes: list[Scene] = []
    for index, chunk in enumerate(chunks):
        start = 0.0 if index == 0 else round(duration * index / scene_count, 2)
        end = duration if index == scene_count - 1 else round(duration * (index + 1) / scene_count, 2)
        headline = chunk[0][:24] or record.theme or f"场景 {index + 1}"
        scenes.append(
            Scene(
                scene_id=f"scene-{index + 1:02d}",
                start=start,
                end=end,
                headline=headline,
                support=chunk,
            )
        )
    return scenes


def probe_duration(audio_path: str | Path) -> float:
    ffprobe = find_ffmpeg_tool("ffprobe")
    if not ffprobe:
        return 45.0

    try:
        completed = subprocess.run(
            [
                ffprobe,
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                str(audio_path),
            ],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (FileNotFoundError, OSError, subprocess.TimeoutExpired):
        return 45.0

    if completed.returncode != 0:
        return 45.0

    try:
        duration = float(completed.stdout.strip())
    except ValueError:
        return 45.0
    return duration if duration > 0 else 45.0


def write_plan(record: JobRecord, paths: PipelinePaths, duration_seconds: float) -> list[Scene]:
    scenes = build_scene_plan(record, duration_seconds)
    paths.plan_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "job_id": record.job_id,
        "duration_seconds": duration_seconds,
        "scenes": [asdict(scene) for scene in scenes],
    }
    (paths.plan_dir / "scene_plan.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return scenes


def render_mvp_video(
    record: JobRecord,
    paths: PipelinePaths,
    audio_path: str | Path,
    duration_seconds: float,
) -> Path:
    ffmpeg = find_ffmpeg_tool("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("缺少 FFmpeg，无法生成 MP4。")

    paths.output_dir.mkdir(parents=True, exist_ok=True)
    output_path = paths.output_dir / normalize_output_name(record.output_name)
    duration = max(float(duration_seconds), 1.0)
    audio = Path(audio_path)

    args = [
        ffmpeg,
        "-y",
        "-f",
        "lavfi",
        "-i",
        f"color=c=0x111827:s=1080x1920:r=30:d={duration}",
    ]
    if audio.exists():
        args.extend(["-i", str(audio), "-map", "0:v:0", "-map", "1:a:0"])
    else:
        args.extend(["-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100", "-map", "0:v:0", "-map", "1:a:0"])

    args.extend(
        [
            "-t",
            str(duration),
            "-shortest",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-movflags",
            "+faststart",
            str(output_path),
        ]
    )
    completed = subprocess.run(args, capture_output=True, text=True, check=False)
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout or "FFmpeg failed").strip()
        raise RuntimeError(detail)
    return output_path


def review_video(output_path: str | Path, paths: PipelinePaths) -> dict[str, object]:
    ffprobe = find_ffmpeg_tool("ffprobe")
    ffmpeg = find_ffmpeg_tool("ffmpeg")
    paths.review_dir.mkdir(parents=True, exist_ok=True)
    output = Path(output_path)
    summary: dict[str, object] = {
        "output_path": str(output),
        "has_video": False,
        "has_audio": False,
        "contact_sheet": str(paths.review_dir / "contact.jpg"),
    }

    if ffprobe:
        try:
            completed = subprocess.run(
                [
                    ffprobe,
                    "-v",
                    "error",
                    "-show_streams",
                    "-of",
                    "json",
                    str(output),
                ],
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
            if completed.returncode == 0:
                streams = json.loads(completed.stdout or "{}").get("streams", [])
                summary["has_video"] = any(stream.get("codec_type") == "video" for stream in streams)
                summary["has_audio"] = any(stream.get("codec_type") == "audio" for stream in streams)
            else:
                summary["probe_error"] = (completed.stderr or completed.stdout).strip()
        except (FileNotFoundError, OSError, subprocess.TimeoutExpired, json.JSONDecodeError) as exc:
            summary["probe_error"] = str(exc)
    else:
        summary["probe_error"] = "缺少 ffprobe，无法检查音视频流。"

    if ffmpeg:
        contact_path = paths.review_dir / "contact.jpg"
        completed = subprocess.run(
            [
                ffmpeg,
                "-y",
                "-i",
                str(output),
                "-frames:v",
                "1",
                "-q:v",
                "2",
                str(contact_path),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        summary["contact_sheet_created"] = completed.returncode == 0 and contact_path.exists()
        if completed.returncode != 0:
            summary["contact_error"] = (completed.stderr or completed.stdout).strip()
    else:
        summary["contact_sheet_created"] = False
        summary["contact_error"] = "缺少 FFmpeg，无法生成 review/contact.jpg。"

    return summary
