class VendingMachine:
    def __init__(self):
        self.inventory = {}
        self.balance = 0

    def add_item(self, item_name: str, price: float, quantity: int):
        restock_result = self.restock_item(item_name, quantity)
        if not restock_result:
            self.inventory[item_name] = {'price': price, 'quantity': quantity}

    def display_items(self) -> str | bool:
        if not self.inventory:
            return False
        items = []
        for item_name, item_info in self.inventory.items():
            formatted_line = f"{item_name} - ${item_info['price']} [{item_info['quantity']}]"
            items.append(formatted_line)
        return "\n".join(items)

    def insert_coin(self, amount: float) -> float:
        current_balance = self.balance
        self.balance = current_balance + amount
        return self.balance

    def purchase_item(self, item_name: str) -> float | bool:
        if item_name in self.inventory:
            item = self.inventory[item_name]
            if item['quantity'] > 0 and self.balance >= item['price']:
                self.balance -= item['price']
                item['quantity'] -= 1
                return self.balance
        return False

    def restock_item(self, item_name: str, quantity: float) -> bool:
        if item_name in self.inventory:
            self.inventory[item_name]['quantity'] += quantity
            return True
        return False

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
