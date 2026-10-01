class DiscountStrategy:
    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.cart = cart
        self.promotion = promotion
        self.__total = self.total()

    def BulkItemPromo(self, order):
        discount = 0
        for item in order.cart:
            if item['quantity'] >= 20:
                discount += item['quantity'] * item['price'] * 0.1
        return discount

    def FidelityPromo(self, order):
        if order.customer['fidelity'] >= 1000:
            discount = order.total() * 0.05
        else:
            discount = 0
        return discount

    def LargeOrderPromo(self, order):
        distinct_products = {item['product'] for item in order.cart}
        distinct_product_count = len(distinct_products)
        if distinct_product_count >= 10:
            discount_amount = order.total() * 0.07
            return discount_amount
        return 0

    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion(self)
        return self.__total - discount

    def total(self):
        total_value = sum(item['quantity'] * item['price'] for item in self.cart)
        self.__total = total_value
        return self.__total

import unittest


class DiscountStrategyTestTotal(unittest.TestCase):
    def test_total_1(self):
        customer = {'name': 'John Doe', 'fidelity': 1200}
        cart = [{'product': 'product1', 'quantity': 10, 'price': 20.0},
                {'product': 'product2', 'quantity': 5, 'price': 10.0}]
        order = DiscountStrategy(customer, cart)
        expected_total = 250.0
        actual_total = order.total()
        self.assertEqual(actual_total, expected_total)

    def test_total_2(self):
        customer = {'name': 'John Doe', 'fidelity': 1200}
        cart = [{'product': 'product1', 'quantity': 10, 'price': 10.0},
                {'product': 'product2', 'quantity': 5, 'price': 10.0}]
        order = DiscountStrategy(customer, cart)
        expected_total = 150.0
        actual_total = order.total()
        self.assertEqual(actual_total, expected_total)

    def test_total_3(self):
        customer = {'name': 'John Doe', 'fidelity': 1200}
        cart = [{'product': 'product1', 'quantity': 10, 'price': 200.0},
                {'product': 'product2', 'quantity': 5, 'price': 10.0}]
        order = DiscountStrategy(customer, cart)
        expected_total = 2050.0
        actual_total = order.total()
        self.assertEqual(actual_total, expected_total)

    def test_total_4(self):
        customer = {'name': 'John Doe', 'fidelity': 1200}
        cart = [{'product': 'product1', 'quantity': 1, 'price': 20.0},
                {'product': 'product2', 'quantity': 5, 'price': 10.0}]
        order = DiscountStrategy(customer, cart)
        expected_total = 70.0
        actual_total = order.total()
        self.assertEqual(actual_total, expected_total)

    def test_total_5(self):
        customer = {'name': 'John Doe', 'fidelity': 1200}
        cart = []
        order = DiscountStrategy(customer, cart)
        expected_total = 0
        actual_total = order.total()
        self.assertEqual(actual_total, expected_total)


class DiscountStrategyTestDue(unittest.TestCase):
    def test_due_1(self):
        customer = {'name': 'John Doe', 'fidelity': 1200}
        cart = [{'product': 'product1', 'quantity': 10, 'price': 20.0},
                {'product': 'product2', 'quantity': 5, 'price': 10.0}]
        order = DiscountStrategy(customer, cart)
        expected_due = 250.0
        actual_due = order.due()
        self.assertEqual(actual_due, expected_due)

    def test_due_2(self):
        customer = {'name': 'John Doe', 'fidelity': 1200}
        cart = [{'product': 'product1', 'quantity': 10, 'price': 20.0},
                {'product': 'product2', 'quantity': 5, 'price': 10.0}]
        order = DiscountStrategy(customer, cart, DiscountStrategy.FidelityPromo)
        expected_due = 237.5
        actual_due = order.due()
        self.assertEqual(actual_due, expected_due)

    def test_due_3(self):
        customer = {'name': 'John Doe', 'fidelity': 1200}
        cart = [{'product': 'product1', 'quantity': 20, 'price': 20.0},
                {'product': 'product2', 'quantity': 5, 'price': 10.0}]
        order = DiscountStrategy(customer, cart, DiscountStrategy.BulkItemPromo)
        expected_due = 410.0
        actual_due = order.due()
        self.assertEqual(actual_due, expected_due)

    def test_due_4(self):
        customer = {'name': 'John Doe', 'fidelity': 1200}
        cart = [{'product': f'product{i}', 'quantity': 1, 'price': 10.0} for i in range(15)]
        order = DiscountStrategy(customer, cart, DiscountStrategy.LargeOrderPromo)
        expected_due = 139.5
        actual_due = order.due()
        self.assertEqual(actual_due, expected_due)

    def test_due_5(self):
        customer = {'name': 'John Doe', 'fidelity': 900}
        cart = [{'product': 'product1', 'quantity': 10, 'price': 20.0},
                {'product': 'product2', 'quantity': 5, 'price': 10.0}]
        order = DiscountStrategy(customer, cart, DiscountStrategy.FidelityPromo)
        expected_due = 250.0
        actual_due = order.due()
        self.assertEqual(actual_due, expected_due)


