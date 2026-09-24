class BookManagement:
    def __init__(self):
        self.inventory = {}

    def add_book(self, title: str, quantity: int = 1):
        if title in self.inventory:
            self.inventory[title] += quantity
        else:
            self.inventory[title] = quantity

    def remove_book(self, title: str, quantity: int) -> None:
        if title not in self.inventory or self.inventory[title] < quantity:
            raise False
        updated_stock = self.inventory[title] - quantity
        if updated_stock == 0:
            del self.inventory[title]
        else:
            self.inventory[title] = updated_stock

    def view_book_quantity(self, title: str) -> int:
        if title not in self.inventory:
            return 0
        return self.inventory[title]

    def view_inventory(self):
        return self.inventory

import unittest

class BookManagementTestViewBookQuantity(unittest.TestCase):
    def test_view_book_quantity_1(self):
        bookManagement = BookManagement()
        bookManagement.add_book("book1", 2)
        self.assertEqual(2, bookManagement.view_book_quantity("book1"))

    def test_view_book_quantity_2(self):
        bookManagement = BookManagement()
        self.assertEqual(0, bookManagement.view_book_quantity("book1"))

    def test_view_book_quantity_3(self):
        bookManagement = BookManagement()
        bookManagement.add_book("book1", 2)
        self.assertEqual(2, bookManagement.view_book_quantity("book1"))

    def test_view_book_quantity_4(self):
        bookManagement = BookManagement()
        bookManagement.add_book("book1", 2)
        bookManagement.remove_book("book1", 2)
        self.assertEqual(0, bookManagement.view_book_quantity("book1"))

    def test_view_book_quantity_5(self):
        bookManagement = BookManagement()
        bookManagement.add_book("book1", 3)
        bookManagement.remove_book("book1", 2)
        self.assertEqual(1, bookManagement.view_book_quantity("book1"))

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
