class BlackjackGame:
    def __init__(self):
        self.deck = self.create_deck()
        self.player_hand = []
        self.dealer_hand = []

    def calculate_hand_value(self, hand: list) -> int:
        value = 0
        aces = 0

        for card in hand:
            rank = card[:-1]

            if rank.isdigit():
                value += int(rank)
            elif rank in ("J", "Q", "K"):
                value += 10
            elif rank == "A":
                value += 11
                aces += 1

        while value > 21 and aces > 0:
            value -= 10
            aces -= 1

        return value

    def check_winner(self, player_hand: data, dealer_hand: data) -> string:
        player_value = self.calculate_hand_value(player_hand)
        dealer_value = self.calculate_hand_value(dealer_hand)

        player_over_21 = player_value > 21
        dealer_over_21 = dealer_value > 21

        if player_over_21 and dealer_over_21:
            if player_value <= dealer_value:
                return "Player wins"
            return "Dealer wins"

        if player_over_21:
            return "Dealer wins"

        if dealer_over_21:
            return "Player wins"

        if player_value <= dealer_value:
            return "Dealer wins"

        return "Player wins"

    def create_deck(self) -> list[str]:
        import random

        deck = []
        suits = ["S", "C", "D", "H"]
        ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

        for suit in suits:
            for rank in ranks:
                deck.append(rank + suit)

        random.shuffle(deck)
        return deck

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
