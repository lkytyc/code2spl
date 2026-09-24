class PushBoxGame:
    def __init__(self, map):
        self.map = map
        self.player_row = 0
        self.player_col = 0
        self.targets = []
        self.boxes = []
        self.target_count = 0
        self.is_game_over = False
        self.init_game()

    def init_game(self):
        for row in range(len(self.map)):
            for col in range(len(self.map[row])):
                cell = self.map[row][col]
                if cell == 'O':
                    self.player_row = row
                    self.player_col = col
                elif cell == 'G':
                    self.targets.append((row, col))
                    self.target_count += 1
                elif cell == 'X':
                    self.boxes.append((row, col))

    def check_win(self):
        self.is_game_over = all(box in self.targets for box in self.boxes) and len(self.boxes) == self.target_count
        return self.is_game_over

    def move(self, direction):
        dr = 0
        dc = 0
        if direction == 'w':
            dr = -1
        elif direction == 's':
            dr = 1
        elif direction == 'a':
            dc = -1
        elif direction == 'd':
            dc = 1

        new_pr = self.player_row + dr
        new_pc = self.player_col + dc

        if not (0 <= new_pr < len(self.map) and 0 <= new_pc < len(self.map[new_pr])):
            return self.check_win()

        if self.map[new_pr][new_pc] == '#':
            return self.check_win()

        if (new_pr, new_pc) in self.boxes:
            new_br = new_pr + dr
            new_bc = new_pc + dc

            if not (0 <= new_br < len(self.map) and 0 <= new_bc < len(self.map[new_br])):
                return self.check_win()

            if self.map[new_br][new_bc] == '#':
                return self.check_win()

            if (new_br, new_bc) in self.boxes:
                return self.check_win()

            self.boxes.remove((new_pr, new_pc))
            self.boxes.append((new_br, new_bc))
            self.player_row = new_pr
            self.player_col = new_pc
        else:
            self.player_row = new_pr
            self.player_col = new_pc

        return self.check_win()

    def print_map(self):
        for row in self.map:
            print(' '.join(row))

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
