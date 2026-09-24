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
        self.targets = []
        self.boxes = []
        self.target_count = 0
        self.is_game_over = False
        for r, row in enumerate(self.map):
            for c, ch in enumerate(row):
                if ch == 'O':
                    self.player_row = r
                    self.player_col = c
                elif ch == 'G':
                    self.targets.append((r, c))
                    self.target_count += 1
                elif ch == 'X':
                    self.boxes.append((r, c))

    def check_win(self):
        """
        Check if the game is won. The game is won when all the boxes are placed on target positions.
        And update the value of self.is_game_over.
        :return self.is_game_over: True if all the boxes are placed on target positions, or False otherwise.
        >>> game = PushBoxGame(["#####", "#O  #", "# X #", "#  G#", "#####"]) 
        >>> game.check_win()
        """
        self.is_game_over = len(self.boxes) == self.target_count and all(box in self.targets for box in self.boxes)
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
        if self.is_game_over:
            return True

        delta = {'w': (-1, 0), 's': (1, 0), 'a': (0, -1), 'd': (0, 1)}
        if direction not in delta:
            return self.check_win()

        dr, dc = delta[direction]
        nr = self.player_row + dr
        nc = self.player_col + dc

        if nr < 0 or nr >= len(self.map) or nc < 0 or nc >= len(self.map[nr]) or self.map[nr][nc] == '#':
            return self.check_win()

        if (nr, nc) in self.boxes:
            br = nr + dr
            bc = nc + dc
            if br < 0 or br >= len(self.map) or bc < 0 or bc >= len(self.map[br]) or self.map[br][bc] == '#' or (br, bc) in self.boxes:
                return self.check_win()
            self.boxes = [(br, bc) if box == (nr, nc) else box for box in self.boxes]

        self.player_row = nr
        self.player_col = nc
        return self.check_win()

    def print_map(self):
        for r, row in enumerate(self.map):
            line = []
            for c, ch in enumerate(row):
                if r == self.player_row and c == self.player_col:
                    line.append('O')
                elif (r, c) in self.boxes:
                    line.append('X')
                elif (r, c) in self.targets:
                    line.append('G')
                else:
                    line.append(ch)
            print(' '.join(line), end=' \n')

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
