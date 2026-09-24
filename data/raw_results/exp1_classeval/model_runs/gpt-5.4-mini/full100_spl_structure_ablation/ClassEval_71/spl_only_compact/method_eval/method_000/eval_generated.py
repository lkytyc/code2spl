class PushBoxGame:
    def __init__(self, map: any):
        self.map = map
        self.player_row = 0
        self.player_col = 0
        self.targets = []
        self.boxes = []
        self.target_count = 0
        self.is_game_over = False
        self.init_game()

    def check_win(self):
        box_on_target_count = 0
        for box in self.boxes:
            if box in self.targets:
                box_on_target_count += 1
        if box_on_target_count == self.target_count:
            self.is_game_over = True
        return self.is_game_over

    def init_game(self):
        for row in range(len(self.map)):
            for col in range(len(self.map[row])):
                cell_value = self.map[row][col]
                if cell_value == "O":
                    self.player_row = row
                    self.player_col = col
                elif cell_value == "G":
                    self.targets.append((row, col))
                    self.target_count += 1
                elif cell_value == "X":
                    self.boxes.append((row, col))

    def move(self, direction: str) -> bool:
        new_player_row = self.player_row
        new_player_col = self.player_col

        if direction == "w":
            new_player_row -= 1
        elif direction == "s":
            new_player_row += 1
        elif direction == "a":
            new_player_col -= 1
        elif direction == "d":
            new_player_col += 1

        movement_allowed = self.map[new_player_row][new_player_col] != "#"
        if movement_allowed:
            if (new_player_row, new_player_col) in self.boxes:
                delta_row = new_player_row - self.player_row
                delta_col = new_player_col - self.player_col
                new_box_row = new_player_row + delta_row
                new_box_col = new_player_col + delta_col
                if self.map[new_box_row][new_box_col] != "#":
                    self.boxes.remove((new_player_row, new_player_col))
                    self.boxes.append((new_box_row, new_box_col))
                    self.player_row = new_player_row
                    self.player_col = new_player_col
            else:
                self.player_row = new_player_row
                self.player_col = new_player_col

        result = self.check_win()
        return result

import unittest

class PushBoxGameTestInitGame(unittest.TestCase):
    def setUp(self) -> None:
        self.game_map = [
            "#####",
            "#O  #",
            "# X #",
            "#  G#",
            "#####"
        ]
        self.game = PushBoxGame(self.game_map)

    def test_init_game_1(self):
        self.assertEqual(self.game.map, self.game_map)

    def test_init_game_2(self):
        self.assertEqual(self.game.is_game_over, False)

    def test_init_game_3(self):
        self.assertEqual(self.game.player_col, 1)

    def test_init_game_4(self):
        self.assertEqual(self.game.player_row, 1)

    def test_init_game_5(self):
        self.assertEqual(self.game.targets, [(3, 3)])

    def test_init_game_6(self):
        self.assertEqual(self.game.boxes, [(2, 2)])

    def test_init_game_7(self):
        self.assertEqual(self.game.target_count, 1)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
