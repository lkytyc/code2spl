class VendingMachine:
    def __init__(self):
        self.inventory = {}
        self.balance = 0

    def add_item(self, item_name, price, quantity):
        restock_result = self.restock_item(item_name, quantity)
        restock_failed = not restock_result
        if restock_failed:
            self.inventory[item_name] = {'price': price, 'quantity': quantity}

    def display_items(self):
        inventory_is_falsy = not self.inventory
        if inventory_is_falsy:
            return False
        else:
            items = []
            for item_name, item_info in self.inventory.items():
                items.append(f"{item_name} - ${item_info['price']} [{item_info['quantity']}]")
            return "\n".join(items)

    def insert_coin(self, amount):
        self.balance = self.balance + amount
        updated_balance = self.balance
        return updated_balance

    def purchase_item(self, item_name):
        item_exists = item_name in self.inventory
        if item_exists:
            item = self.inventory[item_name]
            purchase_allowed = item['quantity'] > 0 and self.balance >= item['price']
            if purchase_allowed:
                self.balance = self.balance - item['price']
                updated_balance = self.balance
                item['quantity'] = item['quantity'] - 1
                updated_quantity = item['quantity']
                return updated_balance
            else:
                return False
        else:
            return False

    def restock_item(self, item_name, quantity):
        item_exists = item_name in self.inventory
        if item_exists:
            self.inventory[item_name]['quantity'] = self.inventory[item_name]['quantity'] + quantity
            updated_quantity = self.inventory[item_name]['quantity']
            return True
        else:
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
