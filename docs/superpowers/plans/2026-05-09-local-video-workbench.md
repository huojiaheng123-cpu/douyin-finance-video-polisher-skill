# Local Video Workbench Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a local browser workbench that accepts a finance voiceover, creates a local generation job, runs a deterministic MVP video pipeline, and returns a downloadable 9:16 MP4 with capability guidance.

**Architecture:** Add a `workbench/` Python package with focused modules for settings, capability detection, job storage, queue execution, pipeline orchestration, and the FastAPI app. Add a static workbench UI under `workbench/static/` served by FastAPI at `http://127.0.0.1:8787`, while keeping the existing GitHub Pages documentation site in `docs/` unchanged.

**Tech Stack:** Python 3.10+, FastAPI, Uvicorn, pytest, FFmpeg/ffprobe, plain HTML/CSS/JavaScript for the local UI.

---

## File Structure

- Create `requirements.txt`: runtime and test dependencies for the local app.
- Create `workbench/__init__.py`: package marker.
- Create `workbench/config.py`: filesystem paths, allowed extensions, size limits, and host/port defaults.
- Create `workbench/capabilities.py`: structured capability checks, reusing the intent of `scripts/check_capabilities.py`.
- Create `workbench/models.py`: dataclasses and typed dictionaries shared by services.
- Create `workbench/job_store.py`: create, read, update, list jobs on disk.
- Create `workbench/pipeline.py`: transcript/script handling, scene planning, FFmpeg render fallback, review checks.
- Create `workbench/queue.py`: single-worker in-process queue.
- Create `workbench/app.py`: FastAPI app and API routes.
- Create `workbench/static/index.html`: local upload/progress/download UI.
- Create `workbench/static/app.js`: browser logic for upload and polling.
- Create `workbench/static/styles.css`: local tool interface styling.
- Create `scripts/run_workbench.py`: launches Uvicorn on `127.0.0.1:8787`.
- Create `tests/test_capabilities.py`: capability result tests.
- Create `tests/test_job_store.py`: job filesystem tests.
- Create `tests/test_pipeline.py`: script fallback and review tests.
- Create `tests/test_app.py`: API route tests with FastAPI TestClient.
- Modify `README.md`: add local workbench usage instructions.

## Task 1: Project Dependencies and Settings

**Files:**
- Create: `requirements.txt`
- Create: `workbench/__init__.py`
- Create: `workbench/config.py`
- Test: `tests/test_config.py`

- [ ] **Step 1: Write the failing config tests**

Create `tests/test_config.py`:

```python
from pathlib import Path

from workbench.config import Settings


def test_default_settings_point_inside_repo(tmp_path: Path):
    settings = Settings(base_dir=tmp_path)

    assert settings.jobs_dir == tmp_path / "workbench_data" / "jobs"
    assert settings.static_dir.name == "static"
    assert settings.host == "127.0.0.1"
    assert settings.port == 8787


def test_audio_extension_validation_is_case_insensitive(tmp_path: Path):
    settings = Settings(base_dir=tmp_path)

    assert settings.is_allowed_audio("voice.WAV")
    assert settings.is_allowed_audio("voice.mp3")
    assert settings.is_allowed_audio("voice.m4a")
    assert not settings.is_allowed_audio("voice.exe")
```

- [ ] **Step 2: Run the failing tests**

Run:

```bash
pytest tests/test_config.py -v
```

Expected: FAIL because `workbench.config` does not exist.

- [ ] **Step 3: Add dependencies**

Create `requirements.txt`:

```text
fastapi>=0.110
uvicorn[standard]>=0.27
python-multipart>=0.0.9
pytest>=8.0
httpx>=0.27
```

- [ ] **Step 4: Add the package and settings**

Create `workbench/__init__.py`:

```python
"""Local video generation workbench for douyin-finance-video-polisher."""
```

Create `workbench/config.py`:

```python
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Settings:
    base_dir: Path = REPO_ROOT
    host: str = "127.0.0.1"
    port: int = 8787
    max_upload_bytes: int = 200 * 1024 * 1024
    allowed_audio_extensions: frozenset[str] = field(default_factory=lambda: frozenset({".wav", ".mp3", ".m4a"}))

    @property
    def jobs_dir(self) -> Path:
        return self.base_dir / "workbench_data" / "jobs"

    @property
    def static_dir(self) -> Path:
        return self.base_dir / "workbench" / "static"

    def is_allowed_audio(self, filename: str) -> bool:
        return Path(filename).suffix.lower() in self.allowed_audio_extensions
```

- [ ] **Step 5: Run the tests**

Run:

```bash
pytest tests/test_config.py -v
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add requirements.txt workbench/__init__.py workbench/config.py tests/test_config.py
git commit -m "Add workbench settings"
```

## Task 2: Structured Capability Detection

**Files:**
- Create: `workbench/models.py`
- Create: `workbench/capabilities.py`
- Test: `tests/test_capabilities.py`

- [ ] **Step 1: Write capability tests**

Create `tests/test_capabilities.py`:

