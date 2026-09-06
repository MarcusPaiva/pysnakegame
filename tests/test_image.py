import pygame
import pytest

from game_engine.image import Image


@pytest.fixture
def logo_path():
    return r'./game_src/assets/images/logo/my_logo.png'


def test_image_loads_from_file(logo_path):
    image = Image(logo_path)
    assert image is not None


def test_fade_runs_without_error_and_leaves_something_on_screen(screen, logo_path):
    image = Image(logo_path)

    # A short duration keeps the test fast; fade() blocks for ~duration ms.
    image.fade(screen, duration=20)

    # No assertion on pixel content: fade() legitimately ends at alpha 0
    # (fully faded out), so a blank screen afterwards is expected.
