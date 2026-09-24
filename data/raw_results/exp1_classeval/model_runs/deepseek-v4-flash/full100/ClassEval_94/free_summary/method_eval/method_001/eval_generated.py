class VendingMachine:
    def __init__(self):
        self.items = {}
        self.balance = 0

    def add_item(self, name, price, quantity):
        if name in self.items:
            self.items[name]["quantity"] += quantity
        else:
            self.items[name] = {"price": price, "quantity": quantity}

    def insert_coin(self, coin):
        self.balance += coin
        return self.balance

    def purchase_item(self, name):
        if name not in self.items:
            return False
        if self.items[name]["quantity"] <= 0:
            return False
        if self.balance < self.items[name]["price"]:
            return False

        self.balance -= self.items[name]["price"]
        self.items[name]["quantity"] -= 1
        return self.balance

    def restock_item(self, name, quantity):
        if name not in self.items:
            return False

        self.items[name]["quantity"] += quantity
        return True

    def display_items(self):
        if not self.items:
            return False

        return [
            f"{name} - ${self.items[name]['price']} - {self.items[name]['quantity']}"
            for name in self.items
        ]

import unittest

class VendingMachineTestInsertCoin(unittest.TestCase):
    def test_insert_coin(self):
        vendingMachine = VendingMachine()
        self.assertEqual(vendingMachine.insert_coin(1.25), 1.25)

    def test_insert_coin_2(self):
        vendingMachine = VendingMachine()
        self.assertEqual(vendingMachine.insert_coin(2.5), 2.5)

    def test_insert_coin_3(self):
        vendingMachine = VendingMachine()
        vendingMachine.insert_coin(1.25)
        vendingMachine.insert_coin(1.25)
        self.assertEqual(vendingMachine.balance, 2.50)

    def test_insert_coin_4(self):
        vendingMachine = VendingMachine()
        vendingMachine.balance = 1.25
        vendingMachine.insert_coin(1.25)
        vendingMachine.insert_coin(1.25)
        vendingMachine.insert_coin(1.25)
        self.assertEqual(vendingMachine.balance, 5.0)

    def test_insert_coin_5(self):
        vendingMachine = VendingMachine()
        vendingMachine.balance = 1.25
        vendingMachine.insert_coin(1.25)
        vendingMachine.insert_coin(1.25)
        vendingMachine.insert_coin(1.25)
        vendingMachine.insert_coin(1.25)
        self.assertEqual(vendingMachine.balance, 6.25)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