```python
from workbench.capabilities import assess_level, build_guidance
from workbench.models import ToolStatus


def test_assess_level_minimal_without_ffmpeg_or_renderer():
    tools = [
        ToolStatus(name="FFmpeg", available=False, purpose="mux audio", detail="not found"),
        ToolStatus(name="HyperFrames CLI", available=False, purpose="render video", detail="not found"),
        ToolStatus(name="Browser/media preview", available=True, purpose="watch motion", detail="chrome"),
    ]

    assert assess_level(tools) == "minimal"


def test_assess_level_full_with_ffmpeg_renderer_and_preview():
    tools = [
        ToolStatus(name="FFmpeg", available=True, purpose="mux audio", detail="ffmpeg version"),
        ToolStatus(name="ffprobe", available=True, purpose="inspect streams", detail="ffprobe version"),
        ToolStatus(name="HyperFrames CLI", available=True, purpose="render video", detail="1.0.0"),
        ToolStatus(name="Browser/media preview", available=True, purpose="watch motion", detail="chrome"),
    ]

    assert assess_level(tools) == "full"


def test_guidance_explains_missing_ffmpeg():
    tool = ToolStatus(name="FFmpeg", available=False, purpose="合成音频、抽帧和检查媒体流", detail="not found")

    guidance = build_guidance([tool])

    assert "FFmpeg" in guidance[0]["name"]
    assert "合成音频" in guidance[0]["impact"]
    assert "先安装" in guidance[0]["suggested_fix"]
```

- [ ] **Step 2: Run the failing tests**

Run:

```bash
pytest tests/test_capabilities.py -v
```

Expected: FAIL because the modules do not exist.

- [ ] **Step 3: Add shared models**

Create `workbench/models.py`:

```python
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal


CapabilityLevel = Literal["minimal", "recommended", "full"]
JobStatus = Literal[
    "queued",
    "checking_capabilities",
    "needs_script",
    "planning",
    "rendering",
    "reviewing",
    "completed",
    "failed",
]


@dataclass(frozen=True)
class ToolStatus:
    name: str
    available: bool
    purpose: str
    detail: str


@dataclass
class JobRecord:
    job_id: str
    status: JobStatus
    created_at: str
    updated_at: str
    theme: str
    traffic_word: str
    template: str
    output_name: str
    script: str = ""
    error: str = ""
    progress: list[str] = field(default_factory=list)
    input_audio: str = ""
    output_video: str = ""
    review_summary: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class Scene:
    scene_id: str
    start: float
    end: float
    headline: str
    support: list[str]


@dataclass(frozen=True)
class PipelinePaths:
    job_dir: Path
    input_dir: Path
    transcript_dir: Path
    plan_dir: Path
    render_dir: Path
    review_dir: Path
    output_dir: Path
```

- [ ] **Step 4: Add capability detection**

Create `workbench/capabilities.py`:

```python
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from workbench.models import CapabilityLevel, ToolStatus


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
    return existing_path([
        Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
        Path("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"),
        Path("C:/Program Files/Microsoft/Edge/Application/msedge.exe"),
        Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"),
        home / "AppData" / "Local" / "Google" / "Chrome" / "Application" / "chrome.exe",
        home / "AppData" / "Local" / "Microsoft" / "Edge" / "Application" / "msedge.exe",
    ])


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
    return proc.returncode == 0, output[0] if output else ""


def collect_capabilities() -> list[ToolStatus]:
    ffmpeg = find_ffmpeg_tool("ffmpeg")
    ffmpeg_ok, ffmpeg_detail = try_command([ffmpeg, "-version"]) if ffmpeg else (False, "not found")

    ffprobe = find_ffmpeg_tool("ffprobe")
    ffprobe_ok, ffprobe_detail = try_command([ffprobe, "-version"]) if ffprobe else (False, "not found")

    node = find_command(["node", "node.exe"])
    node_ok, node_detail = try_command([node, "--version"]) if node else (False, "not found")

    npm = find_command(["npm", "npm.cmd"])
    npm_ok, npm_detail = try_command([npm, "--version"]) if npm else (False, "not found")

    npx = find_command(["npx", "npx.cmd"])
    npx_ok, npx_detail = try_command([npx, "--version"]) if npx else (False, "not found")

    hyperframes = find_hyperframes_cli()
    hyperframes_ok, hyperframes_detail = (
        try_command([hyperframes, "--version"]) if hyperframes else (False, "local command not found")
    )

    browser = find_browser()

    return [
        ToolStatus("FFmpeg", ffmpeg_ok, "合成音频、抽帧和检查媒体流", ffmpeg_detail),
        ToolStatus("ffprobe", ffprobe_ok, "读取音频/视频时长和流信息", ffprobe_detail),
        ToolStatus("Node.js", node_ok, "运行 HyperFrames 和浏览器工具", node_detail),
        ToolStatus("npm", npm_ok, "安装或执行前端渲染工具", npm_detail),
        ToolStatus("npx", npx_ok, "无需全局安装即可运行 CLI", npx_detail),
        ToolStatus("HyperFrames CLI", hyperframes_ok, "渲染 HTML 视频和检查布局", hyperframes_detail),
        ToolStatus("Browser/media preview", bool(browser), "动态检查转场和音画同步", browser or "not found"),
        ToolStatus("Transcription timestamps", False, "精准语义分段", "manual or environment-specific"),
    ]


def assess_level(tools: list[ToolStatus]) -> CapabilityLevel:
    by_name = {tool.name: tool.available for tool in tools}
    has_ffmpeg = by_name.get("FFmpeg", False)
    has_renderer = by_name.get("HyperFrames CLI", False)
    has_preview = by_name.get("Browser/media preview", False)
    has_node = by_name.get("Node.js", False)

    if has_ffmpeg and has_renderer and has_preview:
        return "full"
    if has_ffmpeg and (has_renderer or has_node):
        return "recommended"
    return "minimal"


def build_guidance(tools: list[ToolStatus]) -> list[dict[str, str]]:
    guidance: list[dict[str, str]] = []
    for tool in tools:
        if tool.available:
            continue
        if tool.name == "FFmpeg":
            impact = "缺少 FFmpeg 时，无法可靠合成音频、抽动态复审图或检查最终视频流。"
            fix = "先安装或配置 FFmpeg，因为它对生成和复审质量提升最大。"
        elif tool.name == "HyperFrames CLI":
            impact = "缺少 HyperFrames CLI 时，HTML 动效视频不能直接渲染成 MP4。"
            fix = "配置 HyperFrames CLI，或先使用 FFmpeg MVP 渲染作为过渡。"
        elif tool.name == "Transcription timestamps":
            impact = "缺少转写时间戳时，系统只能按文案和时长粗略拆分场景。"
            fix = "先手动填写文案；后续再接 Whisper 或其他转写工具。"
        else:
            impact = f"缺少 {tool.name} 会影响：{tool.purpose}。"
            fix = f"安装或配置 {tool.name} 后再重新检测。"
        guidance.append({"name": tool.name, "impact": impact, "suggested_fix": fix})
    return guidance
```

