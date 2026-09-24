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

class MinesweeperGameTestMain(unittest.TestCase):
    def test_minesweeper_main(self):
        minesweeper_game = MinesweeperGame(3, 1)
        length = len(minesweeper_game.minesweeper_map)
        mine_num = 0
        for row in minesweeper_game.minesweeper_map:
            for cell in row:
                if cell == 'X':
                    mine_num += 1
        self.assertEqual(3, length)
        self.assertEqual(1, mine_num)
        self.assertEqual(minesweeper_game.generate_playerMap(), [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']])
        minesweeper_game.minesweeper_map = [['X', 1, 0], [1, 1, 0], [0, 0, 0]]
        minesweeper_game.player_map = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
        self.assertEqual(minesweeper_game.check_won(minesweeper_game.player_map), False)
        self.assertEqual(minesweeper_game.sweep(1,1), [['-', '-', '-'], ['-', 1, '-'], ['-', '-', '-']])
        self.assertEqual(minesweeper_game.score, 1)

    def test_minesweeper_main_2(self):
        minesweeper_game = MinesweeperGame(3, 2)
        length = len(minesweeper_game.minesweeper_map)
        mine_num = 0
        for row in minesweeper_game.minesweeper_map:
            for cell in row:
                if cell == 'X':
                    mine_num += 1
        self.assertEqual(3, length)
        self.assertEqual(2, mine_num)
        self.assertEqual(minesweeper_game.generate_playerMap(), [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']])
        minesweeper_game.minesweeper_map = [['X', 1, 1], [1, 'X', 1], [1, 1, 1]]
        self.assertEqual(minesweeper_game.check_won(minesweeper_game.player_map), False)
        self.assertEqual(minesweeper_game.sweep(0, 1), [['-', 1, '-'], ['-','-', '-'], ['-', '-', '-']])
        self.assertEqual(minesweeper_game.score, 1)
        self.assertEqual(minesweeper_game.sweep(0, 2), [['-', 1, 1], ['-', '-', '-'], ['-', '-', '-']])
        self.assertEqual(minesweeper_game.score, 2)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
