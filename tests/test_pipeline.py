from workbench.models import JobRecord
from workbench.pipeline import build_scene_plan, needs_script, normalize_output_name


def make_job(script="今天聊AI炒股。先看风险？最后给出操作纪律！"):
    return JobRecord(
        job_id="job-1",
        status="queued",
        created_at="2026-05-09T00:00:00+00:00",
        updated_at="2026-05-09T00:00:00+00:00",
        theme="AI炒股",
        traffic_word="热点",
        template="standard",
        output_name="成片",
        script=script,
    )


def test_needs_script_is_true_for_empty_script_and_false_for_non_empty_script():
    assert needs_script(make_job(script="")) is True
    assert needs_script(make_job(script="   ")) is True
    assert needs_script(make_job(script="有文案")) is False


def test_build_scene_plan_covers_duration_with_headlines():
    scenes = build_scene_plan(make_job(), duration_seconds=45)

    assert 3 <= len(scenes) <= 7
    assert scenes[0].start == 0
    assert scenes[-1].end == 45
    assert all(scene.headline for scene in scenes)
    assert all(isinstance(scene.support, list) for scene in scenes)


def test_normalize_output_name_replaces_bad_filename_chars_and_adds_mp4_suffix():
    assert normalize_output_name("AI:炒股?") == "AI_炒股.mp4"
    assert normalize_output_name("成片.mp4") == "成片.mp4"
