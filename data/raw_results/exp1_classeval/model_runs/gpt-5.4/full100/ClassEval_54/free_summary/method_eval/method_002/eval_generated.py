import random

class MahjongConnect:
    def __init__(self, board_size, icons):
        self.board_size = board_size
        self.icons = list(icons)
        self.board = self.create_board()

    def create_board(self):
        return [
            [random.choice(self.icons) for _ in range(self.board_size)]
            for _ in range(self.board_size)
        ]

    def _in_bounds(self, pos):
        r, c = pos
        return 0 <= r < self.board_size and 0 <= c < self.board_size

    def is_valid_move(self, pos1, pos2):
        if not self._in_bounds(pos1) or not self._in_bounds(pos2):
            return False
        if pos1 == pos2:
            return False
        if self.board[pos1[0]][pos1[1]] == " " or self.board[pos2[0]][pos2[1]] == " ":
            return False
        if self.board[pos1[0]][pos1[1]] != self.board[pos2[0]][pos2[1]]:
            return False
        return self.has_path(pos1, pos2)

    def has_path(self, pos1, pos2):
        if not self._in_bounds(pos1) or not self._in_bounds(pos2):
            return False

        target_icon = self.board[pos1[0]][pos1[1]]
        if target_icon == " ":
            return False

        stack = [pos1]
        visited = {pos1}

        while stack:
            r, c = stack.pop()
            if (r, c) == pos2:
                return True

            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.board_size and 0 <= nc < self.board_size:
                    if (nr, nc) not in visited and self.board[nr][nc] == target_icon:
                        visited.add((nr, nc))
                        stack.append((nr, nc))

        return False

    def remove_icons(self, pos1, pos2):
        if self._in_bounds(pos1):
            self.board[pos1[0]][pos1[1]] = " "
        if self._in_bounds(pos2):
            self.board[pos2[0]][pos2[1]] = " "

    def is_game_over(self):
        return all(cell == " " for row in self.board for cell in row)

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
