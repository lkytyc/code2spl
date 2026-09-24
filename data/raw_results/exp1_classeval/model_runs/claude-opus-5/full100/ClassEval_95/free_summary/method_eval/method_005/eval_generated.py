class Warehouse:
    def __init__(self):
        self.inventory = {}
        self.orders = {}

    def add_product(self, product_id, name, quantity):
        if product_id in self.inventory:
            self.inventory[product_id]['quantity'] += quantity
        else:
            self.inventory[product_id] = {'name': name, 'quantity': quantity}

    def update_product_quantity(self, product_id, amount):
        if product_id not in self.inventory:
            return False
        self.inventory[product_id]['quantity'] += amount

    def get_product_quantity(self, product_id):
        if product_id not in self.inventory:
            return False
        return self.inventory[product_id]['quantity']

    def create_order(self, order_id, product_id, quantity):
        available = self.get_product_quantity(product_id)
        if available is False or available < quantity:
            return False
        self.update_product_quantity(product_id, -quantity)
        self.orders[order_id] = {
            'product_id': product_id,
            'quantity': quantity,
            'status': 'Shipped',
        }

    def change_order_status(self, order_id, status):
        if order_id not in self.orders:
            return False
        self.orders[order_id]['status'] = status

    def track_order(self, order_id):
        if order_id not in self.orders:
            return False
        return self.orders[order_id]['status']

import unittest

class WarehouseTestTrackOrder(unittest.TestCase):
    def test_track_order_1(self):
        warehouse = Warehouse()
        warehouse.add_product(1, 'product 1', 10)
        warehouse.create_order(1, 1, 5)
        self.assertEqual(warehouse.track_order(1), 'Shipped')

    def test_track_order_2(self):
        warehouse = Warehouse()
        result = warehouse.track_order(1)
        self.assertFalse(result)

    def test_track_order_3(self):
        warehouse = Warehouse()
        warehouse.add_product(1, 'product 3', 10)
        warehouse.create_order(1, 1, 1)
        self.assertEqual(warehouse.track_order(1), 'Shipped')

    def test_track_order_4(self):
        warehouse = Warehouse()
        warehouse.add_product(1, 'product 4', 100)
        warehouse.create_order(1, 1, 50)
        self.assertEqual(warehouse.track_order(1), 'Shipped')

    def test_track_order_5(self):
        warehouse = Warehouse()
        warehouse.add_product(1, 'product 5', 100)
        warehouse.create_order(1, 1, 10)
        self.assertEqual(warehouse.track_order(1), 'Shipped')

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
