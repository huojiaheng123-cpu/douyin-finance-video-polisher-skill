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
