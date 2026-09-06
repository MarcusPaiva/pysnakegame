from game_engine.game_brief import GameBrief


def test_default_state():
    brief = GameBrief()
    assert brief.global_points == 0
    assert brief.tries == 0


def test_add_global_points_accumulates():
    brief = GameBrief()
    brief.add_global_points(10)
    brief.add_global_points(5)
    assert brief.global_points == 15


def test_increment_tries():
    brief = GameBrief()
    brief.increment_tries()
    brief.increment_tries()
    assert brief.tries == 2


def test_is_a_singleton():
    first = GameBrief()
    second = GameBrief()
    assert first is second


def test_reinstantiating_does_not_reset_existing_state():
    """Regression test: __init__ used to run on every call, wiping progress."""
    brief = GameBrief()
    brief.global_points = 42
    brief.tries = 7

    same_brief = GameBrief()

    assert same_brief.global_points == 42
    assert same_brief.tries == 7


def test_reset_instance_creates_a_fresh_one():
    brief = GameBrief()
    brief.global_points = 99

    GameBrief.reset_instance()
    fresh_brief = GameBrief()

    assert fresh_brief is not brief
    assert fresh_brief.global_points == 0
