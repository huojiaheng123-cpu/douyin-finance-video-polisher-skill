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
