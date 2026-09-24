import random


class BlackjackGame:
    def __init__(self):
        self.deck = self.create_deck()
        self.player_hand = []
        self.dealer_hand = []

    def create_deck(self):
        suits = ["S", "C", "D", "H"]
        ranks = ["A"] + [str(i) for i in range(2, 11)] + ["J", "Q", "K"]
        deck = [rank + suit for suit in suits for rank in ranks]
        random.shuffle(deck)
        return deck

    def calculate_hand_value(self, hand):
        total = 0
        aces = 0

        for card in hand:
            rank = card[:-1]

            if rank == "A":
                total += 11
                aces += 1
            elif rank in {"J", "Q", "K"}:
                total += 10
            else:
                total += int(rank)

        while total > 21 and aces > 0:
            total -= 10
            aces -= 1

        return total

    def check_winner(self, player_hand, dealer_hand):
        player_total = self.calculate_hand_value(player_hand)
        dealer_total = self.calculate_hand_value(dealer_hand)

        if player_total > 21 and dealer_total > 21:
            if player_total <= dealer_total:
                return "Player wins"
            return "Dealer wins"
        if player_total > 21:
            return "Dealer wins"
        if dealer_total > 21:
            return "Player wins"
        if player_total > dealer_total:
            return "Player wins"
        return "Dealer wins"

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
