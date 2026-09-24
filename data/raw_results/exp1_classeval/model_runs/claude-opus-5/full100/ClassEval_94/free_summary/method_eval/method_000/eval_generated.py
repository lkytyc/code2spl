class VendingMachine:
    def __init__(self):
        self.inventory = {}
        self.balance = 0.0

    def add_item(self, name, price, quantity):
        if name in self.inventory:
            self.restock_item(name, quantity)
        else:
            self.inventory[name] = {"price": price, "quantity": quantity}

    def restock_item(self, name, quantity):
        if name not in self.inventory:
            return False
        self.inventory[name]["quantity"] += quantity
        return True

    def insert_coin(self, amount):
        self.balance += amount
        return self.balance

    def purchase_item(self, name):
        if name not in self.inventory:
            return False
        item = self.inventory[name]
        if item["quantity"] <= 0:
            return False
        if self.balance < item["price"]:
            return False
        self.balance -= item["price"]
        item["quantity"] -= 1
        return self.balance

    def display_items(self):
        if not self.inventory:
            return False
        lines = []
        for name, details in self.inventory.items():
            lines.append(
                f"{name} - ${details['price']:.2f} ({details['quantity']} remaining)"
            )
        return "\n".join(lines)

import unittest

class VendingMachineTestAddItem(unittest.TestCase):
    def test_add_item(self):
        vendingMachine = VendingMachine()
        vendingMachine.add_item('Coke', 1.25, 10)
        self.assertEqual(vendingMachine.inventory, {'Coke': {'price': 1.25, 'quantity': 10}})

    def test_add_item_2(self):
        vendingMachine = VendingMachine()
        vendingMachine.add_item('Coke', 1.25, 10)
        vendingMachine.add_item('Coke', 1.25, 10)
        self.assertEqual(vendingMachine.inventory, {'Coke': {'price': 1.25, 'quantity': 20}})

    def test_add_item_3(self):
        vendingMachine = VendingMachine()
        vendingMachine.add_item('Coke', 1.25, 10)
        vendingMachine.add_item('Pizza', 1.25, 10)
        self.assertEqual(vendingMachine.inventory, {'Coke': {'price': 1.25, 'quantity': 10}, 'Pizza': {'price': 1.25, 'quantity': 10}})

    def test_add_item_4(self):
        vendingMachine = VendingMachine()
        vendingMachine.add_item('Coke', 1.25, 10)
        vendingMachine.add_item('Pizza', 1.25, 10)
        vendingMachine.add_item('Pizza', 1.25, 10)
        self.assertEqual(vendingMachine.inventory, {'Coke': {'price': 1.25, 'quantity': 10}, 'Pizza': {'price': 1.25, 'quantity': 20}})

    def test_add_item_5(self):
        vendingMachine = VendingMachine()
        vendingMachine.add_item('Coke', 1.25, 10)
        vendingMachine.add_item('Pizza', 1.25, 10)
        vendingMachine.add_item('Pizza', 1.25, 10)
        vendingMachine.add_item('Coke', 1.25, 10)
        self.assertEqual(vendingMachine.inventory, {'Coke': {'price': 1.25, 'quantity': 20}, 'Pizza': {'price': 1.25, 'quantity': 20}})

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
