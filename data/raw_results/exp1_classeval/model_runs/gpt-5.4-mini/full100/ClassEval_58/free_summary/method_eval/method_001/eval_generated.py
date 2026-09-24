class MinesweeperGame:
    def __init__(self, n, k):
        self.n = n
        self.k = k
        self.mine_map = self.generate_mine_sweeper_map()
        self.player_map = self.generate_playerMap()
        self.score = 0

    def generate_mine_sweeper_map(self):
        import random

        board = [[0 for _ in range(self.n)] for _ in range(self.n)]
        mines_placed = 0

        while mines_placed < self.k:
            x = random.randrange(self.n)
            y = random.randrange(self.n)
            if board[x][y] == 'X':
                continue

            board[x][y] = 'X'
            mines_placed += 1

            for i in range(max(0, x - 1), min(self.n, x + 2)):
                for j in range(max(0, y - 1), min(self.n, y + 2)):
                    if board[i][j] != 'X':
                        board[i][j] += 1

        return board

    def generate_playerMap(self):
        return [['-' for _ in range(self.n)] for _ in range(self.n)]

    def check_won(self, map):
        for i in range(self.n):
            for j in range(self.n):
                if map[i][j] == '-' and self.mine_map[i][j] != 'X':
                    return False
        return True

    def sweep(self, x, y):
        if self.mine_map[x][y] == 'X':
            return False

        if self.player_map[x][y] == '-':
            self.player_map[x][y] = self.mine_map[x][y]
            self.score += 1

        if self.check_won(self.player_map):
            return True

        return self.player_map

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
