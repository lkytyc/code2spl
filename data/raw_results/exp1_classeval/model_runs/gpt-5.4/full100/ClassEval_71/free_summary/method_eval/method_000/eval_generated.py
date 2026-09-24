class PushBoxGame:
    def __init__(self, map):
        self.map = map
        self.player = None
        self.targets = []
        self.boxes = []
        self.num_targets = 0
        self.game_over = False

        for i, row in enumerate(map):
            for j, cell in enumerate(row):
                if cell == "O":
                    self.player = (i, j)
                elif cell == "G":
                    self.targets.append((i, j))
                elif cell == "X":
                    self.boxes.append((i, j))

        self.num_targets = len(self.targets)

    def move(self, direction):
        if self.game_over or self.player is None:
            return

        moves = {
            "w": (-1, 0),
            "s": (1, 0),
            "a": (0, -1),
            "d": (0, 1),
        }

        if direction not in moves:
            return

        di, dj = moves[direction]
        pi, pj = self.player
        ni, nj = pi + di, pj + dj

        if not self._in_bounds(ni, nj) or self.map[ni][nj] == "#":
            return

        box_index = self._box_index_at(ni, nj)
        if box_index is not None:
            bi, bj = ni + di, nj + dj
            if not self._in_bounds(bi, bj) or self.map[bi][bj] == "#":
                return
            if self._box_index_at(bi, bj) is not None:
                return
            self.boxes[box_index] = (bi, bj)
            self.player = (ni, nj)
        else:
            self.player = (ni, nj)

        self.check_win()

    def check_win(self):
        count = 0
        target_set = set(self.targets)
        for box in self.boxes:
            if box in target_set:
                count += 1
        if count == self.num_targets and self.num_targets > 0:
            self.game_over = True
            return True
        return False

    def _box_index_at(self, i, j):
        for idx, (bi, bj) in enumerate(self.boxes):
            if bi == i and bj == j:
                return idx
        return None

    def _in_bounds(self, i, j):
        return 0 <= i < len(self.map) and 0 <= j < len(self.map[i])

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
