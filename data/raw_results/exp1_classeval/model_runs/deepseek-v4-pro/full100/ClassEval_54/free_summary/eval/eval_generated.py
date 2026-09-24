import random

class MahjongConnect:
    def __init__(self, BOARD_SIZE, ICONS):
        self.BOARD_SIZE = BOARD_SIZE
        self.ICONS = list(ICONS)
        self.board = []
        self.create_board()

    def create_board(self):
        rows, cols = self.BOARD_SIZE
        total_cells = rows * cols
        if total_cells % 2 != 0:
            raise ValueError("Board size must have an even number of cells")
        pairs_needed = total_cells // 2
        icons_pool = []
        for _ in range(pairs_needed):
            icon = random.choice(self.ICONS)
            icons_pool.extend([icon, icon])
        random.shuffle(icons_pool)
        self.board = [icons_pool[i * cols:(i + 1) * cols] for i in range(rows)]

    def is_valid_move(self, pos1, pos2):
        r1, c1 = pos1
        r2, c2 = pos2
        rows, cols = self.BOARD_SIZE
        if not (0 <= r1 < rows and 0 <= c1 < cols and 0 <= r2 < rows and 0 <= c2 < cols):
            return False
        if pos1 == pos2:
            return False
        if self.board[r1][c1] != self.board[r2][c2]:
            return False
        if self.board[r1][c1] == ' ':
            return False
        return self.has_path(pos1, pos2)

    def has_path(self, pos1, pos2):
        r1, c1 = pos1
        r2, c2 = pos2
        icon = self.board[r1][c1]
        rows, cols = self.BOARD_SIZE
        visited = set()
        stack = [(r1, c1)]
        visited.add((r1, c1))
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        while stack:
            r, c = stack.pop()
            if (r, c) == (r2, c2):
                return True
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    if (nr, nc) not in visited and self.board[nr][nc] == icon:
                        visited.add((nr, nc))
                        stack.append((nr, nc))
        return False

    def remove_icons(self, pos1, pos2):
        r1, c1 = pos1
        r2, c2 = pos2
        self.board[r1][c1] = ' '
        self.board[r2][c2] = ' '

    def is_game_over(self):
        for row in self.board:
            for cell in row:
                if cell != ' ':
                    return False
        return True

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


