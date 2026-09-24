class ShoppingCart:
    def __init__(self):
        self.items = {}

    def add_item(self, item: str, price, quantity: int = 1):
        item_exists_flag = item in self.items
        self.items[item] = {'price': price, 'quantity': quantity}

    def remove_item(self, item, quantity: int = 1):
        item_presence_check = item in self.items
        if item_presence_check:
            self.items[item]['quantity'] -= quantity
        else:
            pass

    def total_price(self):
        items_view = self.items.values()
        products_list = [item['quantity'] * item['price'] for item in items_view]
        total = sum(products_list)
        return total

    def view_items(self) -> dict:
        return self.items

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
