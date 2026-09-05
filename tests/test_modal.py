import pygame
import pytest

from src.game_components.modal import Modal


@pytest.fixture
def small_screen():
    """A throwaway surface, distinct from the shared session screen."""
    return pygame.Surface((800, 500))


def test_bounding_box_is_proportional_to_screen_size(small_screen):
    modal = Modal(small_screen, "Game Over", width_ratio=0.6, height_ratio=0.55)

    box = modal._main_bounding_box
    assert box.size.x == pytest.approx(800 * 0.6)
    assert box.size.y == pytest.approx(500 * 0.55)


def test_bounding_box_is_centered_on_screen(small_screen):
    modal = Modal(small_screen, "Game Over", width_ratio=0.6, height_ratio=0.55)

    box = modal._main_bounding_box
    assert box.center == pygame.Vector2(400, 250)


def test_bounding_box_recomputes_when_screen_changes_size():
    """
    Regression test: the modal used to be a fixed pixel size regardless of
    the window, so it did not scale proportionally with the screen.
    """
    surface = pygame.Surface((800, 500))
    modal = Modal(surface, "Game Over", width_ratio=0.6, height_ratio=0.55)
    small_size = modal._main_bounding_box.size

    bigger_surface = pygame.Surface((1600, 1000))
    modal._screen = bigger_surface
    modal.setup()
    modal.update()

    big_size = modal._main_bounding_box.size
    assert big_size.x == pytest.approx(small_size.x * 2)
    assert big_size.y == pytest.approx(small_size.y * 2)
