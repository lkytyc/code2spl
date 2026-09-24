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

class BlackjackGameTestCreateDeck(unittest.TestCase):
    def setUp(self):
        self.blackjackGame = BlackjackGame()
        self.deck = self.blackjackGame.deck

    def test_create_deck_1(self):
        self.assertEqual(len(self.deck), 52)

    def test_create_deck_2(self):
        suits = ['S', 'C', 'D', 'H']
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        for suit in suits:
            for rank in ranks:
                self.assertIn(rank + suit, self.deck)

    def test_create_deck_3(self):
        suits = ['S', 'C', 'D', 'H']
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9']
        for suit in suits:
            for rank in ranks:
                self.assertIn(rank + suit, self.deck)

    def test_create_deck_4(self):
        suits = ['S', 'C', 'D', 'H']
        ranks = ['10', 'J', 'Q', 'K']
        for suit in suits:
            for rank in ranks:
                self.assertIn(rank + suit, self.deck)

    def test_create_deck_5(self):
        suits = ['S', 'C', 'D', 'H']
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9']
        for suit in suits:
            for rank in ranks:
                self.assertIn(rank + suit, self.deck)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
