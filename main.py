import math
from datetime import datetime, timedelta

import pygame

from fruit import Fruit
from player import Player

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
player = Player(screen, time_delta=dt)
player.set_point(1)
fruit = Fruit(screen, time_delta=dt)
fruit.generate()

def circle_collision_detections(position1:pygame.Vector2,radius1:int,position2:pygame.Vector2,radius2:int ) -> bool:
    """
    Euclidean Game collision detection
    :param position1: GameObject's vector position.
    :param radius1: GameObject's radius distance.
    :param position2: GameObject's vector position.
    :param radius2: GameObject's radius distance.
    :return: Collision status as boolean.
    """
    distance = math.sqrt(
        (position1.x - position2.x) ** 2 + (position1.y - position2.y) ** 2)
    if distance <= radius1 + radius2:
        return True


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

prev_time = datetime.now()
collision = 0
pause = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("orange")

    tm = datetime.now() - prev_time
    if tm > timedelta(milliseconds=100):
        prev_time = datetime.now()
        if not pause:
            player.move()
    player.update()
    fruit.update()
    fruit.draw()
    player.draw()

    if detect_player_fruit_collision(player, fruit):
        fruit.generate()
        player.add_point()

    if self_collision(player):
        collision += 1
        pause=True
        print(f"Colidiu! {collision}")

    if pause:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pause = False

    pygame.display.flip()
    clock.tick(60)
pygame.quit()