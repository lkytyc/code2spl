class BookManagement:
    def __init__(self):
        self.inventory = {}

    def add_book(self, title: str, quantity: int = 1) -> None:
        if title in self.inventory:
            self.inventory[title] += quantity
        else:
            self.inventory[title] = quantity

    def remove_book(self, title: str, quantity: int) -> None:
        if title not in self.inventory or self.inventory[title] < quantity:
            raise False

        updated_stock = self.inventory[title] - quantity
        self.inventory[title] = updated_stock

        if updated_stock == 0:
            del self.inventory[title]

    def view_inventory(self) -> dict:
        return self.inventory

    def view_book_quantity(self, title: str) -> int:
        if title not in self.inventory:
            return 0
        return self.inventory[title]

import unittest

class BookManagementTestViewInventory(unittest.TestCase):
    def test_view_inventory_1(self):
        bookManagement = BookManagement()
        bookManagement.add_book("book1", 2)
        bookManagement.add_book("book2")
        expected = {"book1": 2, "book2": 1}
        self.assertEqual(expected, bookManagement.inventory)

    def test_view_inventory_2(self):
        bookManagement = BookManagement()
        expected = {}
        self.assertEqual(expected, bookManagement.inventory)

    def test_view_inventory_3(self):
        bookManagement = BookManagement()
        bookManagement.add_book("book1", 2)
        bookManagement.add_book("book2")
        expected = {"book1": 2, "book2": 1}
        self.assertEqual(expected, bookManagement.inventory)

    def test_view_inventory_4(self):
        bookManagement = BookManagement()
        bookManagement.add_book("book1", 2)
        bookManagement.add_book("book2")
        bookManagement.remove_book("book1", 2)
        expected = {"book2": 1}
        self.assertEqual(expected, bookManagement.inventory)

    def test_view_inventory_5(self):
        bookManagement = BookManagement()
        bookManagement.add_book("book1", 2)
        bookManagement.add_book("book2", 1)
        bookManagement.remove_book("book1", 2)
        bookManagement.remove_book("book2",1)
        expected = {}
        self.assertEqual(expected, bookManagement.inventory)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
