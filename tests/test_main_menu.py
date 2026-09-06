import pytest

from game_src.screens.main_menu import MainMenu


def test_buttons_are_centered_on_screen_x_axis(screen):
    """
    Regression test: Start Game and Exit used to sit at hardcoded x
    positions (400 and 500), so neither was centered and they didn't
    even line up with each other.
    """
    menu = MainMenu(screen)
    menu.setup()
    menu._process()  # computes each button's bounding box from its position

    screen_center_x = screen.get_width() / 2
    for button in (menu._start_game_btn, menu._exit_game_game_btn):
        assert button._main_bounding_box.center[0] == pytest.approx(screen_center_x, abs=1.0)


def test_title_is_centered_on_screen_x_axis(screen):
    """Regression test: the title used to be blitted at a hardcoded x=370."""
    menu = MainMenu(screen)
    menu.setup()

    screen_center_x = screen.get_width() / 2
    title_x, _ = menu._title_position
    title_center_x = title_x + menu._game_title.get_width() / 2

    assert title_center_x == pytest.approx(screen_center_x, abs=1.0)
