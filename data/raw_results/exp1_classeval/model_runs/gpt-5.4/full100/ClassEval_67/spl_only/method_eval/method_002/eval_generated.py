class Order:
    def __init__(self):
        self.menu = []
        self.selected_dishes = []
        self.sales = {}

    def add_dish(self, dish):
        for menu_dish in self.menu:
            if dish["dish"] == menu_dish["dish"]:
                if menu_dish["count"] < dish["count"]:
                    return False
                menu_dish["count"] -= dish["count"]
                break
        self.selected_dishes.append(dish)
        return True

    def calculate_total(self):
        total = 0
        for dish in self.selected_dishes:
            dish_total = dish["price"] * dish["count"] * self.sales[dish["dish"]]
            total += dish_total
        return total

    def checkout(self):
        if len(self.selected_dishes) == 0:
            return False
        total = self.calculate_total()
        self.selected_dishes = []
        return total

import unittest

class OrderTestCheckout(unittest.TestCase):
    def setUp(self):
        self.order = Order()
        self.order.menu.append({"dish": "dish1", "price": 10, "count": 5})
        self.order.menu.append({"dish": "dish2", "price": 15, "count": 3})
        self.order.menu.append({"dish": "dish3", "price": 20, "count": 7})
        self.order.sales = {"dish1": 0.9, "dish2": 1, "dish3": 0.8}

    # as test_main
    def test_checkout_1(self):
        self.order.add_dish({"dish": "dish1", "price": 10, "count": 2})
        self.order.add_dish({"dish": "dish3", "price": 20, "count": 2})
        result = self.order.checkout()
        self.assertEqual(50, result)

        menu = self.order.menu
        for menu_dish in menu:
            if menu_dish["dish"] == "dish1":
                self.assertEqual(menu_dish["count"], 3)
            if menu_dish["dish"] == "dish2":
                self.assertEqual(menu_dish["count"], 3)
            if menu_dish["dish"] == "dish3":
                self.assertEqual(menu_dish["count"], 5)
        self.assertEqual([], self.order.selected_dishes)

    # haven't ordered dishes.
    # self.selected_dishes is empty
    def test_checkout_2(self):
        result = self.order.checkout()
        self.assertFalse(result)

    def test_checkout_3(self):
        self.order.add_dish({"dish": "dish1", "price": 10, "count": 1})
        self.order.add_dish({"dish": "dish3", "price": 20, "count": 1})
        result = self.order.checkout()
        self.assertEqual(25, result)

        menu = self.order.menu
        for menu_dish in menu:
            if menu_dish["dish"] == "dish1":
                self.assertEqual(menu_dish["count"], 4)
            if menu_dish["dish"] == "dish2":
                self.assertEqual(menu_dish["count"], 3)
            if menu_dish["dish"] == "dish3":
                self.assertEqual(menu_dish["count"], 6)
        self.assertEqual([], self.order.selected_dishes)

    def test_checkout_4(self):
        self.order.add_dish({"dish": "dish1", "price": 10, "count": 3})
        self.order.add_dish({"dish": "dish3", "price": 20, "count": 3})
        result = self.order.checkout()
        self.assertEqual(75, result)

        menu = self.order.menu
        for menu_dish in menu:
            if menu_dish["dish"] == "dish1":
                self.assertEqual(menu_dish["count"], 2)
            if menu_dish["dish"] == "dish2":
                self.assertEqual(menu_dish["count"], 3)
            if menu_dish["dish"] == "dish3":
                self.assertEqual(menu_dish["count"], 4)
        self.assertEqual([], self.order.selected_dishes)

    def test_checkout_5(self):
        self.order.add_dish({"dish": "dish1", "price": 10, "count": 5})
        self.order.add_dish({"dish": "dish3", "price": 20, "count": 5})
        result = self.order.checkout()
        self.assertEqual(125, result)

        menu = self.order.menu
        for menu_dish in menu:
            if menu_dish["dish"] == "dish1":
                self.assertEqual(menu_dish["count"], 0)
            if menu_dish["dish"] == "dish2":
                self.assertEqual(menu_dish["count"], 3)
            if menu_dish["dish"] == "dish3":
                self.assertEqual(menu_dish["count"], 2)
        self.assertEqual([], self.order.selected_dishes)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
