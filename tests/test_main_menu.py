import pytest

from light_game_engine.inputs.game_input import Buttons
from light_game_engine.scene.game_management import GameStatus, SceneManagement
from game_src.screens.main_menu import MainMenu


class _FakeJoystick:
    """A double satisfying just what button_just_pressed() needs."""

    def __init__(self):
        self._just_pressed = set()

    def press_once(self, button):
        self._just_pressed = {button}

    def clear(self):
        self._just_pressed = set()

    def button_just_pressed(self, button):
        return button in self._just_pressed


def test_buttons_are_centered_on_screen_x_axis(screen):
    """
    Regression test: Start Game and Exit used to sit at hardcoded x
    positions (400 and 500), so neither was centered and they didn't
    even line up with each other.
    """
    menu = MainMenu(screen)
    menu.setup()
    menu._process()  # computes each button's bounding box from its position

    screen_center_x = screen.width() / 2
    for button in (menu._start_game_btn, menu._exit_game_game_btn):
        assert button._main_bounding_box.center[0] == pytest.approx(screen_center_x, abs=1.0)


def test_title_is_centered_on_screen_x_axis(screen):
    """Regression test: the title used to be blitted at a hardcoded x=370."""
    menu = MainMenu(screen)
    menu.setup()

    screen_center_x = screen.width() / 2
    title_x, _ = menu._title_position
    title_center_x = title_x + menu._game_title.get_width() / 2

    assert title_center_x == pytest.approx(screen_center_x, abs=1.0)


def test_exit_stops_the_game_via_light_game_engine_status(screen):
    menu = MainMenu(screen)
    menu.setup()

    menu._MainMenu__exit_game()

    assert GameStatus().game_is_running is False


def test_start_game_switches_to_the_game_stage_scene(screen):
    fake_scene = type("FakeScene", (), {"reset": lambda self: None})()
    SceneManagement().add_scene("main_menu", fake_scene)
    SceneManagement().add_scene("game_stage", fake_scene)
    menu = MainMenu(screen)
    menu.setup()

    menu._MainMenu__go_to_game()

    assert SceneManagement().get_current_scene_name == "game_stage"


def test_joystick_dpad_moves_focus_between_buttons(screen):
    joystick = _FakeJoystick()
    menu = MainMenu(screen, joystick)
    menu.setup()
    assert menu._focused_index == 0

    joystick.press_once(Buttons.dpad_down)
    menu._process()
    assert menu._focused_index == 1

    joystick.press_once(Buttons.dpad_up)
    menu._process()
    assert menu._focused_index == 0
