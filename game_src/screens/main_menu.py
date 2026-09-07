from typing import Optional

from light_game_engine.font import GameFont
from light_game_engine.game_objects.button import Button
from light_game_engine.inputs.game_input import Buttons, Joystick
from light_game_engine.scene.game_management import GameStatus, SceneManagement
from light_game_engine.scene.game_scene import GameScene
from light_game_engine.screen import SurfaceScreen


class MainMenu(GameScene):
    def __init__(self, screen: SurfaceScreen, joystick: Optional[Joystick] = None):
        self._screen = screen
        self._joystick = joystick
        self._game_title = None
        self._title_position = (0, 0)
        self._main_font = GameFont(120, 'PySnake').set_font(
            r'./game_src/assets/fonts/roboto/Roboto-Black.ttf'
        ).set_color([255, 255, 255])
        self._start_game_btn = Button(screen, 400, 400, "Start Game", on_click=self.__go_to_game)
        self._exit_game_game_btn = Button(screen, 500, 500, "Exit", on_click=self.__exit_game)
        self._buttons = [self._start_game_btn, self._exit_game_game_btn]
        self._focused_index = 0
        self._game_status = GameStatus()

    def __go_to_game(self):
        SceneManagement().set_current_scene("game_stage")
        SceneManagement().reset_current_scene()

    def __exit_game(self):
        self._game_status.set_game_is_running(False)

    def setup(self):
        self._start_game_btn.set_font(r'./game_src/assets/fonts/roboto/Roboto-Black.ttf')
        self._start_game_btn.hover_color("#596869")
        self._start_game_btn.setup()
        self._exit_game_game_btn.set_font(r'./game_src/assets/fonts/roboto/Roboto-Black.ttf')
        self._exit_game_game_btn.hover_color("red")
        self._exit_game_game_btn.setup()
        self._game_title = self._main_font.render()
        self._title_position = ((self._screen.width() - self._game_title.get_width()) / 2, 150)
        self.__center_button(self._start_game_btn, 400)
        self.__center_button(self._exit_game_game_btn, 500)

    def reset(self) -> None:
        """
        Nothing to reset - the menu has no state that changes after setup().
        """
        pass

    def __center_button(self, button: Button, y: float):
        """
        Reposition a button so its center sits on the screen's X axis.
        :param button: Button to center (must already be set up).
        :param y: Axis y start position to keep.
        """
        width = button.content_size().width
        center_x = self._screen.width() / 2
        button.set_position(center_x - (width / 2) + button.margin, y)

    def __navigate(self):
        if self._joystick is None:
            return
        if self._joystick.button_just_pressed(Buttons.dpad_down):
            self._focused_index = (self._focused_index + 1) % len(self._buttons)
        elif self._joystick.button_just_pressed(Buttons.dpad_up):
            self._focused_index = (self._focused_index - 1) % len(self._buttons)

    def _process(self):
        self.__navigate()
        for index, button in enumerate(self._buttons):
            button.focus(index == self._focused_index)
            button.update(self._joystick)

    def _draw(self):
        self._start_game_btn.draw()
        self._exit_game_game_btn.draw()
        self._screen.draw(
            self._game_title,
            self._title_position
        )

    def loop(self):
        if self._joystick is not None:
            self._joystick.detect_buttons()
        self._screen.fill("orange")
        self._process()
        self._draw()
        self._screen.set_clock(60)
