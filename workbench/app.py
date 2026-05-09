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
        try:
            record = store.get_job(job_id)
        except FileNotFoundError as exc:
            raise HTTPException(status_code=404, detail="任务不存在。") from exc
        if not record.output_video:
            raise HTTPException(status_code=404, detail="任务还没有生成视频。")
        path = store.paths_for(job_id).job_dir / record.output_video
        if not path.exists():
            raise HTTPException(status_code=404, detail="输出文件不存在。")
        return FileResponse(path, media_type="video/mp4", filename=path.name)

    @app.get("/api/jobs/{job_id}/review")
    def review_job(job_id: str):
        try:
            record = store.get_job(job_id)
        except FileNotFoundError as exc:
            raise HTTPException(status_code=404, detail="任务不存在。") from exc
        return {"job_id": job_id, "review_summary": record.review_summary}

    if settings.static_dir.exists():
        app.mount("/", StaticFiles(directory=settings.static_dir, html=True), name="static")

    return app


app = create_app()
