from dataclasses import dataclass, field
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Settings:
    base_dir: Path = REPO_ROOT
    host: str = "127.0.0.1"
    port: int = 8787
    max_upload_bytes: int = 200 * 1024 * 1024
    allowed_audio_extensions: frozenset[str] = field(
        default_factory=lambda: frozenset({".wav", ".mp3", ".m4a"})
    )

    @property
    def jobs_dir(self) -> Path:
        return self.base_dir / "workbench_data" / "jobs"

    @property
    def static_dir(self) -> Path:
        return self.base_dir / "workbench" / "static"

    def is_allowed_audio(self, filename: str) -> bool:
        return Path(filename).suffix.lower() in self.allowed_audio_extensions
