class VendingMachine:
    def __init__(self):
        self.inventory = {}
        self.balance = 0

    def add_item(self, item_name, price, quantity):
        restock_result = self.restock_item(item_name, quantity)
        should_create_item = not restock_result
        if should_create_item:
            self.inventory[item_name] = {
                "price": price,
                "quantity": quantity,
            }

    def display_items(self):
        inventory_is_empty = not self.inventory
        if inventory_is_empty:
            return False

        items = []
        for item_name, item_info in self.inventory.items():
            items.append(
                f"{item_name} - ${item_info['price']} [{item_info['quantity']}]"
            )
        return "\n".join(items)

    def insert_coin(self, amount):
        self.balance += amount
        return self.balance

    def purchase_item(self, item_name):
        item_exists = item_name in self.inventory
        if item_exists:
            item = self.inventory[item_name]
            purchase_allowed = (
                item["quantity"] > 0 and self.balance >= item["price"]
            )
            if purchase_allowed:
                self.balance -= item["price"]
                item["quantity"] -= 1
                return self.balance

        return False

    def restock_item(self, item_name, quantity):
        exists = item_name in self.inventory
        if exists:
            self.inventory[item_name]["quantity"] += quantity
            return True

        return False

import unittest

class VendingMachineTestDisplayItems(unittest.TestCase):
    def test_display_items(self):
        vendingMachine = VendingMachine()
        vendingMachine.inventory = {'Coke': {'price': 1.25, 'quantity': 10}}
        self.assertEqual(vendingMachine.display_items(), 'Coke - $1.25 [10]')

    def test_display_items_2(self):
        vendingMachine = VendingMachine()
        self.assertEqual(vendingMachine.display_items(), False)

    def test_display_items_3(self):
        vendingMachine = VendingMachine()
        vendingMachine.inventory = {'Coke': {'price': 1.25, 'quantity': 10}, 'Pizza': {'price': 1.25, 'quantity': 10}}
        self.assertEqual(vendingMachine.display_items(),"Coke - $1.25 [10]\nPizza - $1.25 [10]")

    def test_display_items_4(self):
        vendingMachine = VendingMachine()
        vendingMachine.inventory = {'Coke': {'price': 1.25, 'quantity': 0}}
        self.assertEqual(vendingMachine.display_items(), 'Coke - $1.25 [0]')

    def test_display_items_5(self):
        vendingMachine = VendingMachine()
        vendingMachine.inventory = {'Coke': {'price': 1.25, 'quantity': 0}, 'Pizza': {'price': 1.25, 'quantity': 10}}
        self.assertEqual(vendingMachine.display_items(), 'Coke - $1.25 [0]\nPizza - $1.25 [10]')

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
