import random


class MahjongConnect:
    def __init__(self, board_size, icons):
        self.rows, self.cols = board_size
        self.icons = icons
        self.board = self._generate_board()

    def _generate_board(self):
        return [
            [random.choice(self.icons) for _ in range(self.cols)]
            for _ in range(self.rows)
        ]

    def is_valid_move(self, pos1, pos2):
        r1, c1 = pos1
        r2, c2 = pos2

        # Check bounds
        if not (0 <= r1 < self.rows and 0 <= c1 < self.cols):
            return False
        if not (0 <= r2 < self.rows and 0 <= c2 < self.cols):
            return False

        # Positions must differ
        if pos1 == pos2:
            return False

        # Icons must match
        if self.board[r1][c1] != self.board[r2][c2]:
            return False

        # Must be a traversable path
        if not self.has_path(pos1, pos2):
            return False

        return True

    def has_path(self, pos1, pos2):
        r1, c1 = pos1
        target_icon = self.board[r1][c1]

        visited = set()
        stack = [pos1]

        while stack:
            current = stack.pop()
            if current == pos2:
                return True
            if current in visited:
                continue
            visited.add(current)

            r, c = current
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if (
                    0 <= nr < self.rows
                    and 0 <= nc < self.cols
                    and (nr, nc) not in visited
                    and self.board[nr][nc] == target_icon
                ):
                    stack.append((nr, nc))

        return False

    def remove_icons(self, pos1, pos2):
        r1, c1 = pos1
        r2, c2 = pos2
        self.board[r1][c1] = ' '
        self.board[r2][c2] = ' '

    def is_game_over(self):
        return all(
            self.board[r][c] == ' '
            for r in range(self.rows)
            for c in range(self.cols)
        )

import unittest

class MahjongConnectTestHasPath(unittest.TestCase):
    def test_has_path_1(self):
        mc = MahjongConnect([4, 4], ['a', 'b', 'c'])
        mc.board = [['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a']]
        res = mc.has_path((0, 0), (1, 0))
        self.assertEqual(res, True)

    def test_has_path_2(self):
        mc = MahjongConnect([4, 4], ['a', 'b', 'c'])
        mc.board = [['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a']]
        res = mc.has_path((0, 0), (0, 0))
        self.assertEqual(res, True)

    def test_has_path_3(self):
        mc = MahjongConnect([4, 4], ['a', 'b', 'c'])
        mc.board = [['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a']]
        res = mc.has_path((0, 0), (3, 0))
        self.assertEqual(res, True)

    def test_has_path_4(self):
        mc = MahjongConnect([4, 4], ['a', 'b', 'c'])
        mc.board = [['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a']]
        res = mc.has_path((0, 0), (1, 1))
        self.assertEqual(res, False)

    def test_has_path_5(self):
        mc = MahjongConnect([4, 4], ['a', 'b', 'c'])
        mc.board = [['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a']]
        res = mc.has_path((300, 0), (1, 1))
        self.assertEqual(res, False)

    def test_has_path_6(self):
        mc = MahjongConnect([4, 4], ['a', 'b', 'c'])
        mc.board = [['a', 'a', 'a', 'a'],
                    ['a', 'a', 'a', 'a'],
                    ['a', 'a', 'a', 'a'],
                    ['a', 'a', 'a', 'a']]
        res = mc.has_path((0, 0), (3, 3))
        self.assertEqual(res, True)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
