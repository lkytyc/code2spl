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

class BookManagementTestAddBook(unittest.TestCase):
    def test_add_book_1(self):
        bookManagement = BookManagement()
        bookManagement.add_book("book1")
        self.assertEqual({"book1": 1}, bookManagement.inventory)

    def test_add_book_2(self):
        bookManagement = BookManagement()
        self.assertEqual({}, bookManagement.inventory)

    def test_add_book_3(self):
        bookManagement = BookManagement()
        bookManagement.add_book("book1")
        bookManagement.add_book("book1", 2)
        self.assertEqual({"book1": 3}, bookManagement.inventory)

    def test_add_book_4(self):
        bookManagement = BookManagement()
        bookManagement.add_book("book1", 2)
        self.assertEqual({"book1": 2}, bookManagement.inventory)

    def test_add_book_5(self):
        bookManagement = BookManagement()
        bookManagement.add_book("book1", 2)
        bookManagement.add_book("book1")
        self.assertEqual({"book1": 3}, bookManagement.inventory)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
