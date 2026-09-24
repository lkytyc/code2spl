class Order:
    def __init__(self):
        self.menu = []
        self.selected_dishes = []
        self.sales = {}

    def add_dish(self, dish):
        for menu_item in self.menu:
            if menu_item["dish"] == dish["dish"]:
                if 0 < dish["count"] <= menu_item["count"]:
                    menu_item["count"] -= dish["count"]
                    self.selected_dishes.append({
                        "dish": dish["dish"],
                        "count": dish["count"],
                        "price": dish["price"]
                    })
                    return True
                return False
        return False

    def calculate_total(self):
        total = 0.0
        for dish in self.selected_dishes:
            total += dish["price"] * dish["count"] * self.sales.get(dish["dish"], 1)
        return total

    def checkout(self):
        if not self.selected_dishes:
            return False
        return self.calculate_total()

import unittest

class OrderTestCalculateTotal(unittest.TestCase):
    def setUp(self):
        self.order = Order()
        self.order.menu.append({"dish": "dish1", "price": 10, "count": 5})
        self.order.menu.append({"dish": "dish2", "price": 15, "count": 3})
        self.order.menu.append({"dish": "dish3", "price": 20, "count": 7})
        self.order.sales = {"dish1": 0.9, "dish2": 1, "dish3": 0.8}

    def test_calculate_total_1(self):
        self.order.add_dish({"dish": "dish1", "price": 10, "count": 2})
        self.order.add_dish({"dish": "dish3", "price": 20, "count": 2})
        result = self.order.calculate_total()
        self.assertEqual(50, result)

    def test_calculate_total_2(self):
        self.order.add_dish({"dish": "dish1", "price": 10, "count": 2})
        self.order.add_dish({"dish": "dish2", "price": 15, "count": 2})
        result = self.order.calculate_total()
        self.assertEqual(48, result)

    def test_calculate_total_3(self):
        self.order.add_dish({"dish": "dish1", "price": 10, "count": 1})
        self.order.add_dish({"dish": "dish3", "price": 20, "count": 1})
        result = self.order.calculate_total()
        self.assertEqual(25, result)

    def test_calculate_total_4(self):
        self.order.add_dish({"dish": "dish1", "price": 10, "count": 3})
        self.order.add_dish({"dish": "dish3", "price": 20, "count": 3})
        result = self.order.calculate_total()
        self.assertEqual(75, result)

    def test_calculate_total_5(self):
        self.order.add_dish({"dish": "dish1", "price": 10, "count": 4})
        self.order.add_dish({"dish": "dish3", "price": 20, "count": 4})
        result = self.order.calculate_total()
        self.assertEqual(100, result)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
