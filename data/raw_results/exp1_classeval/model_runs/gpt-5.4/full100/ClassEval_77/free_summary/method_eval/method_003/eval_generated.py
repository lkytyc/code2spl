class Snake:
    def __init__(self, screen_width, screen_height, block_size, food_position):
        import random
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.block_size = block_size
        self.start_position = (screen_width // 2 // block_size * block_size, screen_height // 2 // block_size * block_size)
        self.random = random
        self.initial_food_position = food_position
        self.reset()

    def move(self, direction):
        new_head = (
            (self.snake[0][0] + direction[0] * self.block_size) % self.screen_width,
            (self.snake[0][1] + direction[1] * self.block_size) % self.screen_height,
        )
        self.snake.insert(0, new_head)

        if new_head == self.food_position:
            self.eat_food()
        else:
            self.snake.pop()

        if new_head in self.snake[2:]:
            self.reset()

    def eat_food(self):
        self.length += 1
        self.score += 100
        self.food_position = self.random_food_position()

    def reset(self):
        self.length = 1
        self.score = 0
        self.snake = [self.start_position]
        self.food_position = self.random_food_position()

    def random_food_position(self):
        while True:
            pos = (
                self.random.randrange(0, self.screen_width, self.block_size),
                self.random.randrange(0, self.screen_height, self.block_size),
            )
            if pos not in self.snake:
                return pos

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
