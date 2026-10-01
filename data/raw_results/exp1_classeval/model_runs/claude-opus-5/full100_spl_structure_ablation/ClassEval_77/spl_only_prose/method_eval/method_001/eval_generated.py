import random

class Snake:
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, BLOCK_SIZE, food_position):
        self.length = 1
        self.score = 0
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.BLOCK_SIZE = BLOCK_SIZE
        self.positions = [(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)]
        self.food_position = food_position

    def eat_food(self):
        self.length += 1
        self.score += 100
        self.random_food_position()

    def move(self, direction):
        cur = self.positions[0]
        x, y = direction
        new = (
            (cur[0] + x * self.BLOCK_SIZE) % self.SCREEN_WIDTH,
            (cur[1] + y * self.BLOCK_SIZE) % self.SCREEN_HEIGHT,
        )
        if new == self.food_position:
            self.eat_food()
        collision = len(self.positions) > 2 and new in self.positions[2:]
        if collision:
            self.reset()
            return
        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()

    def random_food_position(self):
        while self.food_position in self.positions:
            candidate_x = random.randint(0, self.SCREEN_WIDTH // self.BLOCK_SIZE - 1) * self.BLOCK_SIZE
            candidate_y = random.randint(0, self.SCREEN_HEIGHT // self.BLOCK_SIZE - 1) * self.BLOCK_SIZE
            self.food_position = (candidate_x, candidate_y)

    def reset(self):
        self.length = 1
        self.positions = [(self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2)]
        self.score = 0
        self.random_food_position()

import unittest

class SnakeTestRandomFoodPosition(unittest.TestCase):
    def test_random_food_position_1(self):
        snake = Snake(100, 100, 1, (51, 51))
        self.assertEqual(snake.food_position, (51, 51))
        snake.random_food_position()
        self.assertNotIn(snake.food_position, snake.positions)
        self.assertGreaterEqual(snake.food_position[0], 0)
        self.assertGreaterEqual(snake.food_position[1], 0)
        self.assertLessEqual(snake.food_position[0], 100)
        self.assertLessEqual(snake.food_position[1], 100)

    def test_random_food_position_2(self):
        snake = Snake(100, 100, 1, (99, 99))
        self.assertEqual(snake.food_position, (99, 99))
        snake.random_food_position()
        self.assertNotIn(snake.food_position, snake.positions)
        self.assertGreaterEqual(snake.food_position[0], 0)
        self.assertGreaterEqual(snake.food_position[1], 0)
        self.assertLessEqual(snake.food_position[0], 100)
        self.assertLessEqual(snake.food_position[1], 100)

    def test_random_food_position_3(self):
        snake = Snake(100, 100, 1, (0, 0))
        self.assertEqual(snake.food_position, (0, 0))
        snake.random_food_position()
        self.assertNotIn(snake.food_position, snake.positions)
        self.assertGreaterEqual(snake.food_position[0], 0)
        self.assertGreaterEqual(snake.food_position[1], 0)
        self.assertLessEqual(snake.food_position[0], 100)
        self.assertLessEqual(snake.food_position[1], 100)

    def test_random_food_position_4(self):
        snake = Snake(100, 100, 1, (40, 40))
        self.assertEqual(snake.food_position, (40, 40))
        snake.random_food_position()
        self.assertNotIn(snake.food_position, snake.positions)
        self.assertGreaterEqual(snake.food_position[0], 0)
        self.assertGreaterEqual(snake.food_position[1], 0)
        self.assertLessEqual(snake.food_position[0], 100)
        self.assertLessEqual(snake.food_position[1], 100)

    def test_random_food_position_5(self):
        snake = Snake(100, 100, 1, (60, 60))
        self.assertEqual(snake.food_position, (60, 60))
        snake.random_food_position()
        self.assertNotIn(snake.food_position, snake.positions)
        self.assertGreaterEqual(snake.food_position[0], 0)
        self.assertGreaterEqual(snake.food_position[1], 0)
        self.assertLessEqual(snake.food_position[0], 100)
        self.assertLessEqual(snake.food_position[1], 100)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