class DiscountStrategyTestFidelityPromo(unittest.TestCase):
    def test_fidelity_promo_1(self):
        customer = {'name': 'John Doe', 'fidelity': 1000}
        cart = [{'product': 'product1', 'quantity': 10, 'price': 20.0},
                {'product': 'product2', 'quantity': 5, 'price': 10.0}]
        order = DiscountStrategy(customer, cart, DiscountStrategy.FidelityPromo)
        expected_discount = 12.5
        actual_discount = order.promotion(order)
        self.assertEqual(actual_discount, expected_discount)

    def test_fidelity_promo_2(self):
        customer = {'name': 'John Doe', 'fidelity': 800}
        cart = [{'product': 'product1', 'quantity': 10, 'price': 20.0},
                {'product': 'product2', 'quantity': 5, 'price': 10.0}]
        order = DiscountStrategy(customer, cart, DiscountStrategy.FidelityPromo)
        expected_discount = 0
        actual_discount = order.promotion(order)
        self.assertEqual(actual_discount, expected_discount)

    def test_fidelity_promo_3(self):
        customer = {'name': 'John Doe', 'fidelity': 0}
        cart = [{'product': 'product1', 'quantity': 10, 'price': 20.0},
                {'product': 'product2', 'quantity': 5, 'price': 10.0}]
        order = DiscountStrategy(customer, cart, DiscountStrategy.FidelityPromo)
        expected_discount = 0
        actual_discount = order.promotion(order)
        self.assertEqual(actual_discount, expected_discount)

    def test_fidelity_promo_4(self):
        customer = {'name': 'John Doe', 'fidelity': 10000}
        cart = [{'product': 'product1', 'quantity': 10, 'price': 20.0},
                {'product': 'product2', 'quantity': 5, 'price': 10.0}]
        order = DiscountStrategy(customer, cart, DiscountStrategy.FidelityPromo)
        expected_discount = 12.5
        actual_discount = order.promotion(order)
        self.assertEqual(actual_discount, expected_discount)

    def test_fidelity_promo_5(self):
        customer = {'name': 'John Doe', 'fidelity': 1800}
        cart = [{'product': 'product1', 'quantity': 10, 'price': 20.0},
                {'product': 'product2', 'quantity': 5, 'price': 10.0}]
        order = DiscountStrategy(customer, cart, DiscountStrategy.FidelityPromo)
        expected_discount = 12.5
        actual_discount = order.promotion(order)
        self.assertEqual(actual_discount, expected_discount)


