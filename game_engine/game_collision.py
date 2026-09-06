import math
import pygame


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