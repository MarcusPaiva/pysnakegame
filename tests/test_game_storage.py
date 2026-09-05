from src.game_engines.game_brief import GameBrief
from src.utils import game_storage
from src.utils.game_storage import GameBriefStorage


def _use_temp_brief_file(monkeypatch, tmp_path):
    brief_file = tmp_path / "game_brief.storage"
    monkeypatch.setattr(game_storage, "_GAME_BRIEF_FILE", str(brief_file))
    return brief_file


def test_load_brief_defaults_to_zero_when_file_is_missing(monkeypatch, tmp_path):
    _use_temp_brief_file(monkeypatch, tmp_path)
    storage = GameBriefStorage()

    storage.load_brief()

    assert storage.game_brief.global_points == 0
    assert storage.game_brief.tries == 0


def test_save_then_load_round_trip(monkeypatch, tmp_path):
    _use_temp_brief_file(monkeypatch, tmp_path)
    storage = GameBriefStorage()
    storage.game_brief.global_points = 42
    storage.game_brief.tries = 7

    storage.save_brief()
    storage.game_brief.global_points = 0
    storage.game_brief.tries = 0
    storage.load_brief()

    assert storage.game_brief.global_points == 42
    assert storage.game_brief.tries == 7


def test_save_does_not_truncate_before_load_brief_reads_it(monkeypatch, tmp_path):
    """
    Regression test: file_open() used to open with "w+", truncating the
    file before load_brief() ever got to read it, so saved progress was
    silently lost on every run.
    """
    brief_file = _use_temp_brief_file(monkeypatch, tmp_path)
    writer = GameBriefStorage()
    writer.game_brief.global_points = 123
    writer.game_brief.tries = 4
    writer.save_brief()

    assert brief_file.exists()

    # Simulate a fresh run: a new GameBrief singleton with default state.
    GameBrief.reset_instance()
    reader = GameBriefStorage()
    reader.load_brief()

    assert reader.game_brief.global_points == 123
    assert reader.game_brief.tries == 4
