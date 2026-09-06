from game_src.GameObjects.fruit import Fruit


def test_generate_stays_within_bounds_minus_radius(screen, game_bounds):
    fruit = Fruit(screen, game_bounds)

    for _ in range(200):
        fruit.generate()
        x, y = fruit.position.center_x, fruit.position.center_y
        assert game_bounds.x0 + fruit.radius <= x <= game_bounds.x1 - fruit.radius
        assert game_bounds.y0 + fruit.radius <= y <= game_bounds.y1 - fruit.radius
