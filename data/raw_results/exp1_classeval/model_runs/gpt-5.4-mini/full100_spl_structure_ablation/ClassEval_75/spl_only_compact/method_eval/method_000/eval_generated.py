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

class ShoppingCartTestAddItem(unittest.TestCase):
    def test_add_item_1(self):
        shoppingcart = ShoppingCart()
        shoppingcart.add_item("apple", 1, 5)
        self.assertEqual(shoppingcart.items, {"apple": {"price": 1, "quantity": 5}})

    def test_add_item_2(self):
        shoppingcart = ShoppingCart()
        shoppingcart.add_item("apple", 1)
        self.assertEqual(shoppingcart.items, {"apple": {"price": 1, "quantity": 1}})

    def test_add_item_3(self):
        shoppingcart = ShoppingCart()
        shoppingcart.add_item("aaa", 1)
        self.assertEqual(shoppingcart.items, {"aaa": {"price": 1, "quantity": 1}})

    def test_add_item_4(self):
        shoppingcart = ShoppingCart()
        shoppingcart.add_item("bbb", 1)
        self.assertEqual(shoppingcart.items, {"bbb": {"price": 1, "quantity": 1}})

    def test_add_item_5(self):
        shoppingcart = ShoppingCart()
        shoppingcart.add_item("ccc", 1)
        self.assertEqual(shoppingcart.items, {"ccc": {"price": 1, "quantity": 1}})

    def test_add_item_6(self):
        shoppingcart = ShoppingCart()
        shoppingcart.add_item("apple", 1, 5)
        shoppingcart.add_item("apple", 1, 5)
        self.assertEqual(shoppingcart.items, {"apple": {"price": 1, "quantity": 5}})

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
