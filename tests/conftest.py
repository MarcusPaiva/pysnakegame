import os
import sys
from pathlib import Path

# Run pygame headless: no real window/audio device needed to test logic.
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

# Make "src.*" importable regardless of where pytest is invoked from.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pygame
import pytest


@pytest.fixture(scope="session", autouse=True)
def _pygame_session():
    """Initialize pygame once for the whole test session, headlessly."""
    pygame.init()
    pygame.display.set_mode((1100, 720))
    yield
    pygame.quit()


@pytest.fixture(autouse=True)
def _reset_singletons():
    """
    GameStatus and GameBrief are app-wide singletons. Reset them before and
    after every test so state never leaks between tests.
    """
    from src.game_engines.game_status import GameStatus
    from src.game_engines.game_brief import GameBrief

    GameStatus.reset_instance()
    GameBrief.reset_instance()
    yield
    GameStatus.reset_instance()
    GameBrief.reset_instance()


@pytest.fixture
def screen():
    """The (dummy) game window surface, reused by every test."""
    return pygame.display.get_surface()


@pytest.fixture
def game_bounds():
    """A representative play-area bounding box, matching Stage's own setup."""
    from src.game_engines.bounding_box import RectBoundingBox

    return RectBoundingBox(30, 100, 1070, 690)
