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
