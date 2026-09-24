import random

class MinesweeperGame:
    def __init__(self, n, k):
        self.n = n
        self.k = k
        self.minesweeper_map = [['0' for _ in range(n)] for _ in range(n)]
        self.player_map = [['-' for _ in range(n)] for _ in range(n)]
        self.score = 0
        self.game_over = False

        mines_placed = 0
        while mines_placed < k:
            row = random.randint(0, n - 1)
            col = random.randint(0, n - 1)
            if self.minesweeper_map[row][col] != 'X':
                self.minesweeper_map[row][col] = 'X'
                mines_placed += 1

        for i in range(n):
            for j in range(n):
                if self.minesweeper_map[i][j] != 'X':
                    count = 0
                    for di in [-1, 0, 1]:
                        for dj in [-1, 0, 1]:
                            ni, nj = i + di, j + dj
                            if 0 <= ni < n and 0 <= nj < n and self.minesweeper_map[ni][nj] == 'X':
                                count += 1
                    self.minesweeper_map[i][j] = str(count)

    def check_won(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.minesweeper_map[i][j] != 'X' and self.player_map[i][j] == '-':
                    return False
        return True

    def sweep(self, x, y):
        if self.game_over:
            return self.player_map
        if self.minesweeper_map[x][y] == 'X':
            self.game_over = True
            return False
        if self.player_map[x][y] == '-':
            self.player_map[x][y] = self.minesweeper_map[x][y]
            self.score += 1
        if self.check_won():
            return True
        return self.player_map

import unittest

class MinesweeperGameTestGenerateMineSweeperMap(unittest.TestCase):
    def test_generate_mine_sweeper_map(self):
        minesweeper_game = MinesweeperGame(3, 2)
        length = len(minesweeper_game.minesweeper_map)
        mine_num = 0
        for row in minesweeper_game.minesweeper_map:
            for cell in row:
                if cell == 'X':
                    mine_num += 1
        self.assertEqual(3, length)
        self.assertEqual(2, mine_num)

    def test_generate_mine_sweeper_map_2(self):
        minesweeper_game = MinesweeperGame(3, 1)
        length = len(minesweeper_game.minesweeper_map)
        mine_num = 0
        for row in minesweeper_game.minesweeper_map:
            for cell in row:
                if cell == 'X':
                    mine_num += 1
        self.assertEqual(3, length)
        self.assertEqual(1, mine_num)

    def test_generate_mine_sweeper_map_3(self):
        minesweeper_game = MinesweeperGame(3, 0)
        length = len(minesweeper_game.minesweeper_map)
        mine_num = 0
        for row in minesweeper_game.minesweeper_map:
            for cell in row:
                if cell == 'X':
                    mine_num += 1
        self.assertEqual(3, length)
        self.assertEqual(0, mine_num)

    def test_generate_mine_sweeper_map_4(self):
        minesweeper_game = MinesweeperGame(5, 1)
        length = len(minesweeper_game.minesweeper_map)
        mine_num = 0
        for row in minesweeper_game.minesweeper_map:
            for cell in row:
                if cell == 'X':
                    mine_num += 1
        self.assertEqual(length,5)
        self.assertEqual(mine_num, 1)

    def test_generate_mine_sweeper_map_5(self):
        minesweeper_game = MinesweeperGame(4, 1)
        length = len(minesweeper_game.minesweeper_map)
        mine_num = 0
        for row in minesweeper_game.minesweeper_map:
            for cell in row:
                if cell == 'X':
                    mine_num += 1
        self.assertEqual(length, 4)
        self.assertEqual(mine_num, 1)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
