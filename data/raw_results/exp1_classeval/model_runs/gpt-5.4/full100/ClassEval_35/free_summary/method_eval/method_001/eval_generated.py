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

    def move(self, state, direction):
        row, col = self.find_blank(state)
        new_state = [r[:] for r in state]

        if direction == "up":
            new_row, new_col = row - 1, col
        elif direction == "down":
            new_row, new_col = row + 1, col
        elif direction == "left":
            new_row, new_col = row, col - 1
        elif direction == "right":
            new_row, new_col = row, col + 1
        else:
            return new_state

        new_state[row][col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[row][col]
        return new_state

    def solve(self):
        open_list = [(self.initial_state, [])]
        closed_list = []

        while open_list:
            current_state, path = open_list.pop(0)

            if current_state == self.goal_state:
                return path

            closed_list.append(current_state)

            for move in self.get_possible_moves(current_state):
                new_state = self.move(current_state, move)
                if new_state not in closed_list:
                    open_list.append((new_state, path + [move]))

        return None

import unittest

class EightPuzzleTestMove(unittest.TestCase):
    def setUp(self):
        self.initial_state = [[2, 3, 4], [5, 0, 1], [6, 8, 7]]
        self.eightPuzzle = EightPuzzle(self.initial_state)

    def test_move_1(self):
        result = self.eightPuzzle.move(self.initial_state, 'up')
        expected = [[2, 0, 4], [5, 3, 1], [6, 8, 7]]
        self.assertEqual(result, expected)

    def test_move_2(self):
        result = self.eightPuzzle.move(self.initial_state, 'down')
        expected = [[2, 3, 4], [5, 8, 1], [6, 0, 7]]
        self.assertEqual(result, expected)

    def test_move_3(self):
        result = self.eightPuzzle.move(self.initial_state, 'left')
        expected = [[2, 3, 4], [0, 5, 1], [6, 8, 7]]
        self.assertEqual(result, expected)

    def test_move_4(self):
        result = self.eightPuzzle.move(self.initial_state, 'right')
        expected = [[2, 3, 4], [5, 1, 0], [6, 8, 7]]
        self.assertEqual(result, expected)

    def test_move_5(self):
        result = self.eightPuzzle.move(self.initial_state, '???')
        expected = [[2, 3, 4], [5, 0, 1], [6, 8, 7]]
        self.assertEqual(result, expected)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
