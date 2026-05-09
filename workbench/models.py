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
