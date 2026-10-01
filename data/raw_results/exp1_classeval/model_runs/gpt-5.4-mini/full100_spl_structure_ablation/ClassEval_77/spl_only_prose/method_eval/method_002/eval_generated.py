class Snake:
    def __init__(self, SCREEN_WIDTH: number, SCREEN_HEIGHT: number, BLOCK_SIZE: number, food_position: any):
        self.length = 1
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.BLOCK_SIZE = BLOCK_SIZE
        self.positions = [(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)]
        self.score = 0
        self.food_position = food_position

    def eat_food(self):
        self.length += 1
        self.score += 100
        self.random_food_position()

    def move(self, direction: tuple[int, int]) -> None:
        cur = self.positions[0]
        x, y = direction
        new = (
            (cur[0] + x * self.BLOCK_SIZE) % self.SCREEN_WIDTH,
            (cur[1] + y * self.BLOCK_SIZE) % self.SCREEN_HEIGHT,
        )

        if new == self.food_position:
            self.eat_food()

        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
            return

        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()

    def random_food_position(self):
        while self.food_position in self.positions:
            self.food_position = (
                random.randint(0, self.SCREEN_WIDTH // self.BLOCK_SIZE - 1) * self.BLOCK_SIZE,
                random.randint(0, self.SCREEN_HEIGHT // self.BLOCK_SIZE - 1) * self.BLOCK_SIZE,
            )

    def reset(self):
        self.length = 1
        self.positions = [(self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2)]
        self.score = 0
        self.random_food_position()

import unittest

class SnakeTestReset(unittest.TestCase):
    def test_reset_1(self):
        snake = Snake(100, 100, 1, (51, 51))
        snake.move((1, 1))
        snake.reset()
        self.assertEqual(snake.length, 1)
        self.assertEqual(snake.positions[0], (50, 50))
        self.assertEqual(snake.score, 0)

    def test_reset_2(self):
        snake = Snake(100, 100, 1, (51, 51))
        snake.move((0, 1))
        snake.reset()
        self.assertEqual(snake.length, 1)
        self.assertEqual(snake.positions[0], (50, 50))
        self.assertEqual(snake.score, 0)

    def test_reset_3(self):
        snake = Snake(100, 100, 1, (51, 51))
        snake.move((0, -1))
        snake.reset()
        self.assertEqual(snake.length, 1)
        self.assertEqual(snake.positions[0], (50, 50))
        self.assertEqual(snake.score, 0)

    def test_reset_4(self):
        snake = Snake(100, 100, 1, (51, 51))
        snake.move((-1, 0))
        snake.reset()
        self.assertEqual(snake.length, 1)
        self.assertEqual(snake.positions[0], (50, 50))
        self.assertEqual(snake.score, 0)

    def test_reset_5(self):
        snake = Snake(100, 100, 1, (51, 51))
        snake.move((1, 0))
        snake.reset()
        self.assertEqual(snake.length, 1)
        self.assertEqual(snake.positions[0], (50, 50))
        self.assertEqual(snake.score, 0)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
