class Puzzle8:
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
        blank_row, blank_col = self.find_blank(state)
        new_state = [row[:] for row in state]
        if direction == 'up':
            new_row, new_col = blank_row - 1, blank_col
        elif direction == 'down':
            new_row, new_col = blank_row + 1, blank_col
        elif direction == 'left':
            new_row, new_col = blank_row, blank_col - 1
        elif direction == 'right':
            new_row, new_col = blank_row, blank_col + 1
        else:
            return new_state
        new_state[blank_row][blank_col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[blank_row][blank_col]
        return new_state

    def get_possible_moves(self, state):
        blank_row, blank_col = self.find_blank(state)
        moves = []
        if blank_row > 0:
            moves.append('up')
        if blank_row < 2:
            moves.append('down')
        if blank_col > 0:
            moves.append('left')
        if blank_col < 2:
            moves.append('right')
        return moves

    def solve(self):
        open_list = [(self.initial_state, [])]
        closed_list = []
        while open_list:
            current_state, path = open_list.pop(0)
            if current_state == self.goal_state:
                return path
            if current_state in closed_list:
                continue
            closed_list.append(current_state)
            for direction in self.get_possible_moves(current_state):
                new_state = self.move(current_state, direction)
                if new_state not in closed_list:
                    open_list.append((new_state, path + [direction]))
        return None

import unittest

class EightPuzzleTestFindBlank(unittest.TestCase):
    def test_find_blank_1(self):
        state = [[2, 3, 4], [5, 8, 1], [6, 0, 7]]
        eightPuzzle = EightPuzzle(state)
        self.assertEqual(eightPuzzle.find_blank(state), (2, 1))

    def test_find_blank_2(self):
        state = [[2, 3, 4], [5, 0, 1], [6, 8, 7]]
        eightPuzzle = EightPuzzle(state)
        self.assertEqual(eightPuzzle.find_blank(state), (1, 1))

    def test_find_blank_3(self):
        state = [[2, 3, 4], [5, 8, 1], [6, 8, 7]]
        eightPuzzle = EightPuzzle(state)
        self.assertEqual(eightPuzzle.find_blank(state), None)

    def test_find_blank_4(self):
        state = [[2, 3, 4], [5, 8, 1], [6, 8, 7]]
        eightPuzzle = EightPuzzle(state)
        self.assertEqual(eightPuzzle.find_blank(state), None)

    def test_find_blank_5(self):
        state = [[2, 3, 4], [5, 8, 1], [6, 8, 7]]
        eightPuzzle = EightPuzzle(state)
        self.assertEqual(eightPuzzle.find_blank(state), None)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
