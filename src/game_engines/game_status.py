from src.game_engines.screen_game import ScreenGame


class GameStatus:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(GameStatus, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._current_screen = ScreenGame.main_menu
        self._running = True
        self._change_screen_trigger = False

    def dismiss_change_screen_trigger(self):
        self._change_screen_trigger = False

    @property
    def change_screen_trigger(self):
        return self._change_screen_trigger

    @classmethod
    def reset_instance(cls):
        cls._instance = None

    @property
    def current_screen(self):
        return self._current_screen

    @current_screen.setter
    def current_screen(self, destination_screen:ScreenGame):
        self._change_screen_trigger = True
        self._current_screen = destination_screen

    def close_game(self):
        self._running = False

    @property
    def game_running(self):
        return self._running