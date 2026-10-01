class ShoppingCart:
    def __init__(self):
        self.items = {}

    def add_item(self, item, price, quantity=1):
        item_exists = item in self.items
        self.items[item] = {"price": price, "quantity": quantity}

    def remove_item(self, item, quantity=1):
        item_present = item in self.items
        if item_present:
            updated_quantity = self.items[item]["quantity"] - quantity
            self.items[item]["quantity"] = updated_quantity

    def total_price(self) -> float:
        total_price = 0
        for item in self.items.values():
            item_total = item["quantity"] * item["price"]
            total_price += item_total
        return total_price

    def view_items(self) -> dict:
        items_value = self.items
        return items_value

import unittest

class ShoppingCartTestViewItems(unittest.TestCase):
    def test_view_items_1(self):
        shoppingcart = ShoppingCart()
        shoppingcart.add_item("apple", 1, 5)
        self.assertEqual(shoppingcart.view_items(), {"apple": {"price": 1, "quantity": 5}})

    def test_view_items_2(self):
        shoppingcart = ShoppingCart()
        shoppingcart.add_item("apple", 1, 4)
        self.assertEqual(shoppingcart.view_items(), {"apple": {"price": 1, "quantity": 4}})

    def test_view_items_3(self):
        shoppingcart = ShoppingCart()
        shoppingcart.add_item("apple", 1, 3)
        self.assertEqual(shoppingcart.view_items(), {"apple": {"price": 1, "quantity": 3}})

    def test_view_items_4(self):
        shoppingcart = ShoppingCart()
        shoppingcart.add_item("apple", 1, 2)
        self.assertEqual(shoppingcart.view_items(), {"apple": {"price": 1, "quantity": 2}})

    def test_view_items_5(self):
        shoppingcart = ShoppingCart()
        shoppingcart.add_item("apple", 1, 1)
        self.assertEqual(shoppingcart.view_items(), {"apple": {"price": 1, "quantity": 1}})

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
