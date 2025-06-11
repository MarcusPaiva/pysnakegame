from datetime import datetime, timedelta

import pygame
from pygame import Surface, SurfaceType

from src.GameObjects.player import Player
from src.GameObjects.fruit import Fruit
from src.utils.game_collision import circle_collision_detections


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
        for idx, pos in enumerate(player.positions[:-1]):
            return circle_collision_detections(pos, player.radius, last, player.radius)


class Stage:
    def __init__(self, screen:Surface | SurfaceType):
        self._screen = screen
        self._pause = False
        self._clock = pygame.time.Clock()
        self._running = True
        self._player = Player(screen)
        self._fruit = Fruit(screen)
        self._collision = 0
        self._prev_time = datetime.now()

    def setup(self) -> None:
        """
        Stage setup.
        """
        self._player.set_point(1)
        self._fruit.generate()


    def loop(self):
        """
        Main game loop.
        """
        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
            self._screen.fill("orange")

            tm = datetime.now() - self._prev_time
            if tm > timedelta(milliseconds=100):
                self._prev_time = datetime.now()
                if not self._pause:
                    self._player.move()
            self._player.update()
            self._fruit.update()
            self._fruit.draw()
            self._player.draw()

            if detect_player_fruit_collision(self._player, self._fruit):
                self._fruit.generate()
                self._player.add_point()

            if self_collision(self._player):
                self._collision += 1
                self._pause = True
                print(f"Colidiu! {self._collision}")

            if self._pause:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    self._pause = False
            else:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    self._pause = True

            pygame.display.flip()
            self._clock.tick(60)