import random

class Blackjack:
    def __init__(self):
        self.deck = self.create_deck()
        self.player_hand = []
        self.dealer_hand = []

    def create_deck(self):
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        suits = ['H', 'D', 'C', 'S']
        deck = [rank + suit for suit in suits for rank in ranks]
        random.shuffle(deck)
        return deck

    def calculate_hand_value(self, hand):
        total = 0
        aces = 0
        for card in hand:
            rank = card[:-1]
            if rank in ['J', 'Q', 'K']:
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
        player_val = self.calculate_hand_value(player_hand)
        dealer_val = self.calculate_hand_value(dealer_hand)
        player_bust = player_val > 21
        dealer_bust = dealer_val > 21

        if player_bust and dealer_bust:
            if player_val <= dealer_val:
                return 'Player wins'
            return 'Dealer wins'
        elif player_bust:
            return 'Dealer wins'
        elif dealer_bust:
            return 'Player wins'
        else:
            if player_val > dealer_val:
                return 'Player wins'
            return 'Dealer wins'

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
