import pytest

from game_engine.bounding_box import CircleBoundingBox, RectBoundingBox


def test_initial_and_final_position():
    box = RectBoundingBox(10, 20, 110, 220)
    assert box.initial_position == [10, 20]
    assert box.final_position == [110, 220]


def test_size():
    box = RectBoundingBox(10, 20, 110, 220)
    assert box.size == [100, 200]


def test_center():
    box = RectBoundingBox(0, 0, 100, 200)
    assert box.center == [50, 100]


def test_bounds_tuple():
    box = RectBoundingBox(10, 20, 110, 220)
    assert box.bounds == (10, 20, 110, 220)


def test_rect_plain_number_accessors():
    box = RectBoundingBox(10, 20, 110, 220)
    assert (box.x0, box.y0, box.x1, box.y1) == (10, 20, 110, 220)
    assert (box.width, box.height) == (100, 200)
    assert (box.center_x, box.center_y) == (60, 120)


def test_rect_copy_is_independent():
    box = RectBoundingBox(10, 20, 110, 220)
    copy = box.copy()

    assert copy is not box
    assert (copy.x0, copy.y0, copy.x1, copy.y1) == (box.x0, box.y0, box.x1, box.y1)


def test_circle_plain_number_accessors():
    circle = CircleBoundingBox(50, 60, 10)
    assert (circle.center_x, circle.center_y) == (50, 60)
    assert (circle.x0, circle.y0, circle.x1, circle.y1) == (40, 50, 60, 70)
    assert (circle.width, circle.height) == (20, 20)


def test_circle_pair_accessors_are_plain_lists():
    circle = CircleBoundingBox(50, 60, 10)
    assert circle.center == [50, 60]
    assert circle.initial_position == [40, 50]
    assert circle.final_position == [60, 70]
    assert circle.size == [20, 20]


def test_circle_set_position_moves_to_an_absolute_point():
    circle = CircleBoundingBox(0, 0, 10)
    circle.set_position(100, 200)
    assert (circle.center_x, circle.center_y) == (100, 200)


def test_circle_move_by_shifts_relatively():
    circle = CircleBoundingBox(10, 10, 5)
    circle.move_by(-3, 4)
    assert (circle.center_x, circle.center_y) == (7, 14)


def test_circle_copy_is_independent():
    circle = CircleBoundingBox(10, 10, 5)
    copy = circle.copy()
    copy.move_by(100, 100)

    assert (circle.center_x, circle.center_y) == (10, 10)
    assert (copy.center_x, copy.center_y) == (110, 110)


def test_circle_equality_is_by_value():
    assert CircleBoundingBox(1, 2, 3) == CircleBoundingBox(1, 2, 3)
    assert CircleBoundingBox(1, 2, 3) != CircleBoundingBox(9, 2, 3)


def test_circle_membership_check_works_like_player_self_collision():
    history = [CircleBoundingBox(0, 0, 5), CircleBoundingBox(10, 10, 5)]
    assert CircleBoundingBox(0, 0, 5) in history
    assert CircleBoundingBox(99, 99, 5) not in history
