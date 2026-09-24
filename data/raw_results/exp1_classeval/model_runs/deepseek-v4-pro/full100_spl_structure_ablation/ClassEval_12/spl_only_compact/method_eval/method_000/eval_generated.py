import random

class BlackjackGame:
    def __init__(self):
        self.deck = self.create_deck()
        self.player_hand = []
        self.dealer_hand = []

    def calculate_hand_value(self, hand: list) -> int:
        value = 0
        num_aces = 0
        for card in hand:
            rank = card[:-1]
            if rank.isdigit():
                value += int(rank)
            elif rank in ('J', 'Q', 'K'):
                value += 10
            elif rank == 'A':
                value += 11
                num_aces += 1
        while value > 21 and num_aces > 0:
            value -= 10
            num_aces -= 1
        return value

    def check_winner(self, player_hand: object, dealer_hand: object) -> str:
        player_value = self.calculate_hand_value(player_hand)
        dealer_value = self.calculate_hand_value(dealer_hand)
        if player_value > 21 and dealer_value > 21:
            if player_value <= dealer_value:
                return 'Player wins'
            else:
                return 'Dealer wins'
        elif player_value > 21:
            return 'Dealer wins'
        elif dealer_value > 21:
            return 'Player wins'
        else:
            if player_value <= dealer_value:
                return 'Dealer wins'
            else:
                return 'Player wins'

    def create_deck(self) -> list[str]:
        deck = []
        suits = ['S', 'C', 'D', 'H']
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        for suit in suits:
            for rank in ranks:
                deck.append(rank + suit)
        random.shuffle(deck)
        return deck

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
