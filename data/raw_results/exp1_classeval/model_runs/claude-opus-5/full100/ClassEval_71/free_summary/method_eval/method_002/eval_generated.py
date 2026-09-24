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

class PushBoxGameTestMove(unittest.TestCase):
    def setUp(self) -> None:
        self.game_map = [
            "#####",
            "#O  #",
            "# X #",
            "#  G#",
            "#####"
        ]
        self.game = PushBoxGame(self.game_map)

    def test_move_1(self):
        moves = ['d', 's', 'a', 's']
        for move in moves:
            self.assertFalse(self.game.move(move))
        self.assertTrue(self.game.move('d'))

    def test_move_2(self):
        self.game.move('a')
        self.assertEqual(self.game.player_col, 1)
        self.assertEqual(self.game.player_row, 1)
        self.assertFalse(self.game.is_game_over)

    def test_move_3(self):
        self.game.move('d')
        self.assertEqual(self.game.player_col, 2)
        self.assertEqual(self.game.player_row, 1)
        self.assertFalse(self.game.is_game_over)

    def test_move_4(self):
        self.game.move('s')
        self.assertEqual(self.game.player_col, 1)
        self.assertEqual(self.game.player_row, 2)
        self.assertFalse(self.game.is_game_over)

    def test_move_5(self):
        self.game.move('w')
        self.assertEqual(self.game.player_col, 1)
        self.assertEqual(self.game.player_row, 1)
        self.assertFalse(self.game.is_game_over)

    def test_move_6(self):
        self.game.move('?')
        self.assertFalse(self.game.is_game_over)

    def test_move_7(self):
        self.game_map = [
            "#####",
            "# X #",
            "# O #",
            "#  G#",
            "#####"
        ]
        self.game = PushBoxGame(self.game_map)
        self.game.move('w')
        self.assertEqual(self.game.player_col, 2)
        self.assertEqual(self.game.player_row, 2)
        self.assertFalse(self.game.is_game_over)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
