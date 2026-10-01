class Warehouse:
    """
    The class manages inventory and orders, including adding products, updating product quantities, retrieving product quantities, creating orders, changing order statuses, and tracking orders.
    """

    def __init__(self):
        self.inventory = {}  # Product ID: Product
        self.orders = {}  # Order ID: Order

    def add_product(self, product_id, name, quantity):
        if product_id not in self.inventory:
            self.inventory[product_id] = {'name': name, 'quantity': quantity}
        else:
            self.inventory[product_id]['quantity'] += quantity

    def update_product_quantity(self, product_id, quantity):
        if product_id in self.inventory:
            self.inventory[product_id]['quantity'] += quantity

    def get_product_quantity(self, product_id):
        if product_id in self.inventory:
            return self.inventory[product_id]['quantity']
        return False

    def create_order(self, order_id, product_id, quantity):
        if self.get_product_quantity(product_id) >= quantity:
            self.update_product_quantity(product_id, -quantity)
            self.orders[order_id] = {
                'product_id': product_id,
                'quantity': quantity,
                'status': 'Shipped'
            }
        else:
            return False

    def change_order_status(self, order_id, status):
        if order_id in self.orders:
            self.orders[order_id]['status'] = status
        else:
            return False

    def track_order(self, order_id):
        if order_id in self.orders:
            return self.orders[order_id]['status']
        return False

import unittest

class WarehouseTestGetProductQuantity(unittest.TestCase):
    def test_get_product_quantity_1(self):
        warehouse = Warehouse()
        warehouse.add_product(1, 'product 1', 10)
        self.assertEqual(warehouse.get_product_quantity(1), 10)

    def test_get_product_quantity_2(self):
        warehouse = Warehouse()
        self.assertEqual(warehouse.get_product_quantity(1), False)

    def test_get_product_quantity_3(self):
        warehouse = Warehouse()
        warehouse.add_product(1, 'product 1', 5)
        self.assertEqual(warehouse.get_product_quantity(1), 5)

    def test_get_product_quantity_4(self):
        warehouse = Warehouse()
        warehouse.add_product(1, 'product 1', 100)
        self.assertEqual(warehouse.get_product_quantity(1), 100)

    def test_get_product_quantity_5(self):
        warehouse = Warehouse()
        warehouse.add_product(5, 'product 1', 10)
        self.assertEqual(warehouse.get_product_quantity(5), 10)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
