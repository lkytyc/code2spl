class VendingMachine:
    """
    This is a class to simulate a vending machine, including adding products, inserting coins, purchasing products, viewing balance, replenishing product inventory, and displaying product information.
    """

    def __init__(self):
        """
        Initializes the vending machine's inventory and balance.
        """
        self.inventory = {}
        self.balance = 0

    def add_item(self, item_name, price, quantity):
        """
        Adds a product to the vending machine's inventory.
        :param item_name: The name of the product to be added, str.
        :param price: The price of the product to be added, float.
        :param quantity: The quantity of the product to be added, int.
        :return: None
        """
        restock_result = self.restock_item(item_name, quantity)
        should_create_item = not restock_result

        if should_create_item:
            self.inventory[item_name] = {
                "price": price,
                "quantity": quantity,
            }

    def insert_coin(self, amount):
        """
        Inserts coins into the vending machine.
        :param amount: The amount of coins to be inserted, float.
        :return: The balance of the vending machine after the coins are inserted, float.
        """
        self.balance += amount
        return self.balance

    def purchase_item(self, item_name):
        """
        Purchases a product from the vending machine and returns the balance after the purchase and display purchase unsuccessful if the product is out of stock.
        :param item_name: The name of the product to be purchased, str.
        :return: If successful, returns the balance of the vending machine after the product is purchased, float,otherwise,returns False.
        """
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
        """
        Replenishes the inventory of a product already in the vending machine.
        :param item_name: The name of the product to be replenished, str.
        :param quantity: The quantity of the product to be replenished, int.
        :return: If the product is already in the vending machine, returns True, otherwise, returns False.
        """
        exists = item_name in self.inventory

        if exists:
            self.inventory[item_name]["quantity"] += quantity
            return True

        return False

    def display_items(self):
        """
        Displays the products in the vending machine.
        :return: If the vending machine is empty, returns False, otherwise, returns a list of the products in the vending machine, str.
        """
        inventory_is_empty = not self.inventory

        if inventory_is_empty:
            return False

        items = []
        for item_name, item_info in self.inventory.items():
            items.append(
                f"{item_name} - ${item_info['price']} [{item_info['quantity']}]"
            )

        return "\n".join(items)

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
