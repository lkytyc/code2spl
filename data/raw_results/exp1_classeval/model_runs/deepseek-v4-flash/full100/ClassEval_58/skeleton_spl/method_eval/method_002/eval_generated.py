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
        arr = [[0 for _ in range(self.n)] for _ in range(self.n)]
        for num in range(self.k):
            x = random.randint(0, self.n - 1)
            y = random.randint(0, self.n - 1)
            arr[y][x] = 'X'
            if (x >= 0 and x <= self.n - 2) and (y >= 0 and y <= self.n - 1) and arr[y][x + 1] != 'X':
                arr[y][x + 1] += 1
            if (x >= 1 and x <= self.n - 1) and (y >= 0 and y <= self.n - 1) and arr[y][x - 1] != 'X':
                arr[y][x - 1] += 1
            if (x >= 1 and x <= self.n - 1) and (y >= 1 and y <= self.n - 1) and arr[y - 1][x - 1] != 'X':
                arr[y - 1][x - 1] += 1
            if (x >= 0 and x <= self.n - 2) and (y >= 1 and y <= self.n - 1) and arr[y - 1][x + 1] != 'X':
                arr[y - 1][x + 1] += 1
            if (x >= 0 and x <= self.n - 1) and (y >= 1 and y <= self.n - 1) and arr[y - 1][x] != 'X':
                arr[y - 1][x] += 1
            if (x >= 0 and x <= self.n - 2) and (y >= 0 and y <= self.n - 2) and arr[y + 1][x + 1] != 'X':
                arr[y + 1][x + 1] += 1
            if (x >= 1 and x <= self.n - 1) and (y >= 0 and y <= self.n - 2) and arr[y + 1][x - 1] != 'X':
                arr[y + 1][x - 1] += 1
            if (x >= 0 and x <= self.n - 1) and (y >= 0 and y <= self.n - 2) and arr[y + 1][x] != 'X':
                arr[y + 1][x] += 1
        return arr

    def generate_playerMap(self):
        """
        Generates a player map with the given size of the board, the given parameter n is the size of the board,the size of the board is n*n,the parameter k is the number of mines,'-' represents the unknown position.
        :return: The player map, list.
        >>> minesweeper_game = MinesweeperGame(3, 1)
        >>> minesweeper_game.generate_playerMap()
        [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]

        """
        arr = [['-' for row in range(self.n)] for column in range(self.n)]
        return arr

    def check_won(self,map):
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
        if self.minesweeper_map[x][y] == 'X':
            return False
        self.player_map[x][y] = self.minesweeper_map[x][y]
        self.score += 1
        if self.check_won(self.player_map):
            return True
        return self.player_map

import unittest

class MinesweeperGameTestCheckWon(unittest.TestCase):
    def test_check_won(self):
        minesweeper_game = MinesweeperGame(3, 1)
        minesweeper_game.minesweeper_map = [['X', 1, 0], [1, 1, 0], [0, 0, 0]]
        minesweeper_game.player_map = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
        self.assertEqual(minesweeper_game.check_won(minesweeper_game.player_map), False)

    def test_check_won_2(self):
        minesweeper_game = MinesweeperGame(3, 1)
        minesweeper_game.minesweeper_map = [['X', 1, 0], [1, 1, 0], [0, 0, 0]]
        minesweeper_game.player_map = [['-', '-', '-'], ['-', 1, '-'], ['-', '-', '-']]
        self.assertEqual(minesweeper_game.check_won(minesweeper_game.player_map), False)

    def test_check_won_3(self):
        minesweeper_game = MinesweeperGame(3, 0)
        minesweeper_game.minesweeper_map = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        minesweeper_game.player_map = [['-', '-', '-'], ['-', 1, '-'], ['-', '-', '-']]
        self.assertEqual(minesweeper_game.check_won(minesweeper_game.player_map), False)

    def test_check_won_4(self):
        minesweeper_game = MinesweeperGame(3, 1)
        minesweeper_game.minesweeper_map = [['X', 1, 0], [1, 1, 0], [0, 0, 0]]
        minesweeper_game.player_map = [['-', '1', '0'], ['1', 1, '0'], ['0', '0', '0']]
        self.assertEqual(minesweeper_game.check_won(minesweeper_game.player_map), True)

    def test_check_won_5(self):
        minesweeper_game = MinesweeperGame(3, 1)
        minesweeper_game.minesweeper_map = [['X', 1, 0], [1, 1, 0], [0, 0, 0]]
        minesweeper_game.player_map = [['X', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
        self.assertEqual(minesweeper_game.check_won(minesweeper_game.player_map), False)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
