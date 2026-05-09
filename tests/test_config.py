from workbench.config import Settings


def test_settings_paths_are_based_on_base_dir(tmp_path):
    settings = Settings(base_dir=tmp_path)

    assert settings.jobs_dir == tmp_path / "workbench_data" / "jobs"
    assert settings.static_dir == tmp_path / "workbench" / "static"


def test_settings_default_network_binding():
    settings = Settings()

    assert settings.host == "127.0.0.1"
    assert settings.port == 8787


def test_is_allowed_audio_accepts_supported_extensions_case_insensitively():
    settings = Settings()

    assert settings.is_allowed_audio("voice.WAV") is True
    assert settings.is_allowed_audio("voice.mp3") is True
    assert settings.is_allowed_audio("voice.m4a") is True
    assert settings.is_allowed_audio("voice.exe") is False
