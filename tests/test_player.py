import pygame
import pytest

from src.GameObjects.player import Player


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
    assert player.position == game_bounds.center


def test_add_point_increments_score_and_speed(player):
    initial_speed = player._speed
    player.add_point()
    assert player.points == 2
    assert player._speed > initial_speed


def test_wrap_around_right_edge(player, game_bounds):
    player._player_pos.x = game_bounds.final_position.x - 1
    player._player_pos.y = 300
    player._last_position = pygame.K_d

    _move(player)  # steps past the edge and wraps in the same step

    assert player.position.x == pytest.approx(game_bounds.initial_position.x + player.radius)


def test_wrap_around_left_edge(player, game_bounds):
    player._player_pos.x = game_bounds.initial_position.x + 1
    player._player_pos.y = 300
    player._last_position = pygame.K_a

    _move(player)

    assert player.position.x == pytest.approx(game_bounds.final_position.x - player.radius)


def test_wrap_around_top_edge(player, game_bounds):
    player._player_pos.y = game_bounds.initial_position.y + 1
    player._player_pos.x = 300
    player._last_position = pygame.K_w

    _move(player)

    assert player.position.y == pytest.approx(game_bounds.final_position.y - player.radius)


def test_wrap_around_bottom_edge(player, game_bounds):
    player._player_pos.y = game_bounds.final_position.y - 1
    player._player_pos.x = 300
    player._last_position = pygame.K_s

    _move(player)

    assert player.position.y == pytest.approx(game_bounds.initial_position.y + player.radius)


def test_positions_history_is_capped_at_current_points(player):
    player.points = 3
    for _ in range(10):
        player._last_position = pygame.K_d
        _move(player)

    assert len(player.positions) <= 3
