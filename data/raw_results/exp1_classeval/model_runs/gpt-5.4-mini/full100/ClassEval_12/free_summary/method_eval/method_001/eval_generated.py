class BlackjackGame:
    def __init__(self):
        self.deck = self.create_deck()
        self.player_hand = []
        self.dealer_hand = []

    def create_deck(self):
        suits = ['S', 'C', 'D', 'H']
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        deck = [rank + suit for suit in suits for rank in ranks]
        import random
        random.shuffle(deck)
        return deck

    def calculate_hand_value(self, hand):
        value = 0
        aces = 0

        for card in hand:
            rank = card[:-1]
            if rank in ('J', 'Q', 'K'):
                value += 10
            elif rank == 'A':
                value += 11
                aces += 1
            else:
                value += int(rank)

        while value > 21 and aces > 0:
            value -= 10
            aces -= 1

        return value

    def check_winner(self, player_hand, dealer_hand):
        player_value = self.calculate_hand_value(player_hand)
        dealer_value = self.calculate_hand_value(dealer_hand)

        if player_value > 21 and dealer_value <= 21:
            return 'Dealer wins'
        if dealer_value > 21 and player_value <= 21:
            return 'Player wins'
        if player_value > 21 and dealer_value > 21:
            return 'Player wins' if player_value < dealer_value else 'Dealer wins'

        return 'Player wins' if player_value > dealer_value else 'Dealer wins'

import unittest

class BlackjackGameTestCalculateHandValue(unittest.TestCase):
    def test_calculate_hand_value_1(self):
        blackjackGame = BlackjackGame()
        hand = ['2S', '3S', '4S', '5S']
        self.assertEqual(blackjackGame.calculate_hand_value(hand), 14)

    def test_calculate_hand_value_2(self):
        blackjackGame = BlackjackGame()
        hand = ['2S', '3S', 'JS', 'QS']
        self.assertEqual(blackjackGame.calculate_hand_value(hand), 25)

    def test_calculate_hand_value_3(self):
        blackjackGame = BlackjackGame()
        hand = ['2S', '3S', '4S', 'AS']
        self.assertEqual(blackjackGame.calculate_hand_value(hand), 20)

    def test_calculate_hand_value_4(self):
        blackjackGame = BlackjackGame()
        hand = ['JS', 'QS', '4S', 'AS']
        self.assertEqual(blackjackGame.calculate_hand_value(hand), 25)

    def test_calculate_hand_value_5(self):
        blackjackGame = BlackjackGame()
        hand = ['JS', 'QS', 'AS', 'AS', 'AS']
        self.assertEqual(blackjackGame.calculate_hand_value(hand), 23)

    def test_calculate_hand_value_6(self):
        blackjackGame = BlackjackGame()
        hand = ['JS', 'QS', 'BS', 'CS']
        self.assertEqual(blackjackGame.calculate_hand_value(hand), 20)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
