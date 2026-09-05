import pygame

from src.game_engines.bounding_box import RectBoundingBox


def test_initial_and_final_position():
    box = RectBoundingBox(10, 20, 110, 220)
    assert box.initial_position == pygame.Vector2(10, 20)
    assert box.final_position == pygame.Vector2(110, 220)


def test_size():
    box = RectBoundingBox(10, 20, 110, 220)
    assert box.size == pygame.Vector2(100, 200)


def test_center():
    box = RectBoundingBox(0, 0, 100, 200)
    assert box.center == pygame.Vector2(50, 100)


def test_bounds_tuple():
    box = RectBoundingBox(10, 20, 110, 220)
    assert box.bounds == (10, 20, 110, 220)
