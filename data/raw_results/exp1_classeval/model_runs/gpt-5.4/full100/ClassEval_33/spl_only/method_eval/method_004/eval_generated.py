class DiscountStrategy:
    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.cart = cart
        self.promotion = promotion
        self.__total = self.total()

    def total(self):
        line_item_values = (item["quantity"] * item["price"] for item in self.cart)
        total_value = sum(line_item_values)
        self.__total = total_value
        return self.__total

    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion(self)
        return self.__total - discount

    @staticmethod
    def FidelityPromo(order):
        if order.customer["fidelity"] >= 1000:
            discount = order.total() * 0.05
        else:
            discount = 0
        return discount

    @staticmethod
    def BulkItemPromo(order):
        discount = 0
        for item in order.cart:
            if item["quantity"] >= 20:
                discount += item["quantity"] * item["price"] * 0.1
        return discount

    @staticmethod
    def LargeOrderPromo(order):
        distinct_products = {item["product"] for item in order.cart}
        distinct_product_count = len(distinct_products)
        if distinct_product_count >= 10:
            discount_amount = order.total() * 0.07
            return discount_amount
        return 0

import unittest

class DiscountStrategyTestLargeOrderPromo(unittest.TestCase):
    def test_large_order_promo_1(self):
        customer = {'name': 'John Doe', 'fidelity': 1200}
        cart = [{'product': f'product{i}', 'quantity': 1, 'price': 10.0} for i in range(10)]
        order = DiscountStrategy(customer, cart, DiscountStrategy.LargeOrderPromo)
        expected_discount = 7.0
        actual_discount = order.promotion(order)
        self.assertAlmostEqual(actual_discount, expected_discount)

    def test_large_order_promo_2(self):
        customer = {'name': 'John Doe', 'fidelity': 1200}
        cart = [{'product': f'product{i}', 'quantity': 1, 'price': 10.0} for i in range(5)]
        order = DiscountStrategy(customer, cart, DiscountStrategy.LargeOrderPromo)
        expected_discount = 0
        actual_discount = order.promotion(order)
        self.assertEqual(actual_discount, expected_discount)

    def test_large_order_promo_3(self):
        customer = {'name': 'John Doe', 'fidelity': 1200}
        cart = [{'product': f'product{i}', 'quantity': 1, 'price': 10.0} for i in range(100)]
        order = DiscountStrategy(customer, cart, DiscountStrategy.LargeOrderPromo)
        expected_discount = 70.0
        actual_discount = order.promotion(order)
        self.assertAlmostEqual(actual_discount, expected_discount)

    def test_large_order_promo_4(self):
        customer = {'name': 'John Doe', 'fidelity': 1200}
        cart = [{'product': f'product{i}', 'quantity': 1, 'price': 10.0} for i in range(1000)]
        order = DiscountStrategy(customer, cart, DiscountStrategy.LargeOrderPromo)
        expected_discount = 700.0
        actual_discount = order.promotion(order)
        self.assertAlmostEqual(actual_discount, expected_discount)

    def test_large_order_promo_5(self):
        customer = {'name': 'John Doe', 'fidelity': 1200}
        cart = [{'product': f'product{i}', 'quantity': 1, 'price': 10.0} for i in range(1)]
        order = DiscountStrategy(customer, cart, DiscountStrategy.LargeOrderPromo)
        expected_discount = 0.0
        actual_discount = order.promotion(order)
        self.assertAlmostEqual(actual_discount, expected_discount)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
