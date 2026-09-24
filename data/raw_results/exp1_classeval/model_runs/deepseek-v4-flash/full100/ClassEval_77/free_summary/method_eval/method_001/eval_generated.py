import random

class Snake:
    def __init__(self, screen_width, screen_height, block_size):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.block_size = block_size
        self.center_x = screen_width // 2 // block_size * block_size
        self.center_y = screen_height // 2 // block_size * block_size
        self.body = [(self.center_x, self.center_y)]
        self.length = 1
        self.score = 0
        self.direction = (block_size, 0)  # moving right initially
        self.food = self.random_food_position()
        self.grow_flag = False

    def move(self):
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head_x = (head_x + dx) % self.screen_width
        new_head_y = (head_y + dy) % self.screen_height
        new_head = (new_head_x, new_head_y)

        # Check food collision
        if new_head == self.food:
            self.body.insert(0, new_head)
            self.length += 1
            self.score += 100
            self.food = self.random_food_position()
            self.grow_flag = True
        else:
            # Check self collision (excluding head and neck)
            if new_head in self.body[1:]:
                # Reset game
                self.body = [(self.center_x, self.center_y)]
                self.length = 1
                self.score = 0
                self.direction = (self.block_size, 0)
                self.food = self.random_food_position()
                self.grow_flag = False
                return
            self.body.insert(0, new_head)
            if not self.grow_flag:
                self.body.pop()
            else:
                self.grow_flag = False

    def random_food_position(self):
        while True:
            x = random.randrange(0, self.screen_width, self.block_size)
            y = random.randrange(0, self.screen_height, self.block_size)
            if (x, y) not in self.body:
                return (x, y)

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
