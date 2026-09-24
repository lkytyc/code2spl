class Sokoban:
    def __init__(self, grid):
        self.grid = [list(row) for row in grid]
        self.player_pos = None
        self.boxes = set()
        self.targets = set()
        self.completed = False

        for r, row in enumerate(self.grid):
            for c, cell in enumerate(row):
                if cell == 'O':
                    self.player_pos = (r, c)
                    self.grid[r][c] = ' '
                elif cell == 'G':
                    self.targets.add((r, c))
                elif cell == 'X':
                    self.boxes.add((r, c))
                    self.grid[r][c] = ' '

    def move(self, direction):
        if self.completed:
            return True

        dr, dc = {
            'w': (-1, 0),
            's': (1, 0),
            'a': (0, -1),
            'd': (0, 1)
        }.get(direction, (0, 0))

        if dr == 0 and dc == 0:
            return self.completed

        r, c = self.player_pos
        nr, nc = r + dr, c + dc

        if self.grid[nr][nc] == '#':
            return self.completed

        if (nr, nc) in self.boxes:
            br, bc = nr + dr, nc + dc
            if self.grid[br][bc] == '#' or (br, bc) in self.boxes:
                return self.completed
            self.boxes.remove((nr, nc))
            self.boxes.add((br, bc))

        self.player_pos = (nr, nc)

        if all(box in self.targets for box in self.boxes):
            self.completed = True

        return self.completed

import unittest

class PushBoxGameTestInitGame(unittest.TestCase):
    def setUp(self) -> None:
        self.game_map = [
            "#####",
            "#O  #",
            "# X #",
            "#  G#",
            "#####"
        ]
        self.game = PushBoxGame(self.game_map)

    def test_init_game_1(self):
        self.assertEqual(self.game.map, self.game_map)

    def test_init_game_2(self):
        self.assertEqual(self.game.is_game_over, False)

    def test_init_game_3(self):
        self.assertEqual(self.game.player_col, 1)

    def test_init_game_4(self):
        self.assertEqual(self.game.player_row, 1)

    def test_init_game_5(self):
        self.assertEqual(self.game.targets, [(3, 3)])

    def test_init_game_6(self):
        self.assertEqual(self.game.boxes, [(2, 2)])

    def test_init_game_7(self):
        self.assertEqual(self.game.target_count, 1)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
