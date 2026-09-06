import pygame

from game_engine.inputs.game_input import Keyboard, Keys, set_reapeat


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


def test_keys_covers_every_pygame_key_constant():
    """Keys should have one member per pygame K_* constant, not a hand-picked few."""
    pygame_key_names = {name for name in dir(pygame) if name.startswith("K_")}
    assert len(pygame_key_names) > 100  # sanity check pygame actually exposes many keys
    for name in pygame_key_names:
        assert Keys(getattr(pygame, name)).value == getattr(pygame, name)


def test_friendly_arrow_aliases_match_their_canonical_member():
    assert Keys.key_up is Keys.up
    assert Keys.key_down is Keys.down
    assert Keys.key_left is Keys.left
    assert Keys.key_right is Keys.right


def test_detects_an_arbitrary_letter_key(monkeypatch):
    pressed = _FakePressed({pygame.K_a: True})
    monkeypatch.setattr(pygame.key, "get_pressed", lambda: pressed)
    keyboard = Keyboard()

    keyboard.detect_buttons()

    assert Keys.a in keyboard.current_keys_pressing


def test_set_reapeat_forwards_to_pygame_key_set_repeat(monkeypatch):
    calls = []
    monkeypatch.setattr(pygame.key, "set_repeat", lambda delay, interval: calls.append((delay, interval)))

    set_reapeat(50, 200)

    assert calls == [(50, 200)]
