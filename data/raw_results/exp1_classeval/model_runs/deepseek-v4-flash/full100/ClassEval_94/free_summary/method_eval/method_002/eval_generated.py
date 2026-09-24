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

class VendingMachineTestPurchaseItem(unittest.TestCase):
    def test_purchase_item(self):
        vendingMachine = VendingMachine()
        vendingMachine.inventory = {'Coke': {'price': 1.25, 'quantity': 10}}
        vendingMachine.balance = 1.25
        self.assertEqual(vendingMachine.purchase_item('Coke'), 0.0)
        self.assertEqual(vendingMachine.inventory, {'Coke': {'price': 1.25, 'quantity': 9}})

    def test_purchase_item_2(self):
        vendingMachine = VendingMachine()
        vendingMachine.inventory = {'Coke': {'price': 1.25, 'quantity': 10}}
        vendingMachine.balance = 1.25
        self.assertEqual(vendingMachine.purchase_item('Pizza'), False)
        self.assertEqual(vendingMachine.inventory, {'Coke': {'price': 1.25, 'quantity': 10}})

    def test_purchase_item_3(self):
        vendingMachine = VendingMachine()
        vendingMachine.inventory = {'Coke': {'price': 1.25, 'quantity': 10}}
        vendingMachine.balance = 0
        self.assertEqual(vendingMachine.purchase_item('Coke'), False)
        self.assertEqual(vendingMachine.inventory, {'Coke': {'price': 1.25, 'quantity': 10}})

    def test_purchase_item_4(self):
        vendingMachine = VendingMachine()
        vendingMachine.inventory = {'Coke': {'price': 1.25, 'quantity': 0}}
        vendingMachine.balance = 1.25
        self.assertEqual(vendingMachine.purchase_item('Coke'), False)
        self.assertEqual(vendingMachine.inventory, {'Coke': {'price': 1.25, 'quantity': 0}})

    def test_purchase_item_5(self):
        vendingMachine = VendingMachine()
        vendingMachine.inventory = {'Coke': {'price': 1.25, 'quantity': 10}, 'Pizza': {'price': 1.25, 'quantity': 10}}
        vendingMachine.balance = 1.25
        self.assertEqual(vendingMachine.purchase_item('Pizza'), 0.0)
        self.assertEqual(vendingMachine.inventory, {'Coke': {'price': 1.25, 'quantity': 10}, 'Pizza': {'price': 1.25, 'quantity': 9}})

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
