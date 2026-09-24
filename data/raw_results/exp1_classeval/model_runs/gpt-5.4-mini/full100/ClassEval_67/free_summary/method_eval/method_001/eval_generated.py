class Order:
    def __init__(self):
        self.menu = []
        self.selected_dishes = []
        self.sales = {}

    def add_dish(self, dish):
        dish_name = dish.get("dish")
        dish_count = dish.get("count", 0)

        for menu_item in self.menu:
            if menu_item.get("dish") == dish_name:
                if menu_item.get("count", 0) < dish_count:
                    return False
                menu_item["count"] -= dish_count
                self.selected_dishes.append(dish)
                return True

        self.selected_dishes.append(dish)
        return True

    def calculate_total(self):
        total = 0
        for dish in self.selected_dishes:
            dish_name = dish.get("dish")
            price = dish.get("price", 0)
            count = dish.get("count", 0)
            multiplier = self.sales.get(dish_name, 0)
            total += price * count * multiplier
        return total

    def checkout(self):
        if not self.selected_dishes:
            return False
        total = self.calculate_total()
        self.selected_dishes.clear()
        return total

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
