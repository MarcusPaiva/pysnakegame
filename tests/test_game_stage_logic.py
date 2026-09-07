from types import SimpleNamespace

from light_game_engine.bounding_box import CircleBoundingBox
from game_src.screens.game_stage import detect_player_fruit_collision, self_collision


def _fake_player(position, positions=None, radius=10):
    return SimpleNamespace(position=position, positions=positions or [position], radius=radius)


def _fake_fruit(position, radius=10):
    return SimpleNamespace(position=position, radius=radius)


def test_detect_player_fruit_collision_when_overlapping():
    player = _fake_player(CircleBoundingBox(50, 50, 10))
    fruit = _fake_fruit(CircleBoundingBox(52, 50, 10))
    assert detect_player_fruit_collision(player, fruit) is True


def test_detect_player_fruit_collision_when_far_apart():
    player = _fake_player(CircleBoundingBox(0, 0, 10))
    fruit = _fake_fruit(CircleBoundingBox(500, 500, 10))
    assert not detect_player_fruit_collision(player, fruit)


def test_self_collision_false_for_single_segment():
    head = CircleBoundingBox(10, 10, 10)
    player = _fake_player(head, positions=[head])
    assert self_collision(player) is False


def test_self_collision_false_when_head_does_not_overlap_body():
    head = CircleBoundingBox(30, 30, 10)
    body = [CircleBoundingBox(10, 10, 10), CircleBoundingBox(20, 20, 10), head]
    player = _fake_player(head, positions=body)
    assert self_collision(player) is False


def test_self_collision_true_when_head_overlaps_body():
    head = CircleBoundingBox(10, 10, 10)
    body = [CircleBoundingBox(10, 10, 10), CircleBoundingBox(20, 20, 10), head]
    player = _fake_player(head, positions=body)
    assert self_collision(player) is True
