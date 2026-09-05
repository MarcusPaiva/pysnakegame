import pygame

from src.game_engines.game_input import Keyboard, Keys


class _FakePressed(dict):
    def __getitem__(self, key):
        return self.get(key, False)


def test_no_keys_pressed(monkeypatch):
    monkeypatch.setattr(pygame.key, "get_pressed", lambda: _FakePressed())
    keyboard = Keyboard()

    keyboard.detect_buttons()

    assert keyboard.user_is_pressing is False
    assert keyboard.current_keys_pressing == []


def test_detects_arrow_and_escape_keys(monkeypatch):
    pressed = _FakePressed({pygame.K_UP: True, pygame.K_ESCAPE: True})
    monkeypatch.setattr(pygame.key, "get_pressed", lambda: pressed)
    keyboard = Keyboard()

    keyboard.detect_buttons()

    assert keyboard.user_is_pressing is True
    assert Keys.key_up in keyboard.current_keys_pressing
    assert Keys.escape in keyboard.current_keys_pressing
    assert Keys.key_down not in keyboard.current_keys_pressing


def test_state_refreshes_on_each_call(monkeypatch):
    pressed = _FakePressed({pygame.K_RIGHT: True})
    monkeypatch.setattr(pygame.key, "get_pressed", lambda: pressed)
    keyboard = Keyboard()
    keyboard.detect_buttons()
    assert Keys.key_right in keyboard.current_keys_pressing

    pressed.clear()
    keyboard.detect_buttons()
    assert keyboard.current_keys_pressing == []
    assert keyboard.user_is_pressing is False
