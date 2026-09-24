class Order:
    """
    The class manages restaurant orders by allowing the addition of dishes, calculation of the total cost, and checkout.
    """


    def __init__(self):
        """
        Initialize the order management system
        self.menu stores the dishes of resturant inventory
        menu = [{"dish": dish name, "price": price, "count": count}, ...]
        self.selected_dishes stores the dished selected by customer
        selected_dish = {"dish": dish name, "count": count, price: price}
        self.sales stores the sales of each dish
        sales = {dish name: sales}
        """
        self.menu = []
        self.selected_dishes = []
        self.sales = {}


    def add_dish(self, dish):
        """
        Check the self.menu and add into self.selected_dish if the dish count is valid.
        And if the dish has successfully been added, change the count in self.menu.
        :param dish: dict, the information of dish. dish = {"dish": dish name, "count": count, price: price}
        :return: True if successfully added, or False otherwise.
        >>> order = Order()
        >>> order.menu.append({"dish": "dish1", "price": 10, "count": 5})
        >>> order.add_dish({"dish": "dish1", "price": 10, "count": 3})
        True
        """
        for menu_dish in self.menu:
            if menu_dish["dish"] == dish["dish"]:
                if menu_dish["count"] >= dish["count"]:
                    menu_dish["count"] -= dish["count"]
                    self.selected_dishes.append(dish)
                    return True
                else:
                    return False
        return False


    def calculate_total(self):
        """
        Calculate the total price of dishes that have been ordered. Multiply the count, price and sales.
        :return total: float, the final total price.
        >>> order = Order()
        >>> order.menu.append({"dish": "dish1", "price": 10, "count": 5})
        >>> order.sales = {"dish1": 0.8}
        >>> order.add_dish({"dish": "dish1", "price": 10, "count": 4})
        True
        >>> order.calculate_total()
        32.0
        """
        total = 0
        for dish in self.selected_dishes:
            total += dish['price'] * dish['count'] * self.sales[dish['dish']]
        return total


    def checkout(self):
        """
        Check out the dished ordered. IF the self.selected_dishes is not empty, invoke the calculate_total
        method to check out.
        :return Flase if the self.selected_dishes is empty, or total(return value of calculate_total) otherwise.
        >>> order = Order()
        >>> order.menu.append({"dish": "dish1", "price": 10, "count": 5})
        >>> order.sales = {"dish1": 0.8}
        >>> order.add_dish({"dish": "dish1", "price": 10, "count": 4})
        True
        >>> order.checkout()
        32.0
        """
        if self.selected_dishes:
            total = self.calculate_total()
            self.selected_dishes = []
            return total
        else:
            return False

import unittest

class OrderTestAddDish(unittest.TestCase):
    def setUp(self):
        self.order = Order()

        self.order.menu.append({"dish": "dish1", "price": 10, "count": 5})
        self.order.menu.append({"dish": "dish2", "price": 15, "count": 3})
        self.order.menu.append({"dish": "dish3", "price": 20, "count": 7})
        self.order.sales = {"dish1": 0.9, "dish2": 1, "dish3": 0.8}

    # add dish in menu
    def test_add_dish_1(self):
        result = self.order.add_dish({"dish": "dish3", "price": 15, "count": 4})
        self.assertTrue(result)

        # test the status of self.menu and self.selected_dishes
        menu = self.order.menu
        for menu_dish in menu:
            if menu_dish["dish"] == "dish1":
                self.assertEqual(menu_dish["count"], 5)
            if menu_dish["dish"] == "dish2":
                self.assertEqual(menu_dish["count"], 3)
            if menu_dish["dish"] == "dish3":
                self.assertEqual(menu_dish["count"], 3)
        self.assertEqual(self.order.selected_dishes, [{"dish": "dish3", "price": 15, "count": 4}])

    # add dish when dish count exceeds the remaining count
    def test_add_dish_2(self):
        result = self.order.add_dish({"dish": "dish3", "price": 15, "count": 8})
        self.assertFalse(result)

        menu = self.order.menu
        for menu_dish in menu:
            if menu_dish["dish"] == "dish1":
                self.assertEqual(menu_dish["count"], 5)
            if menu_dish["dish"] == "dish2":
                self.assertEqual(menu_dish["count"], 3)
            if menu_dish["dish"] == "dish3":
                self.assertEqual(menu_dish["count"], 7)
        self.assertEqual(self.order.selected_dishes, [])

    def test_add_dish_3(self):
        result = self.order.add_dish({"dish": "dish3", "price": 15, "count": 7})
        self.assertTrue(result)

        # test the status of self.menu and self.selected_dishes
        menu = self.order.menu
        for menu_dish in menu:
            if menu_dish["dish"] == "dish1":
                self.assertEqual(menu_dish["count"], 5)
            if menu_dish["dish"] == "dish2":
                self.assertEqual(menu_dish["count"], 3)
            if menu_dish["dish"] == "dish3":
                self.assertEqual(menu_dish["count"], 0)
        self.assertEqual(self.order.selected_dishes, [{"dish": "dish3", "price": 15, "count": 7}])

    def test_add_dish_4(self):
        result = self.order.add_dish({"dish": "dish3", "price": 15, "count": 6})
        self.assertTrue(result)

        # test the status of self.menu and self.selected_dishes
        menu = self.order.menu
        for menu_dish in menu:
            if menu_dish["dish"] == "dish1":
                self.assertEqual(menu_dish["count"], 5)
            if menu_dish["dish"] == "dish2":
                self.assertEqual(menu_dish["count"], 3)
            if menu_dish["dish"] == "dish3":
                self.assertEqual(menu_dish["count"], 1)
        self.assertEqual(self.order.selected_dishes, [{"dish": "dish3", "price": 15, "count": 6}])

    def test_add_dish_5(self):
        result = self.order.add_dish({"dish": "dish3", "price": 15, "count": 5})
        self.assertTrue(result)

        # test the status of self.menu and self.selected_dishes
        menu = self.order.menu
        for menu_dish in menu:
            if menu_dish["dish"] == "dish1":
                self.assertEqual(menu_dish["count"], 5)
            if menu_dish["dish"] == "dish2":
                self.assertEqual(menu_dish["count"], 3)
            if menu_dish["dish"] == "dish3":
                self.assertEqual(menu_dish["count"], 2)
        self.assertEqual(self.order.selected_dishes, [{"dish": "dish3", "price": 15, "count": 5}])

    def test_add_dish_6(self):
        self.order.menu = []
        result = self.order.add_dish({})
        self.assertTrue(result)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
