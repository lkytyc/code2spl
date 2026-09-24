class Snake:
    def __init__(self, screen_width, screen_height, block_size, food_position):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.block_size = block_size
        self.food_position = food_position
        self.initial_position = (
            (screen_width // block_size // 2) * block_size,
            (screen_height // block_size // 2) * block_size,
        )
        self.reset()

    def move(self, direction):
        head_x, head_y = self.positions[0]
        dx, dy = direction
        new_head = (
            (head_x + dx * self.block_size) % self.screen_width,
            (head_y + dy * self.block_size) % self.screen_height,
        )

        if new_head == self.food_position:
            self.positions.insert(0, new_head)
            self.eat_food()
            return

        body_to_check = self.positions[1:-1]
        if new_head in body_to_check:
            self.reset()
            return

        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def random_food_position(self):
        import random

        while True:
            x = random.randrange(0, self.screen_width, self.block_size)
            y = random.randrange(0, self.screen_height, self.block_size)
            if (x, y) not in self.positions:
                return (x, y)

    def reset(self):
        self.positions = [self.initial_position]
        self.length = 1
        self.score = 0
        self.food_position = self.random_food_position()

    def eat_food(self):
        self.length += 1
        self.score += 100
        self.food_position = self.random_food_position()

import unittest

class SnakeTestEatFood(unittest.TestCase):
    def test_eat_food_1(self):
        snake = Snake(100, 100, 1, (51, 51))
        self.assertEqual(snake.length, 1)
        self.assertEqual(snake.score, 0)
        snake.eat_food()
        self.assertEqual(snake.length, 2)
        self.assertEqual(snake.score, 100)

    def test_eat_food_2(self):
        snake = Snake(100, 100, 1, (51, 51))
        self.assertEqual(snake.length, 1)
        self.assertEqual(snake.score, 0)
        snake.eat_food()
        snake.eat_food()
        self.assertEqual(snake.length, 3)
        self.assertEqual(snake.score, 200)

    def test_eat_food_3(self):
        snake = Snake(100, 100, 1, (51, 51))
        self.assertEqual(snake.length, 1)
        self.assertEqual(snake.score, 0)
        snake.eat_food()
        snake.eat_food()
        snake.eat_food()
        self.assertEqual(snake.length, 4)
        self.assertEqual(snake.score, 300)

    def test_eat_food_4(self):
        snake = Snake(100, 100, 1, (51, 51))
        self.assertEqual(snake.length, 1)
        self.assertEqual(snake.score, 0)
        snake.eat_food()
        snake.eat_food()
        snake.eat_food()
        snake.eat_food()
        self.assertEqual(snake.length, 5)
        self.assertEqual(snake.score, 400)

    def test_eat_food_5(self):
        snake = Snake(100, 100, 1, (51, 51))
        self.assertEqual(snake.length, 1)
        self.assertEqual(snake.score, 0)
        snake.eat_food()
        snake.eat_food()
        snake.eat_food()
        snake.eat_food()
        snake.eat_food()
        self.assertEqual(snake.length, 6)
        self.assertEqual(snake.score, 500)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
