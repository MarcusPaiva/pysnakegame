import pytest

from game_engine.inputs.game_input import Keys
from game_src.GameObjects.player import Player


@pytest.fixture
def player(screen, game_bounds):
    p = Player(screen, game_bounds)
    # Bypass real keyboard polling: tests drive movement by setting
    # _last_position directly and calling the private move step.
    p._Player__control_event = lambda: None
    return p


def _move(player):
    player._Player__move()


def test_starts_centered_in_bounds(player, game_bounds):
    assert player.position.center_x == game_bounds.center_x
    assert player.position.center_y == game_bounds.center_y


def test_add_point_increments_score_and_speed(player):
    initial_speed = player._speed
    player.add_point()
    assert player.points == 2
    assert player._speed > initial_speed


def test_wrap_around_right_edge(player, game_bounds):
    player._position.set_position(game_bounds.x1 - 1, 300)
    player._last_position = Keys.right

    _move(player)  # steps past the edge and wraps in the same step

    assert player.position.center_x == pytest.approx(game_bounds.x0 + player.radius)


def test_wrap_around_left_edge(player, game_bounds):
    player._position.set_position(game_bounds.x0 + 1, 300)
    player._last_position = Keys.left

    _move(player)

    assert player.position.center_x == pytest.approx(game_bounds.x1 - player.radius)


def test_wrap_around_top_edge(player, game_bounds):
    player._position.set_position(300, game_bounds.y0 + 1)
    player._last_position = Keys.up

    _move(player)

    assert player.position.center_y == pytest.approx(game_bounds.y1 - player.radius)


def test_wrap_around_bottom_edge(player, game_bounds):
    player._position.set_position(300, game_bounds.y1 - 1)
    player._last_position = Keys.down

    _move(player)

    assert player.position.center_y == pytest.approx(game_bounds.y0 + player.radius)


def test_positions_history_is_capped_at_current_points(player):
    player.points = 3
    for _ in range(10):
        player._last_position = Keys.right
        _move(player)

    assert len(player.positions) <= 3
