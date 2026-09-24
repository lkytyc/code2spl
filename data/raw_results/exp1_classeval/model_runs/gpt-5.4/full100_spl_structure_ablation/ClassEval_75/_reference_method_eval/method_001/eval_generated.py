class ShoppingCart:
    def __init__(self):
        self.items = {}

    def add_item(self, item, price, quantity=1):
        if item in self.items:
            self.items[item] = {'price': price, 'quantity': quantity}
        else:
            self.items[item] = {'price': price, 'quantity': quantity}

    def remove_item(self, item, quantity=1):
        if item in self.items:
            self.items[item]['quantity'] -= quantity
        else:
            pass

    def view_items(self) -> dict:
        return self.items

    def total_price(self) -> float:
        return sum([item['quantity'] * item['price'] for item in self.items.values()])

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