- [ ] **Step 5: Run the capability tests**

Run:

```bash
pytest tests/test_capabilities.py -v
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add workbench/models.py workbench/capabilities.py tests/test_capabilities.py
git commit -m "Add structured capability detection"
```

## Task 3: Disk Job Store

**Files:**
- Create: `workbench/job_store.py`
- Test: `tests/test_job_store.py`

- [ ] **Step 1: Write job store tests**

Create `tests/test_job_store.py`:

```python
from pathlib import Path

from workbench.config import Settings
from workbench.job_store import JobStore


def test_create_job_builds_expected_directories(tmp_path: Path):
    store = JobStore(Settings(base_dir=tmp_path))

    record, paths = store.create_job(
        theme="AI炒股",
        traffic_word="AI量化",
        template="ai_quant",
        output_name="AI炒股测试",
        script="AI 都在炒股了，你还只是在手机上看 K 线？",
        original_filename="voice.wav",
    )

    assert record.status == "queued"
    assert paths.input_dir.exists()
    assert paths.transcript_dir.exists()
    assert paths.plan_dir.exists()
    assert paths.render_dir.exists()
    assert paths.review_dir.exists()
    assert paths.output_dir.exists()
    assert (paths.job_dir / "job.json").exists()


def test_update_job_persists_status_and_progress(tmp_path: Path):
    store = JobStore(Settings(base_dir=tmp_path))
    record, _ = store.create_job(
        theme="技术分析",
        traffic_word="技术分析",
        template="technical",
        output_name="测试",
        script="不要再学新指标了。",
        original_filename="voice.wav",
    )

    updated = store.update_job(record.job_id, status="planning", progress_entry="已生成分镜")
    loaded = store.get_job(record.job_id)

    assert updated.status == "planning"
    assert loaded.status == "planning"
    assert "已生成分镜" in loaded.progress


def test_list_jobs_returns_newest_first(tmp_path: Path):
    store = JobStore(Settings(base_dir=tmp_path))
    first, _ = store.create_job("A", "词", "technical", "A", "文案", "a.wav")
    second, _ = store.create_job("B", "词", "book", "B", "文案", "b.wav")

    jobs = store.list_jobs()

    assert [job.job_id for job in jobs] == [second.job_id, first.job_id]
```

- [ ] **Step 2: Run the failing tests**

Run:

```bash
pytest tests/test_job_store.py -v
```

Expected: FAIL because `workbench.job_store` does not exist.

- [ ] **Step 3: Implement the job store**

Create `workbench/job_store.py`:

```python
from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from workbench.config import Settings
from workbench.models import JobRecord, JobStatus, PipelinePaths


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class JobStore:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def create_job(
        self,
        theme: str,
        traffic_word: str,
        template: str,
        output_name: str,
        script: str,
        original_filename: str,
    ) -> tuple[JobRecord, PipelinePaths]:
        job_id = datetime.now().strftime("%Y%m%d%H%M%S") + "-" + uuid4().hex[:8]
        paths = self.paths_for(job_id)
        for path in [
            paths.input_dir,
            paths.transcript_dir,
            paths.plan_dir,
            paths.render_dir,
            paths.review_dir,
            paths.output_dir,
        ]:
            path.mkdir(parents=True, exist_ok=True)

        now = utc_now()
        record = JobRecord(
            job_id=job_id,
            status="queued",
            created_at=now,
            updated_at=now,
            theme=theme.strip(),
            traffic_word=traffic_word.strip(),
            template=template.strip(),
            output_name=output_name.strip() or job_id,
            script=script.strip(),
            input_audio=f"input/{original_filename}",
            progress=["任务已创建"],
        )
        self.save_job(record)
        return record, paths

    def paths_for(self, job_id: str) -> PipelinePaths:
        job_dir = self.settings.jobs_dir / job_id
        return PipelinePaths(
            job_dir=job_dir,
            input_dir=job_dir / "input",
            transcript_dir=job_dir / "transcript",
            plan_dir=job_dir / "plan",
            render_dir=job_dir / "render",
            review_dir=job_dir / "review",
            output_dir=job_dir / "output",
        )

    def get_job(self, job_id: str) -> JobRecord:
        path = self.paths_for(job_id).job_dir / "job.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        return JobRecord(**data)

    def save_job(self, record: JobRecord) -> None:
        path = self.paths_for(record.job_id).job_dir / "job.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(asdict(record), ensure_ascii=False, indent=2), encoding="utf-8")

    def update_job(
        self,
        job_id: str,
        *,
        status: JobStatus | None = None,
        progress_entry: str | None = None,
        error: str | None = None,
        output_video: str | None = None,
        review_summary: dict[str, object] | None = None,
    ) -> JobRecord:
        record = self.get_job(job_id)
        if status is not None:
            record.status = status
        if progress_entry:
            record.progress.append(progress_entry)
        if error is not None:
            record.error = error
        if output_video is not None:
            record.output_video = output_video
        if review_summary is not None:
            record.review_summary = review_summary
        record.updated_at = utc_now()
        self.save_job(record)
        return record

    def list_jobs(self) -> list[JobRecord]:
        if not self.settings.jobs_dir.exists():
            return []
        records = []
        for job_json in self.settings.jobs_dir.glob("*/job.json"):
            data = json.loads(job_json.read_text(encoding="utf-8"))
            records.append(JobRecord(**data))
        return sorted(records, key=lambda job: job.created_at, reverse=True)
```

