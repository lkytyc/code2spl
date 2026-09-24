class PushBoxGame:
    """
    This class implements a functionality of a sokoban game, where the player needs to move boxes to designated targets in order to win.
    """

    def __init__(self, map):
        """
        Initialize the push box game with the map and various attributes.
        :param map: list[str], the map of the push box game, represented as a list of strings. 
            Each character on the map represents a different element, including the following:
            - '#' represents a wall that neither the player nor the box can pass through;
            - 'O' represents the initial position of the player;
            - 'G' represents the target position;
            - 'X' represents the initial position of the box.
        >>> map = ["#####", "#O  #", "# X #", "#  G#", "#####"]   
        >>> game = PushBoxGame(map)                
        """
        self.map = map
        self.player_row = 0
        self.player_col = 0
        self.targets = []
        self.boxes = []
        self.target_count = 0
        self.is_game_over = False
        self.init_game()

    def init_game(self):
        """
        Initialize the game by setting the positions of the player, targets, and boxes based on the map.
        >>> game = PushBoxGame(["#####", "#O  #", "# X #", "#  G#", "#####"]) 
        >>> game.targets
        [(3, 3)]
        >>> game.boxes
        [(2, 2)]
        >>> game.player_row
        1
        >>> game.player_col
        1
        """
        for row_idx, row in enumerate(self.map):
            for col_idx, cell in enumerate(row):
                if cell == 'O':
                    self.player_row = row_idx
                    self.player_col = col_idx
                elif cell == 'G':
                    self.targets.append((row_idx, col_idx))
                elif cell == 'X':
                    self.boxes.append((row_idx, col_idx))
        self.target_count = len(self.targets)

    def check_win(self):
        """
        Check if the game is won. The game is won when all the boxes are placed on target positions.
        And update the value of self.is_game_over.
        :return self.is_game_over: True if all the boxes are placed on target positions, or False otherwise.
        >>> game = PushBoxGame(["#####", "#O  #", "# X #", "#  G#", "#####"]) 
        >>> game.check_win()
        """
        for box in self.boxes:
            if box not in self.targets:
                self.is_game_over = False
                return self.is_game_over
        self.is_game_over = True
        return self.is_game_over

    def move(self, direction):
        """
        Move the player based on the specified direction and check if the game is won.
        :param direction: str, the direction of the player's movement. 
            It can be 'w', 's', 'a', or 'd' representing up, down, left, or right respectively.

        :return: True if the game is won, False otherwise.
        >>> game = PushBoxGame(["#####", "#O  #", "# X #", "#  G#", "#####"])       
        >>> game.print_map()
        # # # # # 
        # O     #
        #   X   #
        #     G #
        # # # # #
        >>> game.move('d')
        False
        >>> game.move('s')   
        False
        >>> game.move('a')   
        False
        >>> game.move('s') 
        False
        >>> game.move('d') 
        True
        """
        direction_map = {
            'w': (-1, 0),
            's': (1, 0),
            'a': (0, -1),
            'd': (0, 1),
        }

        if direction not in direction_map:
            return self.is_game_over

        dr, dc = direction_map[direction]
        new_player_row = self.player_row + dr
        new_player_col = self.player_col + dc

        # Check if new position is a wall
        if self.map[new_player_row][new_player_col] == '#':
            return self.is_game_over

        # Check if new position has a box
        if (new_player_row, new_player_col) in self.boxes:
            # Calculate where the box would be pushed to
            new_box_row = new_player_row + dr
            new_box_col = new_player_col + dc

            # Can't push box into a wall or another box
            if self.map[new_box_row][new_box_col] == '#':
                return self.is_game_over
            if (new_box_row, new_box_col) in self.boxes:
                return self.is_game_over

            # Move the box
            box_idx = self.boxes.index((new_player_row, new_player_col))
            self.boxes[box_idx] = (new_box_row, new_box_col)

        # Move the player
        self.player_row = new_player_row
        self.player_col = new_player_col

        return self.check_win()

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


class PushBoxGameTestCheckWin(unittest.TestCase):
    def setUp(self) -> None:
        self.game_map = [
            "#####",
            "#O  #",
            "# X #",
            "#  G#",
            "#####"
        ]
        self.game = PushBoxGame(self.game_map)

    def test_check_win_1(self):
        self.assertFalse(self.game.check_win())

    def test_check_win_2(self):
        moves = ['d', 's', 'a', 's', 'd']
        for move in moves:
            self.game.move(move)
        self.assertTrue(self.game.check_win())

class PushBoxGameTestMove(unittest.TestCase):
    def setUp(self) -> None:
        self.game_map = [
            "#####",
            "#O  #",
            "# X #",
            "#  G#",
            "#####"
        ]
        self.game = PushBoxGame(self.game_map)

    def test_move_1(self):
        moves = ['d', 's', 'a', 's']
        for move in moves:
            self.assertFalse(self.game.move(move))
        self.assertTrue(self.game.move('d'))

    def test_move_2(self):
        self.game.move('a')
        self.assertEqual(self.game.player_col, 1)
        self.assertEqual(self.game.player_row, 1)
        self.assertFalse(self.game.is_game_over)

    def test_move_3(self):
        self.game.move('d')
        self.assertEqual(self.game.player_col, 2)
        self.assertEqual(self.game.player_row, 1)
        self.assertFalse(self.game.is_game_over)

    def test_move_4(self):
        self.game.move('s')
        self.assertEqual(self.game.player_col, 1)
        self.assertEqual(self.game.player_row, 2)
        self.assertFalse(self.game.is_game_over)

    def test_move_5(self):
        self.game.move('w')
        self.assertEqual(self.game.player_col, 1)
        self.assertEqual(self.game.player_row, 1)
        self.assertFalse(self.game.is_game_over)

    def test_move_6(self):
        self.game.move('?')
        self.assertFalse(self.game.is_game_over)

    def test_move_7(self):
        self.game_map = [
            "#####",
            "# X #",
            "# O #",
            "#  G#",
            "#####"
        ]
        self.game = PushBoxGame(self.game_map)
        self.game.move('w')
        self.assertEqual(self.game.player_col, 2)
        self.assertEqual(self.game.player_row, 2)
        self.assertFalse(self.game.is_game_over)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
