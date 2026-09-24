import random


class MahjongConnect:
    def __init__(self, BOARD_SIZE, ICONS):
        self.BOARD_SIZE = BOARD_SIZE
        self.ICONS = ICONS
        self.board = self.create_board()

    def create_board(self):
        board = []
        for _ in range(self.BOARD_SIZE[0]):
            row = []
            for _ in range(self.BOARD_SIZE[1]):
                row.append(random.choice(self.ICONS))
            board.append(row)
        return board

    def has_path(self, pos1, pos2):
        visited = set()
        stack = [pos1]

        while stack:
            current_pos = stack.pop()

            if current_pos == pos2:
                return True

            if current_pos in visited:
                continue

            visited.add(current_pos)
            x, y = current_pos

            for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                new_x = x + dx
                new_y = y + dy

                if 0 <= new_x < self.BOARD_SIZE[0] and 0 <= new_y < self.BOARD_SIZE[1]:
                    neighbor = (new_x, new_y)
                    if (
                        neighbor not in visited
                        and self.board[new_x][new_y] == self.board[x][y]
                    ):
                        stack.append(neighbor)

        return False

    def is_game_over(self):
        for row in self.board:
            if any(icon != " " for icon in row):
                return False
        return True

    def is_valid_move(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2

        positions_in_bounds = (
            0 <= x1 < self.BOARD_SIZE[0]
            and 0 <= y1 < self.BOARD_SIZE[1]
            and 0 <= x2 < self.BOARD_SIZE[0]
            and 0 <= y2 < self.BOARD_SIZE[1]
        )

        if not positions_in_bounds:
            return False

        if pos1 == pos2:
            return False

        if self.board[x1][y1] != self.board[x2][y2]:
            return False

        if not self.has_path(pos1, pos2):
            return False

        return True

    def remove_icons(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2

        self.board[x1][y1] = " "
        self.board[x2][y2] = " "

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
