import pygame

from game_engine.screen import SurfaceScreen


def test_width_and_height_match_the_requested_size():
    screen = SurfaceScreen(320, 240, "Test")
    assert screen.width() == 320
    assert screen.height() == 240


def test_fill_paints_every_pixel_with_the_color():
    screen = SurfaceScreen(320, 240, "Test")
    screen.fill((10, 20, 30))
    assert screen.get_screen().get_at((5, 5))[:3] == (10, 20, 30)


def test_draw_blits_an_artifact_at_the_given_position():
    screen = SurfaceScreen(320, 240, "Test")
    screen.fill((0, 0, 0))
    artifact = pygame.Surface((10, 10))
    artifact.fill((200, 100, 50))

    screen.draw(artifact, (20, 20))

    assert screen.get_screen().get_at((25, 25))[:3] == (200, 100, 50)


def test_fill_and_draw_return_self_for_chaining():
    screen = SurfaceScreen(320, 240, "Test")
    artifact = pygame.Surface((5, 5))

    assert screen.fill("red") is screen
    assert screen.draw(artifact, (0, 0)) is screen


def test_flip_and_set_clock_do_not_raise():
    screen = SurfaceScreen(320, 240, "Test")
    assert screen.flip() is screen
    assert screen.set_clock(60) is screen


def test_get_screen_returns_the_underlying_pygame_surface():
    screen = SurfaceScreen(320, 240, "Test")
    assert isinstance(screen.get_screen(), pygame.Surface)
