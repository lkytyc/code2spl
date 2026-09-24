class EightPuzzle:
    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    def find_blank(self, state):
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    return i, j
        return None

    def move(self, state, direction):
        new_state = [row[:] for row in state]
        row, col = self.find_blank(new_state)

        if direction == "up" and row > 0:
            new_state[row][col], new_state[row - 1][col] = new_state[row - 1][col], new_state[row][col]
        elif direction == "down" and row < 2:
            new_state[row][col], new_state[row + 1][col] = new_state[row + 1][col], new_state[row][col]
        elif direction == "left" and col > 0:
            new_state[row][col], new_state[row][col - 1] = new_state[row][col - 1], new_state[row][col]
        elif direction == "right" and col < 2:
            new_state[row][col], new_state[row][col + 1] = new_state[row][col + 1], new_state[row][col]
        return new_state

    def get_possible_moves(self, state):
        row, col = self.find_blank(state)
        moves = []
        if row > 0:
            moves.append("up")
        if row < 2:
            moves.append("down")
        if col > 0:
            moves.append("left")
        if col < 2:
            moves.append("right")
        return moves

    def solve(self):
        start_state = [row[:] for row in self.initial_state]
        queue = [(start_state, [])]
        closed = []

        while queue:
            state, path = queue.pop(0)

            if state == self.goal_state:
                return path

            state_key = tuple(tuple(row) for row in state)
            if state_key in closed:
                continue
            closed.append(state_key)

            for move in self.get_possible_moves(state):
                new_state = self.move(state, move)
                new_key = tuple(tuple(row) for row in new_state)
                if new_key not in closed:
                    queue.append((new_state, path + [move]))

        return None

import unittest

class EightPuzzleTestSolve(unittest.TestCase):
    def test_solve_1(self):
        eightPuzzle = EightPuzzle([[1, 2, 3], [4, 5, 6], [7, 0, 8]])
        result = eightPuzzle.solve()
        expected = ['right']
        self.assertEqual(result, expected)

    def test_solve_2(self):
        eightPuzzle = EightPuzzle([[1, 2, 3], [4, 0, 6], [7, 5, 8]])
        result = eightPuzzle.solve()
        expected = ['down', 'right']
        self.assertEqual(result, expected)

    def test_solve_3(self):
        eightPuzzle = EightPuzzle([[1, 2, 3], [0, 4, 5], [6, 7, 8]])
        result = eightPuzzle.solve()
        expected = ['right', 'right', 'down', 'left', 'left', 'up', 'right', 'down', 'right', 'up', 'left', 'left', 'down', 'right', 'right']
        self.assertEqual(result, expected)

    def test_solve_4(self):
        eightPuzzle = EightPuzzle([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
        result = eightPuzzle.solve()
        expected = []
        self.assertEqual(result, expected)

    def test_solve_5(self):
        eightPuzzle = EightPuzzle([[1, 2, 3], [4, 5, 6], [0, 7, 8]])
        result = eightPuzzle.solve()
        expected = ['right', 'right']
        self.assertEqual(result, expected)

    def test_solve_6(self):
        eightPuzzle = EightPuzzle([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        result = eightPuzzle.solve()
        expected = None
        self.assertEqual(result, expected)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
