class MahjongConnect:
    def __init__(self, BOARD_SIZE, ICONS):
        self.BOARD_SIZE = BOARD_SIZE
        self.ICONS = ICONS
        self.board = self.create_board()

    def create_board(self):
        import random
        board = [
            [random.choice(self.ICONS) for _ in range(self.BOARD_SIZE[1])]
            for _ in range(self.BOARD_SIZE[0])
        ]
        return board

    def has_path(self, pos1: tuple[int, int], pos2: tuple[int, int]) -> bool:
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

            for direction in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                new_x = x + direction[0]
                new_y = y + direction[1]
                if 0 <= new_x < self.BOARD_SIZE[0] and 0 <= new_y < self.BOARD_SIZE[1]:
                    if (new_x, new_y) not in visited and self.board[new_x][new_y] == self.board[x][y]:
                        stack.append((new_x, new_y))

        return False

    def is_game_over(self):
        for row in self.board:
            has_non_space_icon = any(icon != " " for icon in row)
            if has_non_space_icon:
                return False
        return True

    def is_valid_move(self, pos1: tuple, pos2: tuple) -> bool:
        x1, y1 = pos1
        x2, y2 = pos2

        bounds_valid = (
            0 <= x1 < self.BOARD_SIZE[0]
            and 0 <= y1 < self.BOARD_SIZE[1]
            and 0 <= x2 < self.BOARD_SIZE[0]
            and 0 <= y2 < self.BOARD_SIZE[1]
        )
        if not bounds_valid:
            return False

        same_position = pos1 == pos2
        if same_position:
            return False

        same_icon = self.board[x1][y1] == self.board[x2][y2]
        if not same_icon:
            return False

        path_exists = self.has_path(pos1, pos2)
        if not path_exists:
            return False

        return True

    def remove_icons(self, pos1: tuple, pos2: tuple):
        x1, y1 = pos1
        x2, y2 = pos2
        self.board[x1][y1] = " "
        self.board[x2][y2] = " "

import unittest

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

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