class MahjongConnectTestIsValidMove(unittest.TestCase):
    def test_is_valid_move_1(self):
        mc = MahjongConnect([4, 4], ['a', 'b', 'c'])
        mc.board = [['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a']]
        res = mc.is_valid_move((0, 0), (1, 0))
        self.assertEqual(res, True)

    def test_is_valid_move_2(self):
        mc = MahjongConnect([4, 4], ['a', 'b', 'c'])
        mc.board = [['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a']]
        res = mc.is_valid_move((0, 0), (0, 1))
        self.assertEqual(res, False)

    def test_is_valid_move_3(self):
        mc = MahjongConnect([4, 4], ['a', 'b', 'c'])
        mc.board = [['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a']]
        res = mc.is_valid_move((-1, 0), (0, 1))
        self.assertEqual(res, False)

    def test_is_valid_move_4(self):
        mc = MahjongConnect([4, 4], ['a', 'b', 'c'])
        mc.board = [['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a']]
        res = mc.is_valid_move((0, 0), (0, 0))
        self.assertEqual(res, False)

    def test_is_valid_move_5(self):
        mc = MahjongConnect([4, 4], ['a', 'b', 'c'])
        mc.board = [['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a']]
        res = mc.is_valid_move((300, 0), (0, 0))
        self.assertEqual(res, False)

    def test_is_valid_move_6(self):
        mc = MahjongConnect([4, 4], ['a', 'b', 'c'])
        mc.board = [['a', 'b', 'a', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a']]
        res = mc.is_valid_move((0, 2), (0, 0))
        self.assertEqual(res, False)


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


class MahjongConnectTestRemoveIcons(unittest.TestCase):
    def test_remove_icons_1(self):
        mc = MahjongConnect([4, 4], ['a', 'b', 'c'])
        mc.board = [['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a']]
        mc.remove_icons((0, 0), (1, 0))
        self.assertEqual(mc.board, [[' ', 'b', 'c', 'a'],
                                    [' ', 'b', 'c', 'a'],
                                    ['a', 'b', 'c', 'a'],
                                    ['a', 'b', 'c', 'a']])

    def test_remove_icons_2(self):
        mc = MahjongConnect([4, 4], ['a', 'b', 'c'])
        mc.board = [['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a']]
        mc.remove_icons((2, 0), (1, 0))
        self.assertEqual(mc.board, [['a', 'b', 'c', 'a'],
                                    [' ', 'b', 'c', 'a'],
                                    [' ', 'b', 'c', 'a'],
                                    ['a', 'b', 'c', 'a']])

    def test_remove_icons_3(self):
        mc = MahjongConnect([4, 4], ['a', 'b', 'c'])
        mc.board = [['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a']]
        mc.remove_icons((1, 1), (0, 1))
        self.assertEqual(mc.board, [['a', ' ', 'c', 'a'],
                                    ['a', ' ', 'c', 'a'],
                                    ['a', 'b', 'c', 'a'],
                                    ['a', 'b', 'c', 'a']])

    def test_remove_icons_4(self):
        mc = MahjongConnect([4, 4], ['a', 'b', 'c'])
        mc.board = [['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a']]
        mc.remove_icons((3, 0), (2, 0))
        self.assertEqual(mc.board, [['a', 'b', 'c', 'a'],
                                    ['a', 'b', 'c', 'a'],
                                    [' ', 'b', 'c', 'a'],
                                    [' ', 'b', 'c', 'a']])

    def test_remove_icons_5(self):
        mc = MahjongConnect([4, 4], ['a', 'b', 'c'])
        mc.board = [['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a']]
        mc.remove_icons((3, 3), (2, 3))
        self.assertEqual(mc.board, [['a', 'b', 'c', 'a'],
                                    ['a', 'b', 'c', 'a'],
                                    ['a', 'b', 'c', ' '],
                                    ['a', 'b', 'c', ' ']])


class MahjongConnectTestIsGameOver(unittest.TestCase):
    def test_is_game_over_1(self):
        mc = MahjongConnect([4, 4], ['a', 'b', 'c'])
        mc.board = [[' ', ' ', ' ', ' '],
                    [' ', ' ', ' ', ' '],
                    [' ', ' ', ' ', ' '],
                    [' ', ' ', ' ', ' ']]
        res = mc.is_game_over()
        self.assertEqual(res, True)

    def test_is_game_over_2(self):
        mc = MahjongConnect([4, 4], ['a', 'b', 'c'])
        mc.board = [['a', ' ', ' ', ' '],
                    ['a', ' ', ' ', ' '],
                    [' ', ' ', ' ', ' '],
                    [' ', ' ', ' ', ' ']]
        res = mc.is_game_over()
        self.assertEqual(res, False)

    def test_is_game_over_3(self):
        mc = MahjongConnect([4, 4], ['a', 'b', 'c'])
        mc.board = [[' ', ' ', ' ', ' '],
                    ['a', ' ', ' ', ' '],
                    [' ', ' ', ' ', ' '],
                    [' ', ' ', ' ', ' ']]
        res = mc.is_game_over()
        self.assertEqual(res, False)

    def test_is_game_over_4(self):
        mc = MahjongConnect([4, 4], ['a', 'b', 'c'])
        mc.board = [['1', ' ', ' ', ' '],
                    [' ', ' ', ' ', ' '],
                    [' ', ' ', ' ', ' '],
                    [' ', ' ', ' ', ' ']]
        res = mc.is_game_over()
        self.assertEqual(res, False)

    def test_is_game_over_5(self):
        mc = MahjongConnect([4, 4], ['a', 'b', 'c'])
        mc.board = [['a', ' ', ' ', ' '],
                    [' ', ' ', ' ', ' '],
                    [' ', ' ', ' ', ' '],
                    [' ', ' ', ' ', ' ']]
        res = mc.is_game_over()
        self.assertEqual(res, False)


class MahjongConnectTest(unittest.TestCase):
    def test_mahjongconnect(self):
        mc = MahjongConnect([4, 4], ['a', 'b', 'c'])
        self.assertEqual(mc.BOARD_SIZE, [4, 4])
        self.assertEqual(mc.ICONS, ['a', 'b', 'c'])
        for row in mc.board:
            for icon in row:
                self.assertIn(icon, mc.ICONS)

        mc.board = [['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a']]
        res = mc.is_valid_move((0, 0), (1, 0))
        self.assertEqual(res, True)

        res = mc.has_path((0, 0), (1, 0))
        self.assertEqual(res, True)

        mc.remove_icons((0, 0), (1, 0))
        self.assertEqual(mc.board, [[' ', 'b', 'c', 'a'],
                                    [' ', 'b', 'c', 'a'],
                                    ['a', 'b', 'c', 'a'],
                                    ['a', 'b', 'c', 'a']])

        mc.board = [[' ', ' ', ' ', ' '],
                    [' ', ' ', ' ', ' '],
                    [' ', ' ', ' ', ' '],
                    [' ', ' ', ' ', ' ']]
        res = mc.is_game_over()
        self.assertEqual(res, True)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
