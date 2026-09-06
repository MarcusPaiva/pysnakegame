from game_engine.bounding_box import CircleBoundingBox
from game_engine.game_collision import circle_collision_detections


def test_overlapping_circles_collide():
    pos1 = CircleBoundingBox(0, 0, 0)
    pos2 = CircleBoundingBox(5, 0, 0)
    assert circle_collision_detections(pos1, 10, pos2, 10) is True


def test_distant_circles_do_not_collide():
    pos1 = CircleBoundingBox(0, 0, 0)
    pos2 = CircleBoundingBox(100, 0, 0)
    assert not circle_collision_detections(pos1, 10, pos2, 10)


def test_circles_exactly_touching_collide():
    # distance == radius1 + radius2 should count as a collision (<=).
    pos1 = CircleBoundingBox(0, 0, 0)
    pos2 = CircleBoundingBox(20, 0, 0)
    assert circle_collision_detections(pos1, 10, pos2, 10) is True


def test_circles_just_apart_do_not_collide():
    pos1 = CircleBoundingBox(0, 0, 0)
    pos2 = CircleBoundingBox(20.01, 0, 0)
    assert not circle_collision_detections(pos1, 10, pos2, 10)