- [ ] **Step 4: Run the job store tests**

Run:

```bash
pytest tests/test_job_store.py -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add workbench/job_store.py tests/test_job_store.py
git commit -m "Add local job store"
```

## Task 4: MVP Pipeline

**Files:**
- Create: `workbench/pipeline.py`
- Test: `tests/test_pipeline.py`

- [ ] **Step 1: Write pipeline tests**

Create `tests/test_pipeline.py`:

```python
from pathlib import Path

from workbench.models import JobRecord
from workbench.pipeline import build_scene_plan, normalize_output_name, needs_script


def make_job(script: str = "你不要再学新指标了。问题不在指标不够多，而是没验证。") -> JobRecord:
    return JobRecord(
        job_id="job-1",
        status="queued",
        created_at="2026-05-09T00:00:00+00:00",
        updated_at="2026-05-09T00:00:00+00:00",
        theme="技术分析",
        traffic_word="技术分析",
        template="technical",
        output_name="测试视频",
        script=script,
        input_audio="input/voice.wav",
    )


def test_needs_script_when_script_is_blank():
    assert needs_script(make_job(script=""))
    assert not needs_script(make_job(script="已经有文案"))


def test_scene_plan_has_at_least_three_visual_recipes():
    scenes = build_scene_plan(make_job(), duration_seconds=45)

    assert len(scenes) >= 3
    assert scenes[0].start == 0
    assert scenes[-1].end == 45
    assert all(scene.headline for scene in scenes)


def test_normalize_output_name_adds_mp4_and_removes_bad_characters():
    assert normalize_output_name("AI:炒股?") == "AI_炒股.mp4"
    assert normalize_output_name("成片.mp4") == "成片.mp4"
```

- [ ] **Step 2: Run the failing tests**

Run:

```bash
pytest tests/test_pipeline.py -v
```

Expected: FAIL because `workbench.pipeline` does not exist.

- [ ] **Step 3: Implement deterministic planning helpers and FFmpeg MVP renderer**

Create `workbench/pipeline.py`:

```python
from __future__ import annotations

import json
import math
import re
import subprocess
from pathlib import Path

from workbench.capabilities import find_ffmpeg_tool
from workbench.models import JobRecord, PipelinePaths, Scene


BAD_FILENAME_CHARS = re.compile(r'[<>:"/\\\\|?*]+')


def needs_script(record: JobRecord) -> bool:
    return not record.script.strip()


def normalize_output_name(name: str) -> str:
    cleaned = BAD_FILENAME_CHARS.sub("_", name.strip()) or "output"
    return cleaned if cleaned.lower().endswith(".mp4") else f"{cleaned}.mp4"


def split_script(script: str) -> list[str]:
    parts = [part.strip() for part in re.split(r"[。！？!?\\n]+", script) if part.strip()]
    return parts or ["请补充文案后重新生成"]


def build_scene_plan(record: JobRecord, duration_seconds: float) -> list[Scene]:
    sentences = split_script(record.script)
    scene_count = max(3, min(7, len(sentences)))
    chunk_size = max(1, math.ceil(len(sentences) / scene_count))
    chunks = [sentences[index : index + chunk_size] for index in range(0, len(sentences), chunk_size)]
    chunks = chunks[:scene_count]
    scene_count = len(chunks)
    scene_duration = duration_seconds / scene_count
    scenes: list[Scene] = []

    for index, chunk in enumerate(chunks):
        start = round(index * scene_duration, 2)
        end = round(duration_seconds if index == scene_count - 1 else (index + 1) * scene_duration, 2)
        headline = chunk[0]
        support = chunk[1:4] or [record.traffic_word or record.theme, "验证", "结果"]
        scenes.append(Scene(f"s{index + 1}", start, end, headline, support))
    return scenes


def probe_duration(audio_path: Path) -> float:
    ffprobe = find_ffmpeg_tool("ffprobe")
    if not ffprobe:
        return 45.0
    proc = subprocess.run(
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
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    try:
        return max(1.0, float(proc.stdout.strip()))
    except ValueError:
        return 45.0


def write_plan(record: JobRecord, paths: PipelinePaths, duration_seconds: float) -> list[Scene]:
    scenes = build_scene_plan(record, duration_seconds)
    payload = [
        {"scene_id": s.scene_id, "start": s.start, "end": s.end, "headline": s.headline, "support": s.support}
        for s in scenes
    ]
    (paths.plan_dir / "scene_plan.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return scenes


def render_mvp_video(record: JobRecord, paths: PipelinePaths, audio_path: Path, duration_seconds: float) -> Path:
    ffmpeg = find_ffmpeg_tool("ffmpeg")
    output = paths.output_dir / normalize_output_name(record.output_name)
    if not ffmpeg:
        raise RuntimeError("缺少 FFmpeg，无法生成 MP4。")

    title = record.theme or record.traffic_word or "财经短视频"
    subtitle = record.script[:42].replace(":", "：").replace("'", "")
    draw_title = f"drawtext=text='{title}':fontcolor=0x11141b:fontsize=72:x=88:y=260"
    draw_subtitle = f"drawtext=text='{subtitle}':fontcolor=0x16886b:fontsize=44:x=88:y=420"
    vf = (
        "color=c=0xfbfbf7:s=1080x1920,"
        "format=yuv420p,"
        f"{draw_title},"
        f"{draw_subtitle}"
    )
    proc = subprocess.run(
        [
            ffmpeg,
            "-y",
            "-f",
            "lavfi",
            "-i",
            vf,
            "-i",
            str(audio_path),
            "-t",
            str(duration_seconds),
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            "-c:v",
            "libx264",
            "-c:a",
            "aac",
            "-b:a",
            "160k",
            "-shortest",
            str(output),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr[-1200:])
    return output


def review_video(output_path: Path, paths: PipelinePaths) -> dict[str, object]:
    ffprobe = find_ffmpeg_tool("ffprobe")
    summary: dict[str, object] = {"output_exists": output_path.exists(), "has_media_probe": False}
    if ffprobe and output_path.exists():
        proc = subprocess.run(
            [ffprobe, "-v", "error", "-show_streams", "-of", "json", str(output_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        summary["has_media_probe"] = proc.returncode == 0
        if proc.returncode == 0:
            data = json.loads(proc.stdout)
            codec_types = sorted({stream.get("codec_type", "") for stream in data.get("streams", [])})
            summary["streams"] = codec_types
            summary["has_audio"] = "audio" in codec_types
            summary["has_video"] = "video" in codec_types

    ffmpeg = find_ffmpeg_tool("ffmpeg")
    contact_sheet = paths.review_dir / "contact.jpg"
    if ffmpeg and output_path.exists():
        subprocess.run(
            [
                ffmpeg,
                "-y",
                "-i",
                str(output_path),
                "-vf",
                "fps=1/8,scale=270:480,tile=3x3",
                str(contact_sheet),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
    summary["contact_sheet"] = str(contact_sheet.relative_to(paths.job_dir)) if contact_sheet.exists() else ""
    return summary
```

