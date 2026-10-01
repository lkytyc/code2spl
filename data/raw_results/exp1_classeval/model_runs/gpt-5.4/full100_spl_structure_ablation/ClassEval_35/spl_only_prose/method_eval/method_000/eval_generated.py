class EightPuzzle:
    def __init__(self, initial_state: any):
        self.initial_state = initial_state
        self.goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    def find_blank(self, state: grid) -> tuple or None:
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    return i, j

    def get_possible_moves(self, state: object) -> list:
        moves = []
        i, j = self.find_blank(state)

        if i > 0:
            moves.append("up")
        if i < 2:
            moves.append("down")
        if j > 0:
            moves.append("left")
        if j < 2:
            moves.append("right")

        return moves

    def move(self, state: grid, direction: string) -> grid:
        i, j = self.find_blank(state)
        new_state = [row[:] for row in state]

        if direction == "up":
            new_state[i][j], new_state[i - 1][j] = (
                new_state[i - 1][j],
                new_state[i][j],
            )
        elif direction == "down":
            new_state[i][j], new_state[i + 1][j] = (
                new_state[i + 1][j],
                new_state[i][j],
            )
        elif direction == "left":
            new_state[i][j], new_state[i][j - 1] = (
                new_state[i][j - 1],
                new_state[i][j],
            )
        elif direction == "right":
            new_state[i][j], new_state[i][j + 1] = (
                new_state[i][j + 1],
                new_state[i][j],
            )

        return new_state

    def solve(self):
        open_list = [(self.initial_state, [])]
        closed_list = []

        while open_list:
            current_state, path = open_list.pop(0)
            closed_list.append(current_state)

            if current_state == self.goal_state:
                return path

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
