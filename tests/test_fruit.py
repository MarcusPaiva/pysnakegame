from src.GameObjects.fruit import Fruit


def test_generate_stays_within_bounds_minus_radius(screen, game_bounds):
    fruit = Fruit(screen, game_bounds)

    for _ in range(200):
        fruit.generate()
        x, y = fruit.position.x, fruit.position.y
        assert game_bounds.initial_position.x + fruit.radius <= x <= game_bounds.final_position.x - fruit.radius
        assert game_bounds.initial_position.y + fruit.radius <= y <= game_bounds.final_position.y - fruit.radius
