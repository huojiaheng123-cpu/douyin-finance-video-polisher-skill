from dataclasses import asdict

from workbench.config import Settings
from workbench.job_store import JobStore


def make_store(tmp_path):
    return JobStore(Settings(base_dir=tmp_path))


def test_create_job_creates_pipeline_directories_and_record(tmp_path):
    store = make_store(tmp_path)

    record, paths = store.create_job(
        theme="大盘复盘",
        traffic_word="热点",
        template="standard",
        output_name=" ",
        script="今天聊聊市场",
        original_filename="market.mp3",
    )

    assert record.status == "queued"
    assert record.progress == ["任务已创建"]
    assert record.input_audio == "input/market.mp3"
    assert record.output_name == record.job_id
    assert paths.job_dir.name == record.job_id
    assert paths.input_dir.is_dir()
    assert paths.transcript_dir.is_dir()
    assert paths.plan_dir.is_dir()
    assert paths.render_dir.is_dir()
    assert paths.review_dir.is_dir()
    assert paths.output_dir.is_dir()
    assert (paths.job_dir / "job.json").is_file()


def test_update_job_persists_status_and_progress_entry(tmp_path):
    store = make_store(tmp_path)
    record, _ = store.create_job(
        theme="主题",
        traffic_word="流量词",
        template="standard",
        output_name="成片",
        script="脚本",
        original_filename="audio.wav",
    )

    updated = store.update_job(
        record.job_id,
        status="planning",
        progress_entry="已生成分镜",
    )
    reloaded = store.get_job(record.job_id)

    assert updated.status == "planning"
    assert updated.progress == ["任务已创建", "已生成分镜"]
    assert asdict(reloaded) == asdict(updated)


def test_list_jobs_returns_newest_first(tmp_path):
    store = make_store(tmp_path)
    first, _ = store.create_job("主题1", "词1", "standard", "one", "", "one.mp3")
    second, _ = store.create_job("主题2", "词2", "standard", "two", "", "two.mp3")

    jobs = store.list_jobs()

    assert [job.job_id for job in jobs] == [second.job_id, first.job_id]
