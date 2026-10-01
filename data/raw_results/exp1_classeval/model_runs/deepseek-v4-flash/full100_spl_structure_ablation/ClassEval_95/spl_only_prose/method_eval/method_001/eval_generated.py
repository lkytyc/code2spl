class Warehouse:
    def __init__(self):
        self.inventory = {}
        self.orders = {}

    def add_product(self, product_id, name, quantity):
        is_new_product = product_id not in self.inventory
        if is_new_product:
            self.inventory[product_id] = {'name': name, 'quantity': quantity}
        else:
            self.inventory[product_id]['quantity'] += quantity

    def change_order_status(self, order_id, status):
        order_exists = order_id in self.orders
        if order_exists:
            self.orders[order_id]['status'] = status
        else:
            return False

    def create_order(self, order_id, product_id, quantity):
        stock_sufficient = self.get_product_quantity(product_id) >= quantity
        if stock_sufficient:
            self.update_product_quantity(product_id, -quantity)
            self.orders[order_id] = {
                'product_id': product_id,
                'quantity': quantity,
                'status': 'Shipped'
            }
        else:
            return False

    def get_product_quantity(self, product_id):
        is_present = product_id in self.inventory
        if is_present:
            return self.inventory[product_id]['quantity']
        else:
            return False

    def track_order(self, order_id):
        order_exists = order_id in self.orders
        if order_exists:
            return self.orders[order_id]['status']
        else:
            return False

    def update_product_quantity(self, product_id, quantity):
        if product_id in self.inventory:
            self.inventory[product_id]['quantity'] += quantity

import unittest

class WarehouseTestUpdateProductQuantity(unittest.TestCase):
    def test_update_product_quantity_1(self):
        warehouse = Warehouse()
        warehouse.add_product(1, 'product 1', 10)
        warehouse.update_product_quantity(1, 5)
        self.assertEqual(warehouse.inventory, {1: {'name': 'product 1', 'quantity': 15}})

    # quantity is negative
    def test_update_product_quantity_2(self):
        warehouse = Warehouse()
        warehouse.add_product(1, 'product 1', 10)
        warehouse.update_product_quantity(1, -5)
        self.assertEqual(warehouse.inventory, {1: {'name': 'product 1', 'quantity': 5}})

    def test_update_product_quantity_3(self):
        warehouse = Warehouse()
        warehouse.update_product_quantity(1, -5)
        self.assertEqual(warehouse.inventory, {})

    def test_update_product_quantity_4(self):
        warehouse = Warehouse()
        warehouse.add_product(1, 'product 1', 10)
        warehouse.update_product_quantity(1, 1)
        self.assertEqual(warehouse.inventory, {1: {'name': 'product 1', 'quantity': 11}})

    def test_update_product_quantity_5(self):
        warehouse = Warehouse()
        warehouse.add_product(1, 'product 1', 10)
        warehouse.update_product_quantity(1, -9)
        self.assertEqual(warehouse.inventory, {1: {'name': 'product 1', 'quantity': 1}})

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
