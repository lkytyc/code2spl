class Warehouse:
    def __init__(self):
        self.inventory = {}
        self.orders = {}

    def add_product(self, product_id, name, quantity):
        product_absent = product_id not in self.inventory
        if product_absent:
            self.inventory[product_id] = {
                "name": name,
                "quantity": quantity,
            }
        else:
            self.inventory[product_id]["quantity"] += quantity

    def change_order_status(self, order_id, status) -> bool:
        order_exists = order_id in self.orders
        if order_exists:
            self.orders[order_id]["status"] = status
        else:
            return False

    def create_order(self, order_id, product_id, quantity):
        stock_is_sufficient = (
            self.get_product_quantity(product_id) >= quantity
        )
        if stock_is_sufficient:
            self.update_product_quantity(product_id, -quantity)
            self.orders[order_id] = {
                "product_id": product_id,
                "quantity": quantity,
                "status": "Shipped",
            }
        else:
            return False

    def get_product_quantity(self, product_id):
        product_exists = product_id in self.inventory
        if product_exists:
            return self.inventory[product_id]["quantity"]
        return False

    def track_order(self, order_id):
        order_exists = order_id in self.orders
        if order_exists:
            return self.orders[order_id]["status"]
        return False

    def update_product_quantity(self, product_id, quantity):
        product_exists = product_id in self.inventory
        if product_exists:
            self.inventory[product_id]["quantity"] += quantity

import unittest

class WarehouseTestChangeOrderStatus(unittest.TestCase):
    def test_change_order_status_1(self):
        warehouse = Warehouse()
        warehouse.add_product(1, 'product 1', 10)
        warehouse.create_order(1, 1, 5)
        warehouse.change_order_status(1, 'Delivered')
        self.assertEqual(warehouse.orders, {1: {'product_id': 1, 'quantity': 5, 'status': 'Delivered'}})

    def test_change_order_status_2(self):
        warehouse = Warehouse()
        result = warehouse.change_order_status(1, 'Delivered')
        self.assertFalse(result)

    def test_change_order_status_3(self):
        warehouse = Warehouse()
        warehouse.add_product(1, 'product 3', 5)
        warehouse.create_order(1, 1, 5)
        warehouse.change_order_status(1, 'Delivered')
        self.assertEqual(warehouse.orders, {1: {'product_id': 1, 'quantity': 5, 'status': 'Delivered'}})

    def test_change_order_status_4(self):
        warehouse = Warehouse()
        warehouse.add_product(1, 'product 4', 100)
        warehouse.create_order(1, 1, 50)
        warehouse.change_order_status(1, 'Delivered')
        self.assertEqual(warehouse.orders, {1: {'product_id': 1, 'quantity': 50, 'status': 'Delivered'}})

    def test_change_order_status_5(self):
        warehouse = Warehouse()
        result = warehouse.change_order_status(2, 'Delivered')
        self.assertFalse(result)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
