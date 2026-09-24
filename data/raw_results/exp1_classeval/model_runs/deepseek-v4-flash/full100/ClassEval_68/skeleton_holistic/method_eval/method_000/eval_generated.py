class PageUtil:
    def __init__(self, data, page_size):
        self.data = data
        self.page_size = page_size
        self.total_items = len(data)
        self.total_pages = (self.total_items + page_size - 1) // page_size

    def get_page(self, page_number):
        if page_number < 1 or page_number > self.total_pages:
            return []
        start = (page_number - 1) * self.page_size
        end = start + self.page_size
        return self.data[start:end]

    def get_page_info(self, page_number):
        if page_number < 1 or page_number > self.total_pages:
            return {}
        page_data = self.get_page(page_number)
        return {
            "current_page": page_number,
            "per_page": self.page_size,
            "total_pages": self.total_pages,
            "total_items": self.total_items,
            "has_previous": page_number > 1,
            "has_next": page_number < self.total_pages,
            "data": page_data,
        }

    def search(self, keyword):
        keyword_str = str(keyword)
        results = [item for item in self.data if keyword_str in str(item)]
        total_results = len(results)
        total_pages = (total_results + self.page_size - 1) // self.page_size
        return {
            "keyword": keyword,
            "total_results": total_results,
            "total_pages": total_pages,
            "results": results,
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
