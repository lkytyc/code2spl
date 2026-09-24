class EightPuzzle:
    def __init__(self, initial):
        self.initial = initial
        self.goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    def find_blank(self, state):
        for r in range(3):
            for c in range(3):
                if state[r][c] == 0:
                    return r, c

    def move(self, state, direction):
        import copy
        r, c = self.find_blank(state)
        new_state = copy.deepcopy(state)
        if direction == 'up':
            new_state[r][c], new_state[r - 1][c] = new_state[r - 1][c], new_state[r][c]
        elif direction == 'down':
            new_state[r][c], new_state[r + 1][c] = new_state[r + 1][c], new_state[r][c]
        elif direction == 'left':
            new_state[r][c], new_state[r][c - 1] = new_state[r][c - 1], new_state[r][c]
        elif direction == 'right':
            new_state[r][c], new_state[r][c + 1] = new_state[r][c + 1], new_state[r][c]
        return new_state

    def get_possible_moves(self, state):
        r, c = self.find_blank(state)
        moves = []
        if r > 0:
            moves.append('up')
        if r < 2:
            moves.append('down')
        if c > 0:
            moves.append('left')
        if c < 2:
            moves.append('right')
        return moves

    def solve(self):
        start = self.initial
        goal = self.goal

        open_list = [(start, [])]
        closed_list = []

        while open_list:
            state, path = open_list.pop(0)

            if state == goal:
                return path

            if state in closed_list:
                continue
            closed_list.append(state)

            for direction in self.get_possible_moves(state):
                next_state = self.move(state, direction)
                if next_state not in closed_list:
                    open_list.append((next_state, path + [direction]))

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
