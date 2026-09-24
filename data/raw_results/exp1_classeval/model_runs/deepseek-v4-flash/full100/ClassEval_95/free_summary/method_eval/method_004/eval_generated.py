class Warehouse:
    def __init__(self):
        self.products = {}
        self.orders = {}

    def add_product(self, product_id, name, quantity):
        if product_id in self.products:
            self.products[product_id]["quantity"] += quantity
        else:
            self.products[product_id] = {"name": name, "quantity": quantity}

    def increase_quantity(self, product_id, amount):
        if product_id not in self.products:
            return False
        self.products[product_id]["quantity"] += amount
        return True

    def get_quantity(self, product_id):
        if product_id not in self.products:
            return False
        return self.products[product_id]["quantity"]

    def create_order(self, order_id, product_id, quantity):
        if product_id not in self.products or self.products[product_id]["quantity"] < quantity:
            return False
        self.products[product_id]["quantity"] -= quantity
        self.orders[order_id] = {
            "product_id": product_id,
            "quantity": quantity,
            "status": "Shipped"
        }
        return True

    def update_order_status(self, order_id, new_status):
        if order_id not in self.orders:
            return False
        self.orders[order_id]["status"] = new_status
        return True

    def get_order_status(self, order_id):
        if order_id not in self.orders:
            return False
        return self.orders[order_id]["status"]

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
