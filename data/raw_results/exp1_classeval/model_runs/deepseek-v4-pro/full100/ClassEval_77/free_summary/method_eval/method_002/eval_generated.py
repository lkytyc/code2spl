class Snake:
    def __init__(self, screen_width, screen_height, block_size, food_position):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.block_size = block_size
        self.food_position = food_position
        self.reset()

    def move(self, direction):
        dx, dy = direction
        head_x, head_y = self.body[0]
        new_head = (
            (head_x + dx * self.block_size) % self.screen_width,
            (head_y + dy * self.block_size) % self.screen_height
        )

        if new_head == self.food_position:
            self.eat_food()
            self.body.insert(0, new_head)
        else:
            if new_head in self.body[2:]:
                self.reset()
                return
            self.body.insert(0, new_head)
            if len(self.body) > self.length:
                self.body.pop()

    def random_food_position(self):
        import random
        while True:
            x = random.randrange(0, self.screen_width, self.block_size)
            y = random.randrange(0, self.screen_height, self.block_size)
            if (x, y) not in self.body:
                return (x, y)

    def reset(self):
        center_x = (self.screen_width // 2) // self.block_size * self.block_size
        center_y = (self.screen_height // 2) // self.block_size * self.block_size
        self.body = [(center_x, center_y)]
        self.length = 1
        self.score = 0
        self.food_position = self.random_food_position()

    def eat_food(self):
        self.length += 1
        self.score += 100
        self.food_position = self.random_food_position()

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
