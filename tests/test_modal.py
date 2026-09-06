import pytest

from game_engine.screen import SurfaceScreen
from game_src.game_components.modal import Modal, Options


@pytest.fixture
def small_screen():
    """A throwaway 800x500 app screen, distinct from the shared session screen."""
    return SurfaceScreen(800, 500, "Test")


def test_bounding_box_is_proportional_to_screen_size(small_screen):
    modal = Modal(small_screen, "Game Over", width_ratio=0.6, height_ratio=0.55)

    box = modal._main_bounding_box
    assert box.size[0] == pytest.approx(800 * 0.6)
    assert box.size[1] == pytest.approx(500 * 0.55)


def test_bounding_box_is_centered_on_screen(small_screen):
    modal = Modal(small_screen, "Game Over", width_ratio=0.6, height_ratio=0.55)

    box = modal._main_bounding_box
    assert box.center == [400, 250]


def test_bounding_box_recomputes_when_screen_changes_size():
    """
    Regression test: the modal used to be a fixed pixel size regardless of
    the window, so it did not scale proportionally with the screen.
    """
    surface_screen = SurfaceScreen(800, 500, "Test")
    modal = Modal(surface_screen, "Game Over", width_ratio=0.6, height_ratio=0.55)
    small_size = modal._main_bounding_box.size

    bigger_screen = SurfaceScreen(1600, 1000, "Test")
    modal._screen = bigger_screen
    modal.setup()
    modal.update()

    big_size = modal._main_bounding_box.size
    assert big_size[0] == pytest.approx(small_size[0] * 2)
    assert big_size[1] == pytest.approx(small_size[1] * 2)


def test_option_buttons_have_equal_outer_margins(small_screen):
    """
    Regression test: unequal-width buttons (short "Try again" vs longer
    "Main Menu") used to leave a big left margin and almost none on the
    right, because positions were computed from the box's absolute right
    edge instead of the buttons' actual rendered widths.
    """
    modal = Modal(small_screen, "Game Over", width_ratio=0.6, height_ratio=0.55)
    modal.setup()
    modal.add_options([
        Options("Try again", lambda: None, "green", "white"),
        Options("Main Menu", lambda: None, "red", "white"),
    ])

    modal.update()

    box = modal._main_bounding_box
    first_btn, last_btn = modal._options_buttons[0], modal._options_buttons[-1]
    left_margin = first_btn._main_bounding_box.initial_position[0] - box.initial_position[0]
    right_margin = box.final_position[0] - last_btn._main_bounding_box.final_position[0]

    assert left_margin == pytest.approx(right_margin, abs=1.0)