- [ ] **Step 4: Run pipeline tests**

Run:

```bash
pytest tests/test_pipeline.py -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add workbench/pipeline.py tests/test_pipeline.py
git commit -m "Add MVP video pipeline helpers"
```

## Task 5: Queue Runner

**Files:**
- Create: `workbench/queue.py`
- Test: `tests/test_queue.py`

- [ ] **Step 1: Write queue tests**

Create `tests/test_queue.py`:

```python
from pathlib import Path

from workbench.config import Settings
from workbench.job_store import JobStore
from workbench.queue import WorkbenchQueue


def test_queue_marks_blank_script_job_as_needs_script(tmp_path: Path):
    store = JobStore(Settings(base_dir=tmp_path))
    record, _ = store.create_job("主题", "词", "technical", "输出", "", "voice.wav")
    queue = WorkbenchQueue(store)

    queue.run_job(record.job_id)
    updated = store.get_job(record.job_id)

    assert updated.status == "needs_script"
    assert "文案" in updated.error
```

- [ ] **Step 2: Run failing queue tests**

Run:

```bash
pytest tests/test_queue.py -v
```

Expected: FAIL because `workbench.queue` does not exist.

- [ ] **Step 3: Implement the queue**

Create `workbench/queue.py`:

```python
from __future__ import annotations

import shutil
import threading
from pathlib import Path

from workbench.job_store import JobStore
from workbench.pipeline import needs_script, probe_duration, render_mvp_video, review_video, write_plan


class WorkbenchQueue:
    def __init__(self, store: JobStore) -> None:
        self.store = store
        self._lock = threading.Lock()

    def enqueue(self, job_id: str) -> None:
        thread = threading.Thread(target=self.run_job, args=(job_id,), daemon=True)
        thread.start()

    def run_job(self, job_id: str) -> None:
        with self._lock:
            record = self.store.get_job(job_id)
            paths = self.store.paths_for(job_id)
            try:
                self.store.update_job(job_id, status="checking_capabilities", progress_entry="开始检查输入")
                if needs_script(record):
                    self.store.update_job(
                        job_id,
                        status="needs_script",
                        error="当前没有可用文案。请在页面补充文案后重新创建任务。",
                        progress_entry="需要补充文案",
                    )
                    return

                input_audio = paths.job_dir / record.input_audio
                if not input_audio.exists():
                    raise RuntimeError("上传音频不存在，请重新上传。")

                self.store.update_job(job_id, status="planning", progress_entry="开始生成分镜")
                duration = probe_duration(input_audio)
                write_plan(record, paths, duration)

                self.store.update_job(job_id, status="rendering", progress_entry="开始渲染 MVP 视频")
                output_video = render_mvp_video(record, paths, input_audio, duration)

                self.store.update_job(job_id, status="reviewing", progress_entry="开始生成复审证据")
                review = review_video(output_video, paths)

                self.store.update_job(
                    job_id,
                    status="completed",
                    progress_entry="视频生成完成",
                    output_video=str(output_video.relative_to(paths.job_dir)),
                    review_summary=review,
                )
            except Exception as exc:
                self.store.update_job(job_id, status="failed", error=str(exc), progress_entry="任务失败")


def save_upload(upload_file, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("wb") as handle:
        shutil.copyfileobj(upload_file.file, handle)
```

