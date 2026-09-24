class PushBoxGame:
    def __init__(self, game_map):
        self.map = [list(row) for row in game_map]
        self.player_pos = None
        self.targets = []
        self.boxes = []
        self.is_game_over = False
        self._scan_initial_state()

    def _scan_initial_state(self):
        for r, row in enumerate(self.map):
            for c, cell in enumerate(row):
                if cell == 'O':
                    self.player_pos = [r, c]
                elif cell == 'G':
                    self.targets.append((r, c))
                elif cell == 'X':
                    self.boxes.append([r, c])

    def move(self, direction):
        if self.is_game_over:
            return False
        dr, dc = 0, 0
        if direction == 'w':
            dr = -1
        elif direction == 's':
            dr = 1
        elif direction == 'a':
            dc = -1
        elif direction == 'd':
            dc = 1
        else:
            return False

        pr, pc = self.player_pos
        nr, nc = pr + dr, pc + dc
        if not (0 <= nr < len(self.map) and 0 <= nc < len(self.map[0])):
            return False
        if self.map[nr][nc] == '#':
            return False

        # Check if there is a box at the new position
        box_index = None
        for i, (br, bc) in enumerate(self.boxes):
            if br == nr and bc == nc:
                box_index = i
                break

        if box_index is not None:
            br, bc = self.boxes[box_index]
            nbr, nbc = br + dr, bc + dc
            if not (0 <= nbr < len(self.map) and 0 <= nbc < len(self.map[0])):
                return False
            if self.map[nbr][nbc] == '#':
                return False
            # Check if there is another box behind
            for (obr, obc) in self.boxes:
                if obr == nbr and obc == nbc:
                    return False
            # Move box
            self.boxes[box_index] = [nbr, nbc]
            # Update map representation (optional, but keep consistent)
            self.map[br][bc] = ' ' if (br, bc) not in self.targets else 'G'
            self.map[nbr][nbc] = 'X'

        # Move player
        self.map[pr][pc] = ' ' if (pr, pc) not in self.targets else 'G'
        self.map[nr][nc] = 'O'
        self.player_pos = [nr, nc]

        return self.check_win()

    def check_win(self):
        for (br, bc) in self.boxes:
            if (br, bc) not in self.targets:
                self.is_game_over = False
                return False
        self.is_game_over = True
        return True

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


class PushBoxGameTestCheckWin(unittest.TestCase):
    def setUp(self) -> None:
        self.game_map = [
            "#####",
            "#O  #",
            "# X #",
            "#  G#",
            "#####"
        ]
        self.game = PushBoxGame(self.game_map)

    def test_check_win_1(self):
        self.assertFalse(self.game.check_win())

    def test_check_win_2(self):
        moves = ['d', 's', 'a', 's', 'd']
        for move in moves:
            self.game.move(move)
        self.assertTrue(self.game.check_win())

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
