class ShoppingCart:
    def __init__(self):
        self.items = {}

    def add_item(self, item, price, quantity=1):
        item_exists = item in self.items
        if item_exists:
            self.items[item] = {'price': price, 'quantity': quantity}
        else:
            self.items[item] = {'price': price, 'quantity': quantity}

    def remove_item(self, item, quantity=1):
        item_exists = item in self.items
        if item_exists:
            self.items[item]['quantity'] -= quantity

    def total_price(self):
        try:
            items = self.items.values()
            result = sum(item['quantity'] * item['price'] for item in items)
            return result
        except Exception as e:
            print("The multiplication or summation cannot be completed because an item value is invalid.")
            raise RuntimeError(
                "Propagation of the underlying runtime error such as KeyError or TypeError."
            ) from e

    def view_items(self):
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
