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


class SnakeTest(unittest.TestCase):
    def test_snake(self):
        snake = Snake(100, 100, 1, (51, 51))
        self.assertEqual(snake.length, 1)
        self.assertEqual(snake.SCREEN_WIDTH, 100)
        self.assertEqual(snake.SCREEN_HEIGHT, 100)
        self.assertEqual(snake.BLOCK_SIZE, 1)
        self.assertEqual(snake.positions[0], (50, 50))
        self.assertEqual(snake.score, 0)
        self.assertEqual(snake.food_position, (51, 51))
        snake.move((1, 1))
        self.assertEqual(snake.length, 2)
        self.assertEqual(snake.positions[0], (51, 51))
        self.assertEqual(snake.score, 100)
        snake.random_food_position()
        self.assertNotIn(snake.food_position, snake.positions)
        snake.reset()
        self.assertEqual(snake.length, 1)
        self.assertEqual(snake.positions[0], (50, 50))
        self.assertEqual(snake.score, 0)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
