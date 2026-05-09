import json
from dataclasses import asdict
from datetime import datetime, timezone
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
        now = utc_now()
        job_id = f"{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-{uuid4().hex[:8]}"
        paths = self.paths_for(job_id)

        for directory in (
            paths.input_dir,
            paths.transcript_dir,
            paths.plan_dir,
            paths.render_dir,
            paths.review_dir,
            paths.output_dir,
        ):
            directory.mkdir(parents=True, exist_ok=True)

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
            progress=["任务已创建"],
            input_audio=f"input/{original_filename}",
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
        job_file = self.paths_for(job_id).job_dir / "job.json"
        data = json.loads(job_file.read_text(encoding="utf-8"))
        return JobRecord(**data)

    def save_job(self, record: JobRecord) -> None:
        paths = self.paths_for(record.job_id)
        paths.job_dir.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(asdict(record), ensure_ascii=False, indent=2)
        (paths.job_dir / "job.json").write_text(payload, encoding="utf-8")

    def update_job(
        self,
        job_id: str,
        status: JobStatus | None = None,
        progress_entry: str | None = None,
        error: str | None = None,
        output_video: str | None = None,
        review_summary: dict[str, object] | None = None,
    ) -> JobRecord:
        record = self.get_job(job_id)
        if status is not None:
            record.status = status
        if progress_entry is not None:
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
        jobs_dir = self.settings.jobs_dir
        if not jobs_dir.exists():
            return []

        records = []
        for job_file in jobs_dir.glob("*/job.json"):
            records.append(self.get_job(job_file.parent.name))
        return sorted(records, key=lambda record: record.created_at, reverse=True)
