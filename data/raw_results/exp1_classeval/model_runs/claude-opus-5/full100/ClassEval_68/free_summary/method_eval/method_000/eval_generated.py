import math


class PageUtil:
    def __init__(self, data: list, page_size: int):
        self.data = data
        self.page_size = page_size
        self.total_items = len(data)
        self.total_pages = math.ceil(self.total_items / page_size) if page_size > 0 else 0

    def get_page(self, page_number: int) -> list:
        if page_number < 1 or page_number > self.total_pages:
            return []
        start_index = (page_number - 1) * self.page_size
        end_index = page_number * self.page_size
        return self.data[start_index:end_index]

    def get_page_info(self, page_number: int) -> dict:
        if page_number < 1 or page_number > self.total_pages:
            return {}
        start_index = (page_number - 1) * self.page_size
        end_index = min(page_number * self.page_size, self.total_items)
        return {
            "current_page": page_number,
            "page_size": self.page_size,
            "total_pages": self.total_pages,
            "total_items": self.total_items,
            "has_previous": page_number > 1,
            "has_next": page_number < self.total_pages,
            "data": self.data[start_index:end_index],
        }

    def search(self, keyword: str) -> dict:
        matches = [item for item in self.data if keyword in str(item)]
        match_count = len(matches)
        page_count = math.ceil(match_count / self.page_size) if self.page_size > 0 else 0
        return {
            "keyword": keyword,
            "match_count": match_count,
            "page_count": page_count,
            "results": matches,
        }

import unittest

class PageUtilTestGetPage(unittest.TestCase):
    def setUp(self):
        self.data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.page_size = 3
        self.page_util = PageUtil(self.data, self.page_size)

    def test_get_page_1(self):
        page_number = 1
        expected_page = [1, 2, 3]
        actual_page = self.page_util.get_page(page_number)
        self.assertEqual(actual_page, expected_page)

    def test_get_page_2(self):
        page_number = 2
        expected_page = [4, 5, 6]
        actual_page = self.page_util.get_page(page_number)
        self.assertEqual(actual_page, expected_page)

    def test_get_page_3(self):
        page_number = 3
        expected_page = [7, 8, 9]
        actual_page = self.page_util.get_page(page_number)
        self.assertEqual(actual_page, expected_page)

    def test_get_page_4(self):
        page_number = 4
        expected_page = [10]
        actual_page = self.page_util.get_page(page_number)
        self.assertEqual(actual_page, expected_page)

    def test_get_page_5(self):
        invalid_page_number = 0
        empty_page = []
        actual_page = self.page_util.get_page(invalid_page_number)
        self.assertEqual(actual_page, empty_page)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
