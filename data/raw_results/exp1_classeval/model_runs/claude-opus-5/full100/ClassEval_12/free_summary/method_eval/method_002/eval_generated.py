import random

class BlackjackGame:
    def __init__(self):
        suits = ['S', 'C', 'D', 'H']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.deck = [f"{rank}{suit}" for suit in suits for rank in ranks]
        random.shuffle(self.deck)
        self.player_hand = []
        self.dealer_hand = []

    def calculate_hand_value(self, hand):
        total = 0
        aces = 0
        for card in hand:
            rank = card[:-1]
            if rank in ('J', 'Q', 'K'):
                total += 10
            elif rank == 'A':
                total += 11
                aces += 1
            else:
                total += int(rank)
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1
        return total

    def check_winner(self, player_hand, dealer_hand):
        player_value = self.calculate_hand_value(player_hand)
        dealer_value = self.calculate_hand_value(dealer_hand)
        player_bust = player_value > 21
        dealer_bust = dealer_value > 21

        if player_bust and dealer_bust:
            if player_value < dealer_value:
                return "player"
            else:
                return "dealer"
        elif player_bust:
            return "dealer"
        elif dealer_bust:
            return "player"
        else:
            if player_value > dealer_value:
                return "player"
            else:
                return "dealer"

import unittest

class BlackjackGameTestCheckWinner(unittest.TestCase):
    def setUp(self):
        self.blackjackGame = BlackjackGame()

    # player > 21 but dealer not, dealer wins.
    def test_check_winner_1(self):
        player_hand = ['2S', 'JS', 'QS']
        dealer_hand = ['7S', '9S']
        self.assertEqual(self.blackjackGame.check_winner(player_hand, dealer_hand), 'Dealer wins')

    # dealer > 21 but player not, player wins.
    def test_check_winner_2(self):
        player_hand = ['2S', '4S', '5S']
        dealer_hand = ['2S', 'JS', 'QS']
        self.assertEqual(self.blackjackGame.check_winner(player_hand, dealer_hand), 'Player wins')

    # both > 21 but dealer smaller, dealer wins.
    def test_check_winner_3(self):
        player_hand = ['3S', 'JS', 'QS']
        dealer_hand = ['2S', 'JS', 'QS']
        self.assertEqual(self.blackjackGame.check_winner(player_hand, dealer_hand), 'Dealer wins')

    # both > 21 but player smaller, player wins.
    def test_check_winner_4(self):
        player_hand = ['2S', 'JS', 'QS']
        dealer_hand = ['3S', 'JS', 'QS']
        self.assertEqual(self.blackjackGame.check_winner(player_hand, dealer_hand), 'Player wins')

    # both < 21 but dealer is bigger, dealer wins.
    def test_check_winner_5(self):
        player_hand = ['2S', '3S', '5S']
        dealer_hand = ['AS', 'JS']
        self.assertEqual(self.blackjackGame.check_winner(player_hand, dealer_hand), 'Dealer wins')

    # both < 21 but player is bigger, player wins.
    def test_check_winner_6(self):
        player_hand = ['AS', 'JS']
        dealer_hand = ['2S', '3S', '5S']
        self.assertEqual(self.blackjackGame.check_winner(player_hand, dealer_hand), 'Player wins')

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
