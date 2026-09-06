import pytest

from game_engine.font import GameFont

_FONT_PATH = r'./game_src/assets/fonts/roboto/Roboto-Black.ttf'


def test_render_returns_a_surface_with_the_text_rendered():
    font = GameFont(_FONT_PATH, 40, "Test").set_color([255, 255, 255])

    surface = font.render()

    assert surface is not None
    assert surface.get_size() == font.get_text_size()


def test_get_text_size_matches_current_text():
    font = GameFont(_FONT_PATH, 40, "A")
    short_size = font.get_text_size()

    font.set_text("A much longer piece of text")
    long_size = font.get_text_size()

    assert long_size[0] > short_size[0]


def test_set_text_changes_what_render_draws():
    font = GameFont(_FONT_PATH, 40, "AAAA").set_color([255, 255, 255])
    first = font.render()

    font.set_text("AAAA AAAA AAAA")
    second = font.render()

    assert second.get_width() > first.get_width()


def test_setters_return_self_for_chaining():
    font = GameFont(_FONT_PATH, 40, "Test")

    result = font.set_color([1, 2, 3]).enable_anti_alias(True).set_background_color(None).set_text("Chained")

    assert result is font
