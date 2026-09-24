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
