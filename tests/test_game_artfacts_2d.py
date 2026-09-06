import pygame
import pytest

from game_engine.game_artfacts_2d import Circle, Rect


def test_rect_renders_at_the_requested_position_and_size(screen):
    drawn = Rect(10, 20, 100, 50).set_fill_color("blue").render(screen)

    assert (drawn.x, drawn.y, drawn.w, drawn.h) == (10, 20, 100, 50)


def test_rect_set_fill_color_returns_self_for_chaining():
    rect = Rect(0, 0, 10, 10)

    assert rect.set_fill_color("red") is rect


def test_rect_actually_paints_the_pixel_with_the_fill_color(screen):
    Rect(5, 5, 20, 20).set_fill_color((10, 20, 30)).render(screen)

    assert screen.get_screen().get_at((15, 15))[:3] == (10, 20, 30)


def test_circle_renders_centered_with_the_requested_radius(screen):
    drawn = Circle(50, 60, 15).set_fill_color("green").render(screen)

    assert (drawn.x, drawn.y, drawn.w, drawn.h) == (35, 45, 30, 30)


def test_circle_set_fill_color_returns_self_for_chaining():
    circle = Circle(0, 0, 10)

    assert circle.set_fill_color("red") is circle


def test_circle_actually_paints_the_center_pixel_with_the_fill_color(screen):
    Circle(60, 60, 15).set_fill_color((40, 50, 60)).render(screen)

    assert screen.get_screen().get_at((60, 60))[:3] == (40, 50, 60)
