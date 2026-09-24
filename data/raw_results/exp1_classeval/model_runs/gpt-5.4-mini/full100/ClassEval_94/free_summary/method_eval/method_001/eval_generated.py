class VendingMachine:
    def __init__(self):
        self.inventory = {}
        self.balance = 0

    def add_item(self, item_name, price, quantity):
        if item_name in self.inventory:
            self.inventory[item_name]["quantity"] += quantity
        else:
            self.inventory[item_name] = {"price": price, "quantity": quantity}
        return True

    def insert_coin(self, amount):
        self.balance += amount
        return self.balance

    def purchase_item(self, item_name):
        if item_name not in self.inventory:
            return False
        item = self.inventory[item_name]
        if item["quantity"] <= 0 or self.balance < item["price"]:
            return False
        self.balance -= item["price"]
        item["quantity"] -= 1
        return self.balance

    def restock_item(self, item_name, quantity):
        if item_name not in self.inventory:
            return False
        self.inventory[item_name]["quantity"] += quantity
        return True

    def display_items(self):
        if not self.inventory:
            return False
        lines = []
        for item_name, data in self.inventory.items():
            lines.append(f"{item_name}: ${data['price']} ({data['quantity']} in stock)")
        return "\n".join(lines)

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
