import math

from game_engine.bounding_box import BoundingBox


def circle_collision_detections(position1:BoundingBox,radius1:int,position2:BoundingBox,radius2:int ) -> bool:
    """
    Euclidean Game collision detection
    :param position1: GameObject's bounding box position.
    :param radius1: GameObject's radius distance.
    :param position2: GameObject's bounding box position.
    :param radius2: GameObject's radius distance.
    :return: Collision status as boolean.
    """
    distance = math.sqrt(
        (position1.center_x - position2.center_x) ** 2 + (position1.center_y - position2.center_y) ** 2)
    if distance <= radius1 + radius2:
        return True
    return False