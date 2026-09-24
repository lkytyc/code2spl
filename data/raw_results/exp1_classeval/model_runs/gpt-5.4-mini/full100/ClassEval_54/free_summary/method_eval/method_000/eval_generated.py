class MahjongConnect:
    def __init__(self, BOARD_SIZE, ICONS):
        self.BOARD_SIZE = BOARD_SIZE
        self.ICONS = ICONS
        self.board = self.create_board()

    def create_board(self):
        rows, cols = self.BOARD_SIZE
        import random
        return [[random.choice(self.ICONS) for _ in range(cols)] for _ in range(rows)]

    def _in_bounds(self, pos):
        if not isinstance(pos, (tuple, list)) or len(pos) != 2:
            return False
        r, c = pos
        rows, cols = self.BOARD_SIZE
        return 0 <= r < rows and 0 <= c < cols

    def is_valid_move(self, pos1, pos2):
        if not self._in_bounds(pos1) or not self._in_bounds(pos2):
            return False
        if tuple(pos1) == tuple(pos2):
            return False
        r1, c1 = pos1
        r2, c2 = pos2
        if self.board[r1][c1] != self.board[r2][c2]:
            return False
        return self.has_path(pos1, pos2)

    def has_path(self, pos1, pos2):
        if not self._in_bounds(pos1) or not self._in_bounds(pos2):
            return False

        start_r, start_c = pos1
        target = tuple(pos2)
        start_icon = self.board[start_r][start_c]

        stack = [tuple(pos1)]
        visited = {tuple(pos1)}

        while stack:
            r, c = stack.pop()
            if (r, c) == target:
                return True

            for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                if not (0 <= nr < self.BOARD_SIZE[0] and 0 <= nc < self.BOARD_SIZE[1]):
                    continue
                if (nr, nc) in visited:
                    continue
                if self.board[nr][nc] == start_icon:
                    visited.add((nr, nc))
                    stack.append((nr, nc))

        return False

    def remove_icons(self, pos1, pos2):
        if self._in_bounds(pos1):
            r1, c1 = pos1
            self.board[r1][c1] = " "
        if self._in_bounds(pos2):
            r2, c2 = pos2
            self.board[r2][c2] = " "

    def is_game_over(self):
        return all(cell == " " for row in self.board for cell in row)

import unittest

class MahjongConnectTestCreateBoard(unittest.TestCase):
    def test_create_board_1(self):
        mc = MahjongConnect([4, 4], ['a', 'b', 'c'])
        self.assertEqual(mc.BOARD_SIZE, [4, 4])
        self.assertEqual(mc.ICONS, ['a', 'b', 'c'])
        for row in mc.board:
            for icon in row:
                self.assertIn(icon, mc.ICONS)

    def test_create_board_2(self):
        mc = MahjongConnect([2, 2], ['a', 'b', 'c'])
        self.assertEqual(mc.BOARD_SIZE, [2, 2])
        self.assertEqual(mc.ICONS, ['a', 'b', 'c'])
        for row in mc.board:
            for icon in row:
                self.assertIn(icon, mc.ICONS)

    def test_create_board_3(self):
        mc = MahjongConnect([3, 3], ['a', 'b', 'c'])
        self.assertEqual(mc.BOARD_SIZE, [3, 3])
        self.assertEqual(mc.ICONS, ['a', 'b', 'c'])
        for row in mc.board:
            for icon in row:
                self.assertIn(icon, mc.ICONS)

    def test_create_board_4(self):
        mc = MahjongConnect([1, 1], ['a', 'b', 'c'])
        self.assertEqual(mc.BOARD_SIZE, [1, 1])
        self.assertEqual(mc.ICONS, ['a', 'b', 'c'])
        for row in mc.board:
            for icon in row:
                self.assertIn(icon, mc.ICONS)

    def test_create_board_5(self):
        mc = MahjongConnect([5, 5], ['a', 'b', 'c'])
        self.assertEqual(mc.BOARD_SIZE, [5, 5])
        self.assertEqual(mc.ICONS, ['a', 'b', 'c'])
        for row in mc.board:
            for icon in row:
                self.assertIn(icon, mc.ICONS)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
