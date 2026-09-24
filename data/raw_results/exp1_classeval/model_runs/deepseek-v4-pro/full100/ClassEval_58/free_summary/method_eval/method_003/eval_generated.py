class MinesweeperGame:
    def __init__(self, n, k):
        self.n = n
        self.k = k
        self.minesweeper_map = self.generate_minesweeper_map()
        self.player_map = [['-' for _ in range(n)] for _ in range(n)]
        self.score = 0

    def generate_minesweeper_map(self):
        import random
        board = [[0 for _ in range(self.n)] for _ in range(self.n)]
        mines = set()
        while len(mines) < self.k:
            x = random.randint(0, self.n - 1)
            y = random.randint(0, self.n - 1)
            if (x, y) not in mines:
                mines.add((x, y))
                board[x][y] = 'X'
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),           (0, 1),
                      (1, -1),  (1, 0),  (1, 1)]
        for x in range(self.n):
            for y in range(self.n):
                if board[x][y] == 'X':
                    continue
                count = 0
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.n and 0 <= ny < self.n and board[nx][ny] == 'X':
                        count += 1
                board[x][y] = count
        return board

    def sweep(self, x, y):
        if self.minesweeper_map[x][y] == 'X':
            return False
        self.player_map[x][y] = self.minesweeper_map[x][y]
        self.score += 1
        if self.check_won():
            return True
        return self.player_map

    def check_won(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.player_map[i][j] == '-' and self.minesweeper_map[i][j] != 'X':
                    return False
        return True

import unittest

class MinesweeperGameTestSweep(unittest.TestCase):
    def test_sweep(self):
        minesweeper_game = MinesweeperGame(3, 1)
        minesweeper_game.minesweeper_map = [['X', 1, 0], [1, 1, 0], [0, 0, 0]]
        minesweeper_game.player_map = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
        self.assertEqual(minesweeper_game.sweep(1,1), [['-', '-', '-'], ['-', 1, '-'], ['-', '-', '-']])
        self.assertEqual(minesweeper_game.score, 1)

    def test_sweep_2(self):
        minesweeper_game = MinesweeperGame(3, 1)
        minesweeper_game.minesweeper_map = [['X', 1, 0], [1, 1, 0], [0, 0, 0]]
        minesweeper_game.player_map = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
        self.assertEqual(minesweeper_game.sweep(0,0), False)
        self.assertEqual(minesweeper_game.score, 0)

    def test_sweep_3(self):
        minesweeper_game = MinesweeperGame(3, 1)
        minesweeper_game.minesweeper_map = [['X', 1, 0], [1, 1, 0], [0, 0, 0]]
        minesweeper_game.player_map = [['-', '-', '0'], ['1', '1', '0'], ['0', '0', '0']]
        self.assertEqual(minesweeper_game.sweep(0,1), True)
        self.assertEqual(minesweeper_game.score, 1)

    def test_sweep_4(self):
        minesweeper_game = MinesweeperGame(3, 1)
        minesweeper_game.minesweeper_map = [['X', 1, 0], [1, 1, 0], [0, 0, 0]]
        minesweeper_game.player_map = [['-', '-', '-'], ['-', '-', '0'], ['0', '0', '0']]
        self.assertEqual(minesweeper_game.sweep(0,2), [['-', '-', 0], ['-', '-', '0'], ['0', '0', '0']])
        self.assertEqual(minesweeper_game.score, 1)

    def test_sweep_5(self):
        minesweeper_game = MinesweeperGame(3, 1)
        minesweeper_game.minesweeper_map = [['X', 1, 0], [1, 1, 0], [0, 0, 0]]
        minesweeper_game.player_map = [['-', '-', '0'], ['-', '1', '0'], ['0', '0', '0']]
        self.assertEqual(minesweeper_game.sweep(1,0), [['-', '-', '0'], [1, '1', '0'], ['0', '0', '0']])
        self.assertEqual(minesweeper_game.score, 1)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