- [ ] **Step 4: Run queue tests**

Run:

```bash
pytest tests/test_queue.py -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add workbench/queue.py tests/test_queue.py
git commit -m "Add serial workbench queue"
```

## Task 6: FastAPI Routes

**Files:**
- Create: `workbench/app.py`
- Test: `tests/test_app.py`

- [ ] **Step 1: Write API tests**

Create `tests/test_app.py`:

```python
from pathlib import Path

from fastapi.testclient import TestClient

from workbench.app import create_app
from workbench.config import Settings


def test_capabilities_endpoint_returns_level(tmp_path: Path):
    client = TestClient(create_app(Settings(base_dir=tmp_path), start_background_jobs=False))

    response = client.get("/api/capabilities")

    assert response.status_code == 200
    assert response.json()["level"] in {"minimal", "recommended", "full"}


def test_create_job_requires_audio_extension(tmp_path: Path):
    client = TestClient(create_app(Settings(base_dir=tmp_path), start_background_jobs=False))

    response = client.post(
        "/api/jobs",
        data={"theme": "主题", "traffic_word": "词", "template": "technical", "output_name": "输出", "script": "文案"},
        files={"audio": ("bad.exe", b"fake", "application/octet-stream")},
    )

    assert response.status_code == 400
    assert "音频" in response.json()["detail"]


def test_create_and_fetch_job(tmp_path: Path):
    client = TestClient(create_app(Settings(base_dir=tmp_path), start_background_jobs=False))

    created = client.post(
        "/api/jobs",
        data={"theme": "主题", "traffic_word": "词", "template": "technical", "output_name": "输出", "script": "文案"},
        files={"audio": ("voice.wav", b"fake-wave", "audio/wav")},
    )

    assert created.status_code == 200
    job_id = created.json()["job_id"]
    fetched = client.get(f"/api/jobs/{job_id}")
    assert fetched.status_code == 200
    assert fetched.json()["job_id"] == job_id
```

- [ ] **Step 2: Run failing API tests**

Run:

```bash
pytest tests/test_app.py -v
```

Expected: FAIL because `workbench.app` does not exist.

- [ ] **Step 3: Implement the FastAPI app**

Create `workbench/app.py`:

```python
from __future__ import annotations

from dataclasses import asdict

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from workbench.capabilities import assess_level, build_guidance, collect_capabilities
from workbench.config import Settings
from workbench.job_store import JobStore
from workbench.queue import WorkbenchQueue, save_upload


def create_app(settings: Settings | None = None, *, start_background_jobs: bool = True) -> FastAPI:
    settings = settings or Settings()
    store = JobStore(settings)
    queue = WorkbenchQueue(store)
    app = FastAPI(title="Douyin Finance Video Workbench")

    @app.get("/api/capabilities")
    def capabilities():
        tools = collect_capabilities()
        return {
            "level": assess_level(tools),
            "tools": [asdict(tool) for tool in tools],
            "guidance": build_guidance(tools),
        }

    @app.post("/api/jobs")
    def create_job(
        theme: str = Form(""),
        traffic_word: str = Form(""),
        template: str = Form("technical"),
        output_name: str = Form(""),
        script: str = Form(""),
        audio: UploadFile = File(...),
    ):
        if not audio.filename or not settings.is_allowed_audio(audio.filename):
            raise HTTPException(status_code=400, detail="请上传 .wav、.mp3 或 .m4a 音频文件。")

        record, paths = store.create_job(theme, traffic_word, template, output_name, script, audio.filename)
        save_upload(audio, paths.input_dir / audio.filename)
        if start_background_jobs:
            queue.enqueue(record.job_id)
        return asdict(store.get_job(record.job_id))

    @app.get("/api/jobs")
    def list_jobs():
        return [asdict(job) for job in store.list_jobs()]

    @app.get("/api/jobs/{job_id}")
    def get_job(job_id: str):
        try:
            return asdict(store.get_job(job_id))
        except FileNotFoundError as exc:
            raise HTTPException(status_code=404, detail="任务不存在。") from exc

    @app.get("/api/jobs/{job_id}/download")
    def download_job(job_id: str):
        record = store.get_job(job_id)
        if not record.output_video:
            raise HTTPException(status_code=404, detail="任务还没有生成视频。")
        path = store.paths_for(job_id).job_dir / record.output_video
        if not path.exists():
            raise HTTPException(status_code=404, detail="输出文件不存在。")
        return FileResponse(path, media_type="video/mp4", filename=path.name)

    @app.get("/api/jobs/{job_id}/review")
    def review_job(job_id: str):
        record = store.get_job(job_id)
        return {"job_id": job_id, "review_summary": record.review_summary}

    if settings.static_dir.exists():
        app.mount("/", StaticFiles(directory=settings.static_dir, html=True), name="static")

    return app


app = create_app()
```

- [ ] **Step 4: Run API tests**

Run:

```bash
pytest tests/test_app.py -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add workbench/app.py tests/test_app.py
git commit -m "Add local workbench API"
```

## Task 7: Local UI

**Files:**
- Create: `workbench/static/index.html`
- Create: `workbench/static/styles.css`
- Create: `workbench/static/app.js`

- [ ] **Step 1: Add the HTML shell**

Create `workbench/static/index.html`:

