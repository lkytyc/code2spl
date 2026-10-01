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

class ShoppingCartTestTotalPrice(unittest.TestCase):
    def test_total_price_1(self):
        shoppingcart = ShoppingCart()
        shoppingcart.add_item("apple", 1, 5)
        shoppingcart.add_item("banana", 2, 3)
        self.assertEqual(shoppingcart.total_price(), 11.0)

    def test_total_price_2(self):
        shoppingcart = ShoppingCart()
        shoppingcart.add_item("apple", 1, 5)
        shoppingcart.add_item("banana", 2, 3)
        shoppingcart.remove_item("apple", 3)
        self.assertEqual(shoppingcart.total_price(), 8.0)

    def test_total_price_3(self):
        shoppingcart = ShoppingCart()
        shoppingcart.add_item("apple", 1, 1)
        shoppingcart.add_item("banana", 2, 1)
        self.assertEqual(shoppingcart.total_price(), 3.0)

    def test_total_price_4(self):
        shoppingcart = ShoppingCart()
        shoppingcart.add_item("apple", 1, 2)
        shoppingcart.add_item("banana", 2, 1)
        self.assertEqual(shoppingcart.total_price(), 4.0)

    def test_total_price_5(self):
        shoppingcart = ShoppingCart()
        shoppingcart.add_item("apple", 1, 3)
        shoppingcart.add_item("banana", 2, 1)
        self.assertEqual(shoppingcart.total_price(), 5.0)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
