from src.game_engines.game_status import GameStatus
from src.game_engines.screen_game import ScreenGame


def test_default_state():
    status = GameStatus()
    assert status.current_screen == ScreenGame.main_menu
    assert status.game_running is True
    assert status.change_screen_trigger is False


def test_changing_screen_sets_trigger():
    status = GameStatus()
    status.current_screen = ScreenGame.game_stage
    assert status.current_screen == ScreenGame.game_stage
    assert status.change_screen_trigger is True

    status.dismiss_change_screen_trigger()
    assert status.change_screen_trigger is False


def test_close_game_stops_loop():
    status = GameStatus()
    status.close_game()
    assert status.game_running is False


def test_is_a_singleton():
    first = GameStatus()
    second = GameStatus()
    assert first is second


def test_reinstantiating_does_not_reset_existing_state():
    """Regression test: __init__ used to run on every call, wiping state."""
    status = GameStatus()
    status.current_screen = ScreenGame.game_stage
    status.close_game()

    same_status = GameStatus()

    assert same_status.current_screen == ScreenGame.game_stage
    assert same_status.game_running is False


def test_reset_instance_creates_a_fresh_one():
    status = GameStatus()
    status.close_game()

    GameStatus.reset_instance()
    fresh_status = GameStatus()

    assert fresh_status is not status
    assert fresh_status.game_running is True
