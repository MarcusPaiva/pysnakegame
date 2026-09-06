from enum import Enum

import pygame


class Keys(Enum):
    escape = "escape"
    key_up = "key_up"
    key_down = "key_down"
    key_left = "key_left"
    key_right = "key_right"


class Keyboard:
    def __init__(self):
        self._current_keys_pressed = []
        self._user_is_pressing = False

    def detect_buttons(self):
        self._current_keys_pressed = []
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self._current_keys_pressed.append(Keys.escape)
        if keys[pygame.K_UP]:
            self._current_keys_pressed.append(Keys.key_up)
        if keys[pygame.K_DOWN]:
            self._current_keys_pressed.append(Keys.key_down)
        if keys[pygame.K_LEFT]:
            self._current_keys_pressed.append(Keys.key_left)
        if keys[pygame.K_RIGHT]:
            self._current_keys_pressed.append(Keys.key_right)
        self._user_is_pressing = True if len(self._current_keys_pressed) > 0 else False

    @property
    def user_is_pressing(self):
        return self._user_is_pressing

    @property
    def current_keys_pressing(self):
        return self._current_keys_pressed
