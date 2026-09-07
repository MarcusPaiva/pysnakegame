from datetime import datetime, timedelta
from typing import Optional

from game_src.GameObjects.player import Player
from game_src.GameObjects.fruit import Fruit
from light_game_engine.game_objects.modal import Modal, Options
from light_game_engine.bounding_box import RectBoundingBox
from light_game_engine.font import GameFont
from light_game_engine.game_artfacts_2d import Rect
from game_src.game_brief import GameBrief
from light_game_engine.inputs.game_input import Buttons, Joystick, Keyboard, Keys, set_reapeat
from light_game_engine.scene.game_management import SceneManagement
from light_game_engine.scene.game_scene import GameScene
from light_game_engine.screen import SurfaceScreen
from light_game_engine.sound import Music
from game_src.utils.game_storage import GameBriefStorage
from light_game_engine.game_collision import circle_collision_detections


def detect_player_fruit_collision(player:Player, fruit:Fruit) -> bool:
    """
    Player and Fruit collision detection.
    :param player: Players' GameObject.
    :param fruit: Fruit's GameObject.
    :return: Collision status as boolean.
    """
    return circle_collision_detections(player.position, player.radius, fruit.position, fruit.radius)

def self_collision(player:Player) -> bool:
    """
    Self player collision detection.
    :param player: Players' GameObject.
    :return: Collision status as boolean.
    """
    last = player.position
    if len(player.positions) > 1:
        if last in player.positions[:-1]:
            return True
    return False


_FONT_PATH = r'./game_src/assets/fonts/roboto/Roboto-Black.ttf'


