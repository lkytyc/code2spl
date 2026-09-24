import random

class MinesweeperGame:
    """
    This is a class that implements mine sweeping games including minesweeping and winning judgment.
    """

    def __init__(self, n, k) -> None:
        """
        Initializes the MinesweeperGame class with the size of the board and the number of mines.
        :param n: The size of the board, int.
        :param k: The number of mines, int.
        """
        self.n = n
        self.k = k
        self.minesweeper_map = self.generate_mine_sweeper_map()
        self.player_map = self.generate_playerMap()
        self.score = 0

    def generate_mine_sweeper_map(self):
        """
        Generates a minesweeper map with the given size of the board and the number of mines,the given parameter n is the size of the board,the size of the board is n*n,the parameter k is the number of mines,'X' represents the mine,other numbers represent the number of mines around the position.
        :return: The minesweeper map, list.
        >>> minesweeper_game = MinesweeperGame(3, 1)
        >>> minesweeper_game.generate_mine_sweeper_map()
        [['X', 1, 0], [1, 1, 0], [0, 0, 0]]

        """
        board = [[0 for _ in range(self.n)] for _ in range(self.n)]
        positions = [(i, j) for i in range(self.n) for j in range(self.n)]
        mines = random.sample(positions, min(self.k, self.n * self.n))
        for x, y in mines:
            board[x][y] = 'X'
        for i in range(self.n):
            for j in range(self.n):
                if board[i][j] == 'X':
                    continue
                count = 0
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        if dx == 0 and dy == 0:
                            continue
                        nx, ny = i + dx, j + dy
                        if 0 <= nx < self.n and 0 <= ny < self.n and board[nx][ny] == 'X':
                            count += 1
                board[i][j] = count
        return board

    def generate_playerMap(self):
        """
        Generates a player map with the given size of the board, the given parameter n is the size of the board,the size of the board is n*n,the parameter k is the number of mines,'-' represents the unknown position.
        :return: The player map, list.
        >>> minesweeper_game = MinesweeperGame(3, 1)
        >>> minesweeper_game.generate_playerMap()
        [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]

        """
        return [['-' for _ in range(self.n)] for _ in range(self.n)]

    def check_won(self, map):
        """
        Checks whether the player has won the game,if there are just mines in the player map,return True,otherwise return False.
        :return: True if the player has won the game, False otherwise.
        >>> minesweeper_game = MinesweeperGame(3, 1)
        >>> minesweeper_game.minesweeper_map = [['X', 1, 0], [1, 1, 0], [0, 0, 0]]
        >>> minesweeper_game.player_map = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
        >>> minesweeper_game.check_won(minesweeper_game.player_map)
        False

        """
        for i in range(self.n):
            for j in range(self.n):
                if map[i][j] == '-' and self.minesweeper_map[i][j] != 'X':
                    return False
        return True

    def sweep(self, x, y):
        """
        Sweeps the given position.
        :param x: The x coordinate of the position, int.
        :param y: The y coordinate of the position, int.
        :return: True if the player has won the game, False otherwise,if the game still continues, return the player map, list.
        >>> minesweeper_game = MinesweeperGame(3, 1)
        >>> minesweeper_game.minesweeper_map = [['X', 1, 0], [1, 1, 0], [0, 0, 0]]
        >>> minesweeper_game.player_map = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
        >>> minesweeper_game.sweep(1, 1)
        [['-', '-', '-'], ['-', 1, '-'], ['-', '-', '-']]

        """
        if not (0 <= x < self.n and 0 <= y < self.n):
            return self.player_map
        if self.player_map[x][y] != '-':
            return True if self.check_won(self.player_map) else self.player_map
        self.player_map[x][y] = self.minesweeper_map[x][y]
        if self.minesweeper_map[x][y] == 'X':
            return False
        return True if self.check_won(self.player_map) else self.player_map

import unittest

class MinesweeperGameTestGeneratePlayerMap(unittest.TestCase):
    def test_generate_playerMap(self):
        minesweeper_game = MinesweeperGame(3, 2)
        self.assertEqual(minesweeper_game.generate_playerMap(), [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']])

    def test_generate_playerMap_2(self):
        minesweeper_game = MinesweeperGame(3, 1)
        self.assertEqual(minesweeper_game.generate_playerMap(), [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']])

    def test_generate_playerMap_3(self):
        minesweeper_game = MinesweeperGame(4, 2)
        self.assertEqual(minesweeper_game.generate_playerMap(),[['-', '-', '-', '-'],['-', '-', '-', '-'],['-', '-', '-', '-'],['-', '-', '-', '-']])

    def test_generate_playerMap_4(self):
        minesweeper_game = MinesweeperGame(1, 4)
        self.assertEqual(minesweeper_game.generate_playerMap(), [['-']])

    def test_generate_playerMap_5(self):
        minesweeper_game = MinesweeperGame(2, 5)
        self.assertEqual(minesweeper_game.generate_playerMap(), [['-', '-'], ['-', '-']])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
