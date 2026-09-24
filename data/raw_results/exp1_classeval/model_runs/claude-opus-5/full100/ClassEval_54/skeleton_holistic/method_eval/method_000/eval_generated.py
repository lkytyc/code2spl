import random

class MahjongConnect:
    """
    MahjongConnect is a class representing a game board for Mahjong Connect with features like creating the board, checking valid moves, finding paths, removing icons, and checking if the game is over.
    """

    def __init__(self, BOARD_SIZE, ICONS):
        """
        initialize the board size and the icon list, create the game board
        :param BOARD_SIZE: list of two integer numbers, representing the number of rows and columns of the game board
        :param ICONS: list of string, representing the icons
        >>>mc = MahjongConnect([4, 4], ['a', 'b', 'c'])
        mc.BOARD_SIZE = [4, 4]
        mc.ICONS = ['a', 'b', 'c']
        mc.board = mc.create_board()
        """
        self.BOARD_SIZE = BOARD_SIZE
        self.ICONS = ICONS
        self.board = self.create_board()

    def create_board(self):
        """
        create the game board with the given board size and icons
        :return: 2-dimensional list, the game board
        >>> mc = MahjongConnect([4, 4], ['a', 'b', 'c'])
        >>> mc.create_board()
        mc.board = [['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a']]
        """
        rows, cols = self.BOARD_SIZE
        total_cells = rows * cols
        # Build a list of icons repeated to fill the board, ensuring pairs
        icons_list = []
        for i in range(total_cells):
            icons_list.append(self.ICONS[i % len(self.ICONS)])
        # Shuffle to randomize placement
        random.shuffle(icons_list)
        # Build 2D board
        board = []
        idx = 0
        for r in range(rows):
            row = []
            for c in range(cols):
                row.append(icons_list[idx])
                idx += 1
            board.append(row)
        return board

    def is_valid_move(self, pos1, pos2):
        """
        check if the move of two icons is valid (i.e. positions are within the game board range, the two positions are not the same, the two positions have the same icon, and there is a valid path between the two positions)
        :param pos1: position tuple(x, y) of the first icon
        :param pos2: position tuple(x, y) of the second icon
        :return:True or False ,representing whether the move of two icons is valid
        >>> mc = MahjongConnect([4, 4], ['a', 'b', 'c'])
        mc.board = [['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a']]
        >>> mc.is_valid_move((0, 0), (1, 0))
        True
        """
        rows, cols = self.BOARD_SIZE
        x1, y1 = pos1
        x2, y2 = pos2

        # Check bounds
        if not (0 <= x1 < rows and 0 <= y1 < cols):
            return False
        if not (0 <= x2 < rows and 0 <= y2 < cols):
            return False

        # Positions must differ
        if pos1 == pos2:
            return False

        # Icons must be non-empty and match
        if self.board[x1][y1] == ' ' or self.board[x2][y2] == ' ':
            return False
        if self.board[x1][y1] != self.board[x2][y2]:
            return False

        # Must have a valid path
        return self.has_path(pos1, pos2)

    def has_path(self, pos1, pos2):
        """
        check if there is a path between two icons using BFS, allowing at most two turns.
        :param pos1: position tuple(x, y) of the first icon
        :param pos2: position tuple(x, y) of the second icon
        :return: True or False ,representing whether there is a path between two icons
        >>> mc = MahjongConnect([4, 4], ['a', 'b', 'c'])
        mc.board = [['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a']]
        >>> mc.is_valid_move((0, 0), (1, 0))
        True
        """
        rows, cols = self.BOARD_SIZE
        x1, y1 = pos1
        x2, y2 = pos2

        # BFS state: (x, y, direction, turns)
        # direction: None means just started, 0=up, 1=down, 2=left, 3=right
        # turns: number of direction changes so far (max 2 allowed)
        from collections import deque

        # visited: (x, y, direction, turns) — track min turns to reach each (x, y, direction)
        # to avoid revisiting with equal or more turns
        visited = {}

        queue = deque()
        # Start with no direction and 0 turns
        queue.append((x1, y1, -1, 0))
        visited[(x1, y1, -1)] = 0

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while queue:
            x, y, cur_dir, turns = queue.popleft()

            for d_idx, (dx, dy) in enumerate(directions):
                nx, ny = x + dx, y + dy

                # New turn count
                new_turns = turns if d_idx == cur_dir else turns + 1

                if new_turns > 2:
                    continue

                # Must stay in bounds — but we allow one step outside to wrap around
                # Actually in standard Mahjong Connect the path can go through the border
                # but positions must be within board. Check bounds:
                if not (0 <= nx < rows and 0 <= ny < cols):
                    continue

                # Reached destination
                if (nx, ny) == (x2, y2):
                    return True

                # Can only pass through empty cells (not the destination which is checked above)
                if self.board[nx][ny] != ' ':
                    continue

                state = (nx, ny, d_idx)
                if state in visited and visited[state] <= new_turns:
                    continue

                visited[state] = new_turns
                queue.append((nx, ny, d_idx, new_turns))

        return False

    def remove_icons(self, pos1, pos2):
        """
        remove the connected icons on the game board
        :param pos1: position tuple(x, y) of the first icon to be removed
        :param pos2: position tuple(x, y) of the second icon to be removed
        :return: None
        >>> mc = MahjongConnect([4, 4], ['a', 'b', 'c'])
        mc.board = [['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a']]
        >>> mc.remove_icons((0, 0), (1, 0))
        mc.board = [[' ', 'b', 'c', 'a'],
                    [' ', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a']]
        """
        x1, y1 = pos1
        x2, y2 = pos2
        self.board[x1][y1] = ' '
        self.board[x2][y2] = ' '

    def is_game_over(self):
        """
        Check if the game is over (i.e., if there are no more icons on the game board)
        :return: True or False ,representing whether the game is over
        >>> mc = MahjongConnect([4, 4] ['a', 'b', 'c'])
        >>> mc.board = [[' ', ' ', ' ', ' '],
        >>>         [' ', ' ', ' ', ' '],
        >>>         [' ', ' ', ' ', ' '],
        >>>         [' ', ' ', ' ', ' ']]
        >>> mc.is_game_over()
        True
        """
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

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