class Stage(GameScene):
    def __init__(self, screen:SurfaceScreen, joystick:Optional[Joystick] = None):
        self._screen = screen
        self._joystick = joystick
        self._pause = False
        self._game_bounds = RectBoundingBox(30, 100, self._screen.width() - 30, self._screen.height() - 30)
        self._game_header_bounds = RectBoundingBox(0, 0, self._screen.width(), self._game_bounds.y0 - 25)
        self._player = Player(screen, self._game_bounds, joystick)
        self._fruit = Fruit(screen, self._game_bounds)
        self._modal_game_over = Modal(self._screen, "Game Over")
        self._modal_pause = Modal(self._screen, "Paused")
        self._collision = 0
        self._end_game = False
        self._main_font = GameFont(80, 'Paused').set_font(_FONT_PATH).set_color([255, 255, 255])
        self._paused_text = self._main_font.render()
        self._main_font.set_text(f'Points {self._player.points}')
        self._points_text = self._main_font.render()
        self._last_key_pressed = []
        self._game_brief = GameBrief()
        self._game_storage = GameBriefStorage()
        self._last_save = datetime.now()
        set_reapeat(50,200)
        self._music = Music(r'./game_src/assets/sounds/music/main_song.mp3')
        self._game_keyboard = Keyboard()

    def reset(self):
        self._collision = 0
        self._player = Player(self._screen, self._game_bounds, self._joystick)
        self._fruit.generate()
        self._end_game = False
        self._pause = False

    def __continue_option(self):
        """
        Continue event.
        :return:
        """
        self._pause = False

    def __try_again_option(self):
        self.reset()

    def setup(self) -> None:
        """
        Stage setup.
        """
        self._game_storage.load_brief()
        self._player.points = 1
        self._fruit.generate()
        self._music.play_loop()
        self._music.set_volume(0.3)
        self._modal_game_over.set_font(_FONT_PATH)
        self._modal_game_over.setup()
        self._modal_game_over.show(False)
        self.__setup_modal_game_over_options()
        self._modal_pause.set_font(_FONT_PATH)
        self._modal_pause.setup()
        self._modal_pause.show(False)
        self.__setup_modal_pause_options()

    def __main_menu_option(self):
        self._player = Player(self._screen, self._game_bounds, self._joystick)
        self._fruit = Fruit(self._screen, self._game_bounds)
        SceneManagement().set_current_scene("main_menu")
        SceneManagement().reset_current_scene()

    def __setup_modal_game_over_options(self):
        options = [
            Options("Try again", self.__try_again_option, "green", "#0f5c0f"),
            Options("Main Menu", self.__main_menu_option, "red", "#7a0000"),
        ]
        self._modal_game_over.add_options(options)

    def __setup_modal_pause_options(self):
        options = [
            Options("Continue", self.__continue_option, "green", "#0f5c0f"),
            Options("Main Menu", self.__main_menu_option, "red", "#7a0000"),
        ]
        self._modal_pause.add_options(options)

    def __save_event(self):
        """
        Periodically persist the global brief, at most once a second.
        """
        tm = datetime.now() - self._last_save
        if tm > timedelta(milliseconds=1000):
            self._game_storage.save_brief()
            self._last_save = datetime.now()

    def __draw_score(self):
        """
        Draw score on header.
        :return:
        """
        self._main_font.set_text(f'Points {self._player.points}')
        self._points_text = self._main_font.render()
        self._screen.draw(
            self._points_text,
            (self._game_header_bounds.x0 + 10, self._game_header_bounds.y0)
        )

    def __draw_header(self):
        """
        Draw header.
        """
        header = self._game_header_bounds
        Rect(header.x0, header.y0, header.width, header.height).set_fill_color("#596869").render(self._screen)
        self.__draw_score()

    def __draw_scenario(self):
        """
        Draw scenario.
        """
        Rect(
            0, self._game_bounds.y0 - 25, self._screen.width(), self._screen.height()
        ).set_fill_color("#A41623").render(self._screen)
        Rect(
            self._game_bounds.x0 - 2, self._game_bounds.y0 - 2,
            self._game_bounds.width + 4, self._game_bounds.height + 4
        ).set_fill_color("black").render(self._screen)
        Rect(
            self._game_bounds.x0, self._game_bounds.y0,
            self._game_bounds.width, self._game_bounds.height
        ).set_fill_color("orange").render(self._screen)

    def __user_io_detection(self):
        """
        Main user detection action.
        :return:
        """
        pause_detection = True
        joystick_pause = self._joystick is not None and self._joystick.button_just_pressed(Buttons.start)
        if self._game_keyboard.user_is_pressing:
            keys = self._game_keyboard.get_user_interaction
            if not self._pause and Keys.escape not in self._last_key_pressed and pause_detection:
                if Keys.escape in keys:
                    self._pause = True
                    pause_detection = False
            if self._pause and Keys.escape not in self._last_key_pressed and pause_detection:
                if Keys.escape in keys:
                    self._pause = False
            self._last_key_pressed = keys
        else:
            self._last_key_pressed = []
        if joystick_pause:
            self._pause = not self._pause

    def __in_game(self):
        """
        In game.
        """
        if not self._pause and not self._end_game:
            self._player.update()
            self._fruit.update()
        self._fruit.draw()
        self._player.draw()

        if detect_player_fruit_collision(self._player, self._fruit):
            self._fruit.generate()
            self._player.add_point()

        if self_collision(self._player) and not self._end_game:
            self._game_brief.add_global_points( self._player.points )
            self._game_brief.increment_tries()
            self._collision += 1
            self._pause = True
            self._end_game = True
            print(f"Colidiu! {self._collision}")

    def __pause_menu(self):
        self._modal_pause.show(self._pause)
        self._modal_pause.update(self._joystick)
        self._modal_pause.draw()

    def __game_over_menu(self):
        self._modal_game_over.show(self._end_game)
        self._modal_game_over.update(self._joystick)
        self._modal_game_over.draw()


    def loop(self):
        """
        Main game loop.
        """
        self._game_keyboard.detect_buttons()
        if self._joystick is not None:
            self._joystick.detect_buttons()
        self._screen.fill("orange")
        self.__user_io_detection()
        self.__draw_header()
        self.__draw_scenario()
        self.__in_game()
        self.__pause_menu()
        self.__game_over_menu()
        self.__save_event()
        self._screen.set_clock(60)
