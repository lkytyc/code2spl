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

class WarehouseTestAddProduct(unittest.TestCase):
    def test_add_product_1(self):
        warehouse = Warehouse()
        warehouse.add_product(1, 'product 1', 10)
        self.assertEqual(warehouse.inventory, {1: {'name': 'product 1', 'quantity': 10}})

    def test_add_product_2(self):
        warehouse = Warehouse()
        warehouse.add_product(1, 'product 1', 10)
        warehouse.add_product(2, 'product 2', 5)
        self.assertEqual(warehouse.inventory,
                         {1: {'name': 'product 1', 'quantity': 10}, 2: {'name': 'product 2', 'quantity': 5}})

    def test_add_product_3(self):
        warehouse = Warehouse()
        warehouse.add_product(1, 'product 3', 10)
        self.assertEqual(warehouse.inventory, {1: {'name': 'product 3', 'quantity': 10}})

    def test_add_product_4(self):
        warehouse = Warehouse()
        warehouse.add_product(1, 'product 4', 10)
        self.assertEqual(warehouse.inventory, {1: {'name': 'product 4', 'quantity': 10}})

    def test_add_product_5(self):
        warehouse = Warehouse()
        warehouse.add_product(1, 'product 5', 10)
        self.assertEqual(warehouse.inventory, {1: {'name': 'product 5', 'quantity': 10}})

    def test_add_product_6(self):
        warehouse = Warehouse()
        warehouse.add_product(1, 'product 5', 10)
        warehouse.add_product(1, 'product 5', 10)
        self.assertEqual(warehouse.inventory, {1: {'name': 'product 5', 'quantity': 20}})

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
