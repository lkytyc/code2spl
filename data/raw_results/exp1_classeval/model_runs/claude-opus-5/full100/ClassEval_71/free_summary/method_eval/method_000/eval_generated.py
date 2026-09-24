class PushBoxGame:
    def __init__(self, map):
        self.map = map
        self.player = None
        self.targets = []
        self.boxes = []
        self.is_game_over = False

        for r, row in enumerate(map):
            for c, cell in enumerate(row):
                if cell == 'O':
                    self.player = (r, c)
                elif cell == 'G':
                    self.targets.append((r, c))
                elif cell == 'X':
                    self.boxes.append((r, c))

    def move(self, direction):
        dr, dc = 0, 0
        if direction == 'w':
            dr, dc = -1, 0
        elif direction == 's':
            dr, dc = 1, 0
        elif direction == 'a':
            dr, dc = 0, -1
        elif direction == 'd':
            dr, dc = 0, 1

        pr, pc = self.player
        nr, nc = pr + dr, pc + dc

        if self.map[nr][nc] == '#':
            return self.check_win()

        if (nr, nc) in self.boxes:
            br, bc = nr + dr, nc + dc
            if self.map[br][bc] == '#':
                return self.check_win()
            self.boxes.remove((nr, nc))
            self.boxes.append((br, bc))

        self.player = (nr, nc)
        return self.check_win()

    def check_win(self):
        count = sum(1 for box in self.boxes if box in self.targets)
        if count == len(self.targets):
            self.is_game_over = True
        return self.is_game_over

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