```html
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>本地财经视频生成工作台</title>
    <link rel="stylesheet" href="/styles.css" />
  </head>
  <body>
    <header class="topbar">
      <div class="brand"><span>9:16</span> 本地财经视频生成工作台</div>
      <button id="refreshCapabilities">重新检测</button>
    </header>
    <main>
      <section class="panel" id="capabilityPanel">
        <h1>上传配音，生成竖屏财经短视频</h1>
        <p id="capabilitySummary">正在检测本机视频能力...</p>
        <div id="toolList" class="tool-list"></div>
      </section>

      <section class="workspace">
        <form id="jobForm" class="panel form-panel">
          <label>音频文件 <input name="audio" type="file" accept=".wav,.mp3,.m4a,audio/*" required /></label>
          <label>视频主题 <input name="theme" placeholder="例如：AI炒股" /></label>
          <label>流量词 <input name="traffic_word" placeholder="例如：AI量化" /></label>
          <label>模板风格
            <select name="template">
              <option value="technical">技术分析</option>
              <option value="ai_quant">AI量化</option>
              <option value="book">书籍推荐</option>
            </select>
          </label>
          <label>输出文件名 <input name="output_name" placeholder="例如：AI炒股_精修版" /></label>
          <label>文案 <textarea name="script" rows="8" placeholder="没有本地转写能力时，请把文案粘贴到这里。"></textarea></label>
          <button class="primary" type="submit">开始生成</button>
        </form>

        <section class="panel">
          <h2>当前任务</h2>
          <div id="currentJob" class="empty">还没有任务。</div>
        </section>
      </section>

      <section class="panel">
        <h2>最近任务</h2>
        <div id="jobList" class="job-list"></div>
      </section>
    </main>
    <script src="/app.js"></script>
  </body>
</html>
```

- [ ] **Step 2: Add the CSS**

Create `workbench/static/styles.css`:

```css
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  color: #10131a;
  background:
    linear-gradient(rgba(16, 19, 26, 0.055) 1px, transparent 1px),
    linear-gradient(90deg, rgba(16, 19, 26, 0.055) 1px, transparent 1px),
    #fbfbf7;
  background-size: 44px 44px;
  font-family: "Microsoft YaHei", "PingFang SC", system-ui, sans-serif;
}

.topbar {
  position: sticky;
  top: 0;
  z-index: 10;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding: 18px 28px;
  border-bottom: 1px solid rgba(16, 19, 26, 0.1);
  background: rgba(251, 251, 247, 0.94);
}

.brand {
  font-size: 18px;
  font-weight: 900;
}

.brand span {
  display: inline-grid;
  place-items: center;
  width: 38px;
  height: 34px;
  margin-right: 8px;
  border: 2px solid #c88f2b;
  color: #16886b;
}

button {
  border: 1px solid rgba(16, 19, 26, 0.18);
  background: #fff;
  color: #10131a;
  padding: 10px 14px;
  font-weight: 900;
  cursor: pointer;
}

.primary {
  background: #10131a;
  color: #fff;
}

main {
  max-width: 1180px;
  margin: 0 auto;
  padding: 28px;
}

.panel {
  background: rgba(255, 255, 255, 0.82);
  border: 1px solid rgba(16, 19, 26, 0.1);
  padding: 24px;
  margin-bottom: 18px;
  box-shadow: 0 18px 44px rgba(16, 19, 26, 0.06);
}

h1 {
  margin: 0 0 10px;
  font-size: 42px;
  line-height: 1.12;
}

h2 {
  margin: 0 0 16px;
}

.workspace {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(320px, 0.85fr);
  gap: 18px;
}

.form-panel {
  display: grid;
  gap: 14px;
}

label {
  display: grid;
  gap: 7px;
  color: #5b6573;
  font-weight: 800;
}

input,
select,
textarea {
  width: 100%;
  border: 1px solid rgba(16, 19, 26, 0.16);
  background: #fff;
  padding: 12px;
  color: #10131a;
  font: inherit;
}

.tool-list,
.job-list {
  display: grid;
  gap: 10px;
}

.tool,
.job {
  border: 1px solid rgba(16, 19, 26, 0.1);
  background: #fff;
  padding: 12px;
}

.ok {
  color: #16886b;
  font-weight: 900;
}

.missing,
.failed {
  color: #e45a4d;
  font-weight: 900;
}

.empty {
  color: #5b6573;
}

@media (max-width: 860px) {
  .topbar,
  .workspace {
    display: block;
  }

  .topbar button {
    margin-top: 12px;
  }

  main {
    padding: 16px;
  }

  h1 {
    font-size: 31px;
  }
}
```

- [ ] **Step 3: Add the browser logic**

Create `workbench/static/app.js`:

