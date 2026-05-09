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
