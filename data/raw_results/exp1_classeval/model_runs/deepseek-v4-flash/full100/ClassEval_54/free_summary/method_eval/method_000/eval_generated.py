import random
from collections import deque

class MahjongConnect:
    def __init__(self, board_size, icons):
        self.board_size = board_size
        self.icons = icons
        self.board = self.create_board()

    def create_board(self):
        self.board = [
            [random.choice(self.icons) for _ in range(self.board_size[1])]
            for _ in range(self.board_size[0])
        ]
        return self.board

    def is_valid_move(self, pos1, pos2):
        r1, c1 = pos1
        r2, c2 = pos2
        rows, cols = self.board_size

        if not (0 <= r1 < rows and 0 <= c1 < cols and 0 <= r2 < rows and 0 <= c2 < cols):
            return False

        if r1 == r2 and c1 == c2:
            return False

        if self.board[r1][c1] == ' ' or self.board[r2][c2] == ' ':
            return False

        if self.board[r1][c1] != self.board[r2][c2]:
            return False

        icon = self.board[r1][c1]
        visited = [[False] * cols for _ in range(rows)]
        queue = deque([(r1, c1)])
        visited[r1][c1] = True

        while queue:
            r, c = queue.popleft()

            if r == r2 and c == c2:
                return True

            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc

                if 0 <= nr < rows and 0 <= nc < cols:
                    if not visited[nr][nc] and self.board[nr][nc] == icon:
                        visited[nr][nc] = True
                        queue.append((nr, nc))

        return False

    def remove_icons(self, pos1, pos2):
        if self.is_valid_move(pos1, pos2):
            self.board[pos1[0]][pos1[1]] = ' '
            self.board[pos2[0]][pos2[1]] = ' '
            return True
        return False

    def is_game_over(self):
        return all(cell == ' ' for row in self.board for cell in row)

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
