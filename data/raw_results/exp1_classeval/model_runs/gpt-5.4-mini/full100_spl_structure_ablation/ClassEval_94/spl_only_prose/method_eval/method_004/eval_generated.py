class VendingMachine:
    def __init__(self):
        self.inventory = {}
        self.balance = 0

    def add_item(self, item_name, price, quantity):
        restock_success = self.restock_item(item_name, quantity)
        if not restock_success:
            self.inventory[item_name] = {"price": price, "quantity": quantity}

    def display_items(self):
        if not self.inventory:
            return False
        items = []
        for item_name, item_info in self.inventory.items():
            items.append(f"{item_name} - ${item_info['price']} [{item_info['quantity']}]")
        return "\n".join(items)

    def insert_coin(self, amount):
        current_balance = self.balance
        updated_balance = current_balance + amount
        self.balance = updated_balance
        return updated_balance

    def purchase_item(self, item_name):
        inventory_membership = item_name in self.inventory
        if inventory_membership:
            item = self.inventory[item_name]
            purchase_eligibility = item["quantity"] > 0 and self.balance >= item["price"]
            if purchase_eligibility:
                self.balance -= item["price"]
                item["quantity"] -= 1
                return self.balance
        return False

    def restock_item(self, item_name, quantity):
        item_exists = item_name in self.inventory
        if item_exists:
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
