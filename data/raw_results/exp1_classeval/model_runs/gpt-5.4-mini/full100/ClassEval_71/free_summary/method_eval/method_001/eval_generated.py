class PushBoxGame:
    def __init__(self, game_map):
        self.game_map = game_map
        self.player_row = None
        self.player_col = None
        self.targets = []
        self.boxes = []
        self.total_targets = 0
        self.game_over = False
        self.init_game()

    def init_game(self):
        self.targets = []
        self.boxes = []
        self.total_targets = 0
        self.game_over = False
        self.player_row = None
        self.player_col = None

        for r, row in enumerate(self.game_map):
            for c, cell in enumerate(row):
                if cell == "O":
                    self.player_row = r
                    self.player_col = c
                elif cell == "G":
                    self.targets.append((r, c))
                elif cell == "X":
                    self.boxes.append((r, c))

        self.total_targets = len(self.targets)

    def move(self, direction):
        if self.game_over:
            return False

        delta = {
            "w": (-1, 0),
            "s": (1, 0),
            "a": (0, -1),
            "d": (0, 1),
        }

        if direction not in delta or self.player_row is None or self.player_col is None:
            return False

        dr, dc = delta[direction]
        nr, nc = self.player_row + dr, self.player_col + dc

        if not self._in_bounds(nr, nc):
            return False

        if self.game_map[nr][nc] == "#":
            return False

        box_index = self._box_index_at(nr, nc)
        if box_index is not None:
            br, bc = nr + dr, nc + dc
            if not self._in_bounds(br, bc):
                return False
            if self.game_map[br][bc] == "#" or self._box_index_at(br, bc) is not None:
                return False
            self.boxes[box_index] = (br, bc)

        self.player_row, self.player_col = nr, nc
        return self.check_win()

    def check_win(self):
        box_set = set(self.boxes)
        count = 0
        for target in self.targets:
            if target in box_set:
                count += 1
        if count == self.total_targets and self.total_targets > 0:
            self.game_over = True
            return True
        return False

    def _in_bounds(self, row, col):
        return 0 <= row < len(self.game_map) and 0 <= col < len(self.game_map[row])

    def _box_index_at(self, row, col):
        for i, (br, bc) in enumerate(self.boxes):
            if br == row and bc == col:
                return i
        return None

import unittest

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

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
