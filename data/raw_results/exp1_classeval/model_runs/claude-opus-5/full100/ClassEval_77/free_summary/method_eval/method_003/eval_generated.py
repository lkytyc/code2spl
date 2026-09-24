import random


class Snake:
    def __init__(self, screen_width, screen_height, block_size, food_position):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.block_size = block_size
        self.length = 1
        self.score = 0
        self.food_position = food_position

        # Center the snake on screen, aligned to the grid
        start_x = (screen_width // 2 // block_size) * block_size
        start_y = (screen_height // 2 // block_size) * block_size
        self.positions = [(start_x, start_y)]

    def move(self, direction):
        head_x, head_y = self.positions[0]
        dx, dy = direction

        new_x = (head_x + dx * self.block_size) % self.screen_width
        new_y = (head_y + dy * self.block_size) % self.screen_height
        new_head = (new_x, new_y)

        if new_head == self.food_position:
            self.eat_food()
        elif new_head in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new_head)
            if len(self.positions) > self.length:
                self.positions = self.positions[:self.length]

    def eat_food(self):
        self.length += 1
        self.score += 100
        self.positions.insert(0, self.food_position)
        self.random_food_position()

    def random_food_position(self):
        while True:
            x = random.randrange(0, self.screen_width, self.block_size)
            y = random.randrange(0, self.screen_height, self.block_size)
            candidate = (x, y)
            if candidate not in self.positions:
                self.food_position = candidate
                break

    def reset(self):
        self.length = 1
        self.score = 0
        start_x = (self.screen_width // 2 // self.block_size) * self.block_size
        start_y = (self.screen_height // 2 // self.block_size) * self.block_size
        self.positions = [(start_x, start_y)]
        self.random_food_position()

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
