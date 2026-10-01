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
