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

class ShoppingCartTestRemoveItem(unittest.TestCase):
    def test_remove_item_1(self):
        shoppingcart = ShoppingCart()
        shoppingcart.add_item("apple", 1, 5)
        shoppingcart.remove_item("apple", 3)
        self.assertEqual(shoppingcart.items, {"apple": {"price": 1, "quantity": 2}})

    def test_remove_item_2(self):
        shoppingcart = ShoppingCart()
        shoppingcart.add_item("apple", 1, 5)
        shoppingcart.remove_item("apple")
        self.assertEqual(shoppingcart.items, {"apple": {"price": 1, "quantity": 4}})

    def test_remove_item_3(self):
        shoppingcart = ShoppingCart()
        shoppingcart.add_item("apple", 1, 5)
        shoppingcart.remove_item("apple", 1)
        self.assertEqual(shoppingcart.items, {"apple": {"price": 1, "quantity": 4}})

    def test_remove_item_4(self):
        shoppingcart = ShoppingCart()
        shoppingcart.add_item("apple", 1, 5)
        shoppingcart.remove_item("apple", 2)
        self.assertEqual(shoppingcart.items, {"apple": {"price": 1, "quantity": 3}})

    def test_remove_item_5(self):
        shoppingcart = ShoppingCart()
        shoppingcart.add_item("apple", 1, 5)
        shoppingcart.remove_item("apple", 4)
        self.assertEqual(shoppingcart.items, {"apple": {"price": 1, "quantity": 1}})

    def test_remove_item_6(self):
        shoppingcart = ShoppingCart()
        shoppingcart.add_item("apple", 1, 5)
        shoppingcart.remove_item("banana", 4)
        self.assertEqual(shoppingcart.items, {"apple": {"price": 1, "quantity": 5}})

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
