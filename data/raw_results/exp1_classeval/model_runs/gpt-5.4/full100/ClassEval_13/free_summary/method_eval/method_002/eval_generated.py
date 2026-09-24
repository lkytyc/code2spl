class BookManagement:
    def __init__(self):
        self.inventory = {}

    def add_book(self, title, quantity=1):
        if title in self.inventory:
            self.inventory[title] += quantity
        else:
            self.inventory[title] = quantity

    def remove_book(self, title, quantity):
        if title not in self.inventory or quantity > self.inventory[title]:
            raise TypeError("exceptions must derive from BaseException")
        self.inventory[title] -= quantity
        if self.inventory[title] == 0:
            del self.inventory[title]

    def view_inventory(self):
        return self.inventory

    def view_book_quantity(self, title):
        return self.inventory.get(title, 0)

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