class DiscountStrategyTestBulkItemPromo(unittest.TestCase):
    def test_bulk_item_promo_1(self):
        customer = {'name': 'John Doe', 'fidelity': 1200}
        cart = [{'product': 'product1', 'quantity': 20, 'price': 10.0},
                {'product': 'product2', 'quantity': 5, 'price': 5.0}]
        order = DiscountStrategy(customer, cart, DiscountStrategy.BulkItemPromo)
        expected_discount = 20.0
        actual_discount = order.promotion(order)
        self.assertEqual(actual_discount, expected_discount)

    def test_bulk_item_promo_2(self):
        customer = {'name': 'John Doe', 'fidelity': 1200}
        cart = [{'product': 'product1', 'quantity': 10, 'price': 10.0},
                {'product': 'product2', 'quantity': 5, 'price': 5.0}]
        order = DiscountStrategy(customer, cart, DiscountStrategy.BulkItemPromo)
        expected_discount = 0
        actual_discount = order.promotion(order)
        self.assertEqual(actual_discount, expected_discount)

    def test_bulk_item_promo_3(self):
        customer = {'name': 'John Doe', 'fidelity': 1200}
        cart = [{'product': 'product1', 'quantity': 100, 'price': 10.0},
                {'product': 'product2', 'quantity': 5, 'price': 5.0}]
        order = DiscountStrategy(customer, cart, DiscountStrategy.BulkItemPromo)
        expected_discount = 100.0
        actual_discount = order.promotion(order)
        self.assertEqual(actual_discount, expected_discount)

    def test_bulk_item_promo_4(self):
        customer = {'name': 'John Doe', 'fidelity': 1200}
        cart = [{'product': 'product1', 'quantity': 1, 'price': 10.0},
                {'product': 'product2', 'quantity': 5, 'price': 5.0}]
        order = DiscountStrategy(customer, cart, DiscountStrategy.BulkItemPromo)
        expected_discount = 0.0
        actual_discount = order.promotion(order)
        self.assertEqual(actual_discount, expected_discount)

    def test_bulk_item_promo_5(self):
        customer = {'name': 'John Doe', 'fidelity': 1200}
        cart = [{'product': 'product1', 'quantity': 30, 'price': 10.0},
                {'product': 'product2', 'quantity': 5, 'price': 5.0}]
        order = DiscountStrategy(customer, cart, DiscountStrategy.BulkItemPromo)
        expected_discount = 30.0
        actual_discount = order.promotion(order)
        self.assertEqual(actual_discount, expected_discount)


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


class DiscountStrategyTest(unittest.TestCase):
    def test_DiscountStrategy(self):
        customer = {'name': 'John Doe', 'fidelity': 1200}
        cart = [{'product': 'product1', 'quantity': 10, 'price': 20.0},
                {'product': 'product2', 'quantity': 5, 'price': 10.0}]
        order = DiscountStrategy(customer, cart)
        expected_total = 250.0
        actual_total = order.total()
        self.assertEqual(actual_total, expected_total)

        customer = {'name': 'John Doe', 'fidelity': 1200}
        cart = [{'product': 'product1', 'quantity': 10, 'price': 20.0},
                {'product': 'product2', 'quantity': 5, 'price': 10.0}]
        order = DiscountStrategy(customer, cart)
        expected_due = 250.0
        actual_due = order.due()
        self.assertEqual(actual_due, expected_due)

        customer = {'name': 'John Doe', 'fidelity': 1000}
        cart = [{'product': 'product1', 'quantity': 10, 'price': 20.0},
                {'product': 'product2', 'quantity': 5, 'price': 10.0}]
        order = DiscountStrategy(customer, cart, DiscountStrategy.FidelityPromo)
        expected_discount = 12.5
        actual_discount = order.promotion(order)
        self.assertEqual(actual_discount, expected_discount)

        customer = {'name': 'John Doe', 'fidelity': 1200}
        cart = [{'product': 'product1', 'quantity': 20, 'price': 10.0},
                {'product': 'product2', 'quantity': 5, 'price': 5.0}]
        order = DiscountStrategy(customer, cart, DiscountStrategy.BulkItemPromo)
        expected_discount = 20.0
        actual_discount = order.promotion(order)
        self.assertEqual(actual_discount, expected_discount)

        customer = {'name': 'John Doe', 'fidelity': 1200}
        cart = [{'product': f'product{i}', 'quantity': 1, 'price': 10.0} for i in range(10)]
        order = DiscountStrategy(customer, cart, DiscountStrategy.LargeOrderPromo)
        expected_discount = 7.0
        actual_discount = order.promotion(order)
        self.assertAlmostEqual(actual_discount, expected_discount)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
