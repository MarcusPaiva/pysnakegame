import os
import sys
from pathlib import Path

# Run pygame headless: no real window/audio device needed to test logic.
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

# Make "light_game_engine.*" and "game_src.*" importable regardless of where
# pytest is invoked from.
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
    GameBrief (ours) and GameStatus/SceneManagement (from
    light_game_engine) are app-wide singletons. Reset them before and
    after every test so state never leaks between tests.

    light_game_engine's singletons don't expose a public reset hook, so
    we clear their private _instance class attribute directly - the same
    trick their own __new__ uses to create the singleton in the first
    place.
    """
    from game_src.game_brief import GameBrief
    from light_game_engine.scene.game_management import GameStatus, SceneManagement

    GameBrief.reset_instance()
    GameStatus._instance = None
    SceneManagement._instance = None
    yield
    GameBrief.reset_instance()
    GameStatus._instance = None
    SceneManagement._instance = None


@pytest.fixture
def screen():
    """
    The (dummy) app screen, reused by every test. Constructing a
    SurfaceScreen at the session's own size reuses pygame's single
    display surface rather than creating a new one.
    """
    from light_game_engine.screen import SurfaceScreen

    return SurfaceScreen(1100, 720, "Test")


@pytest.fixture
def game_bounds():
    """A representative play-area bounding box, matching Stage's own setup."""
    from light_game_engine.bounding_box import RectBoundingBox

    return RectBoundingBox(30, 100, 1070, 690)
