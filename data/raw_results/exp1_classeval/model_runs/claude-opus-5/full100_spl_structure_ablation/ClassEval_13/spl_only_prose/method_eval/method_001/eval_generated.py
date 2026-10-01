class BookManagement:
    def __init__(self):
        self.inventory = {}

    def add_book(self, title, quantity=1):
        title_exists = title in self.inventory
        if title_exists:
            self.inventory[title] = self.inventory[title] + quantity
        else:
            self.inventory[title] = quantity

    def remove_book(self, title, quantity):
        guard_condition = title not in self.inventory or self.inventory[title] < quantity
        if guard_condition:
            print(f"Attempted to remove {quantity} copies of {title} but the item does not exist in inventory or available stock is insufficient")
            raise False
        self.inventory[title] = self.inventory[title] - quantity
        zero_check = self.inventory[title] == 0
        if zero_check:
            del self.inventory[title]

    def view_book_quantity(self, title):
        title_missing = title not in self.inventory
        if title_missing:
            return 0
        return self.inventory[title]

    def view_inventory(self):
        return self.inventory

import unittest

class BookManagementTestRemoveBook(unittest.TestCase):
    def setUp(self) -> None:
        self.bookManagement = BookManagement()
        self.bookManagement.add_book("book1", 2)
        self.bookManagement.add_book("book2")

    # remove all this title books
    def test_remove_book_1(self):
        self.bookManagement.remove_book("book1", 2)
        self.assertEqual(self.bookManagement.inventory, {"book2": 1})

    # remove part
    def test_remove_book_2(self):
        self.bookManagement.remove_book("book1", 1)
        self.assertEqual(self.bookManagement.inventory, {"book1": 1, "book2": 1})

    # remove the title that doesn't exist
    def test_remove_book_3(self):
        with self.assertRaises(Exception):
            self.bookManagement.remove_book("book3", 1)

    # invalid quantity
    def test_remove_book_4(self):
        with self.assertRaises(Exception):
            self.bookManagement.remove_book("book2", 2)

    def test_remove_book_5(self):
        with self.assertRaises(Exception):
            self.bookManagement.remove_book("book2", 5)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