```javascript
const capabilitySummary = document.querySelector("#capabilitySummary");
const toolList = document.querySelector("#toolList");
const jobForm = document.querySelector("#jobForm");
const currentJob = document.querySelector("#currentJob");
const jobList = document.querySelector("#jobList");
const refreshCapabilities = document.querySelector("#refreshCapabilities");

let activeJobId = null;
let pollTimer = null;

async function loadCapabilities() {
  const response = await fetch("/api/capabilities");
  const data = await response.json();
  capabilitySummary.textContent = `当前能力等级：${data.level}`;
  toolList.innerHTML = data.tools
    .map((tool) => {
      const cls = tool.available ? "ok" : "missing";
      const state = tool.available ? "可用" : "缺少";
      return `<div class="tool"><strong>${tool.name}</strong> <span class="${cls}">${state}</span><br><small>${tool.purpose}｜${tool.detail}</small></div>`;
    })
    .join("");
}

function renderJob(job) {
  const download = job.status === "completed"
    ? `<p><a href="/api/jobs/${job.job_id}/download">下载 MP4</a></p>`
    : "";
  const progress = (job.progress || []).map((item) => `<li>${item}</li>`).join("");
  const error = job.error ? `<p class="failed">${job.error}</p>` : "";
  return `<div class="job">
    <strong>${job.output_name || job.job_id}</strong>
    <p>状态：${job.status}</p>
    ${error}
    <ul>${progress}</ul>
    ${download}
  </div>`;
}

async function loadJobs() {
  const response = await fetch("/api/jobs");
  const jobs = await response.json();
  jobList.innerHTML = jobs.length ? jobs.map(renderJob).join("") : '<div class="empty">暂无历史任务。</div>';
}

async function pollJob(jobId) {
  const response = await fetch(`/api/jobs/${jobId}`);
  const job = await response.json();
  currentJob.innerHTML = renderJob(job);
  await loadJobs();
  if (["completed", "failed", "needs_script"].includes(job.status)) {
    clearInterval(pollTimer);
    pollTimer = null;
  }
}

jobForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const formData = new FormData(jobForm);
  currentJob.textContent = "正在上传并创建任务...";
  const response = await fetch("/api/jobs", { method: "POST", body: formData });
  if (!response.ok) {
    const error = await response.json();
    currentJob.innerHTML = `<p class="failed">${error.detail || "创建任务失败"}</p>`;
    return;
  }
  const job = await response.json();
  activeJobId = job.job_id;
  currentJob.innerHTML = renderJob(job);
  if (pollTimer) {
    clearInterval(pollTimer);
  }
  pollTimer = setInterval(() => pollJob(activeJobId), 1600);
});

refreshCapabilities.addEventListener("click", loadCapabilities);

loadCapabilities();
loadJobs();
```

- [ ] **Step 4: Commit**

```bash
git add workbench/static/index.html workbench/static/styles.css workbench/static/app.js
git commit -m "Add local workbench UI"
```

## Task 8: Launcher and Documentation

**Files:**
- Create: `scripts/run_workbench.py`
- Modify: `README.md`

- [ ] **Step 1: Add the launcher**

Create `scripts/run_workbench.py`:

```python
#!/usr/bin/env python3
from __future__ import annotations

import uvicorn

from workbench.config import Settings


def main() -> int:
    settings = Settings()
    uvicorn.run("workbench.app:app", host=settings.host, port=settings.port, reload=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: Add README instructions**

Append this section to `README.md`:

````markdown

## 本地生成工作台

内部试用可以启动本地网站：

```bash
pip install -r requirements.txt
python scripts/run_workbench.py
```

然后打开：

```text
http://127.0.0.1:8787
```

第一版默认只监听本机地址，不会暴露到公网。页面可以上传 `.wav`、`.mp3`、`.m4a`，填写主题、流量词、模板和文案，然后生成本地 MP4。

如果没有本地转写能力，请先把文案粘贴到页面里。缺少 FFmpeg、HyperFrames 或浏览器预览时，页面会说明缺什么、它有什么用，以及下一步该补什么。
````

- [ ] **Step 3: Run docs smoke check**

Run:

```bash
python scripts/run_workbench.py
```

Expected: Uvicorn starts on `http://127.0.0.1:8787`. Stop it with `Ctrl+C` after confirming startup.

- [ ] **Step 4: Commit**

```bash
git add scripts/run_workbench.py README.md
git commit -m "Document local workbench startup"
```

## Task 9: End-to-End Verification

**Files:**
- No new files expected.

- [ ] **Step 1: Install dependencies**

Run:

```bash
pip install -r requirements.txt
```

Expected: FastAPI, Uvicorn, pytest, httpx, and python-multipart install successfully.

- [ ] **Step 2: Run all tests**

Run:

```bash
pytest -v
```

Expected: all tests pass.

- [ ] **Step 3: Run capability check**

Run:

```bash
python scripts/check_capabilities.py
```

Expected: prints a capability level and explains missing items.

- [ ] **Step 4: Start the workbench**

Run:

```bash
python scripts/run_workbench.py
```

Expected: server listens on `http://127.0.0.1:8787`.

- [ ] **Step 5: Manual browser test**

Open `http://127.0.0.1:8787` and verify:

- The upload form is visible on the first screen.
- Capability status is shown.
- Uploading an unsupported file extension returns a Chinese error.
- Uploading an audio file with blank script reaches `needs_script`.
- Uploading an audio file with script creates a job and starts polling.

- [ ] **Step 6: Real MP4 test when FFmpeg is available**

Use a small local `.wav` or `.mp3` and a short script. Expected:

- Job reaches `completed`.
- Download link appears.
- Downloaded MP4 has audio and video streams.
- `workbench_data/jobs/<job_id>/review/contact.jpg` is created when FFmpeg can extract frames.

- [ ] **Step 7: Commit any verification fixes**

If verification requires small fixes:

```bash
git add <changed-files>
git commit -m "Fix workbench verification issues"
```

## Self-Review

- Spec coverage: The plan covers local UI, FastAPI backend, capability detection, job directory layout, script fallback, task status polling, MP4 output, review evidence, and README usage.
- Intentional first-version limit: The MVP renderer creates a working 9:16 MP4 with audio and basic text. Rich HyperFrames scene templates remain a follow-up because this plan prioritizes a reliable upload-to-download loop first.
- Placeholder scan: No task contains unresolved placeholder markers or undefined follow-up placeholders.
- Type consistency: `JobRecord`, `PipelinePaths`, status names, API route names, and file paths match across tasks.
