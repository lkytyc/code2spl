class PageUtil:
    def __init__(self, data, page_size):
        self.data = data
        self.page_size = page_size
        self.total_items = len(data)
        self.total_pages = (self.total_items + self.page_size - 1) // self.page_size

    def get_page(self, page_number):
        if page_number < 1 or page_number > self.total_pages:
            return []
        start_index = (page_number - 1) * self.page_size
        end_index = start_index + self.page_size
        return self.data[start_index:end_index]

    def get_page_info(self, page_number):
        if page_number < 1 or page_number > self.total_pages:
            return {}
        start_index = (page_number - 1) * self.page_size
        end_index = min(start_index + self.page_size, self.total_items)
        page_data = self.data[start_index:end_index]
        page_info = {
            "current_page": page_number,
            "per_page": self.page_size,
            "total_pages": self.total_pages,
            "total_items": self.total_items,
            "has_previous": page_number > 1,
            "has_next": page_number < self.total_pages,
            "data": page_data,
        }
        return page_info

    def search(self, keyword):
        results = [item for item in self.data if keyword in str(item)]
        num_results = len(results)
        num_pages = (num_results + self.page_size - 1) // self.page_size
        search_info = {
            "keyword": keyword,
            "total_results": num_results,
            "total_pages": num_pages,
            "results": results,
        }
        return search_info

import unittest

class PageUtilTestSearch(unittest.TestCase):
    def setUp(self):
        self.data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.page_size = 3
        self.page_util = PageUtil(self.data, self.page_size)

    def test_search_1(self):
        keyword = "1"
        expected_results = {
            "keyword": "1",
            "total_results": 2,
            "total_pages": 1,
            "results": [1, 10]
        }
        actual_results = self.page_util.search(keyword)
        self.assertEqual(actual_results, expected_results)

    def test_search_2(self):
        keyword = "2"
        expected_results = {
            "keyword": "2",
            "total_results": 1,
            "total_pages": 1,
            "results": [2]
        }
        actual_results = self.page_util.search(keyword)
        self.assertEqual(actual_results, expected_results)

    def test_search_3(self):
        keyword = "3"
        expected_results = {
            "keyword": "3",
            "total_results": 1,
            "total_pages": 1,
            "results": [3]
        }
        actual_results = self.page_util.search(keyword)
        self.assertEqual(actual_results, expected_results)

    def test_search_4(self):
        keyword = "4"
        expected_results = {
            "keyword": "4",
            "total_results": 1,
            "total_pages": 1,
            "results": [4]
        }
        actual_results = self.page_util.search(keyword)
        self.assertEqual(actual_results, expected_results)

    def test_search_5(self):
        keyword = "11"
        expected_results = {
            "keyword": "11",
            "total_results": 0,
            "total_pages": 0,
            "results": []
        }
        actual_results = self.page_util.search(keyword)
        self.assertEqual(actual_results, expected_results)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
