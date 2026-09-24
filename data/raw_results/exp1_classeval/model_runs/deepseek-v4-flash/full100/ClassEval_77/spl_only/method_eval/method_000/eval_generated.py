import random

class Snake:
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, BLOCK_SIZE, food_position):
        self.length = 1
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.BLOCK_SIZE = BLOCK_SIZE
        self.positions = [(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)]
        self.score = 0
        self.food_position = food_position

    def move(self, direction):
        cur = self.positions[0]
        x, y = direction
        new_x = (cur[0] + x * self.BLOCK_SIZE) % self.SCREEN_WIDTH
        new_y = (cur[1] + y * self.BLOCK_SIZE) % self.SCREEN_HEIGHT
        new = (new_x, new_y)
        if new == self.food_position:
            self.eat_food()
        collision_occurred = len(self.positions) > 2 and new in self.positions[2:]
        if collision_occurred:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def random_food_position(self):
        while self.food_position in self.positions:
            new_x = random.randint(0, self.SCREEN_WIDTH // self.BLOCK_SIZE - 1) * self.BLOCK_SIZE
            new_y = random.randint(0, self.SCREEN_HEIGHT // self.BLOCK_SIZE - 1) * self.BLOCK_SIZE
            self.food_position = (new_x, new_y)

    def reset(self):
        self.length = 1
        self.positions = [(self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2)]
        self.score = 0
        self.random_food_position()

    def eat_food(self):
        self.length += 1
        self.score += 100
        self.random_food_position()

import unittest

class SnakeTestMove(unittest.TestCase):
    def test_move_1(self):
        snake = Snake(100, 100, 1, (51, 51))
        snake.move((1, 1))
        self.assertEqual(snake.length, 2)
        self.assertEqual(snake.positions[0], (51, 51))
        self.assertEqual(snake.positions[1], (50, 50))
        self.assertEqual(snake.score, 100)

    def test_move_2(self):
        snake = Snake(100, 100, 1, (80, 80))
        snake.move((1, 1))
        self.assertEqual(snake.length, 1)
        self.assertEqual(snake.positions[0], (51, 51))
        self.assertEqual(snake.score, 0)

    def test_move_3(self):
        snake = Snake(100, 100, 1, (51, 51))
        snake.move((1, 0))
        self.assertEqual(snake.length, 1)
        self.assertEqual(snake.positions[0], (51, 50))
        self.assertEqual(snake.score, 0)

    def test_move_4(self):
        snake = Snake(100, 100, 1, (51, 51))
        snake.move((0, 0))
        self.assertEqual(snake.length, 1)
        self.assertEqual(snake.positions[0], (50, 50))
        self.assertEqual(snake.score, 0)

    def test_move_5(self):
        snake = Snake(100, 100, 1, (99, 99))
        snake.move((1, 0))
        self.assertEqual(snake.length, 1)
        self.assertEqual(snake.positions[0], (51, 50))
        self.assertEqual(snake.score, 0)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
