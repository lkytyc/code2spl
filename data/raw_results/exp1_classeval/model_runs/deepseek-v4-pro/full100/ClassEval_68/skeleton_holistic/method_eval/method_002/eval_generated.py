class PageUtil:
    """
    PageUtil class is a versatile utility for handling pagination and search functionalities in an efficient and convenient manner.
    """

    def __init__(self, data, page_size):
        """
        Initialize the PageUtil object with the given data and page size.
        :param data: list, the data to be paginated
        :param page_size: int, the number of items per page
        """
        self.data = data
        self.page_size = page_size
        self.total_items = len(data)
        self.total_pages = (self.total_items + page_size - 1) // page_size

    def get_page(self, page_number):
        """
        Retrieve a specific page of data.
        :param page_number: int, the page number to fetch
        :return: list, the data on the specified page
        >>> page_util = PageUtil([1, 2, 3, 4], 1)
        >>> page_util.get_page(1)
        [1]

        """
        if page_number < 1 or page_number > self.total_pages:
            return []
        start = (page_number - 1) * self.page_size
        end = start + self.page_size
        return self.data[start:end]

    def get_page_info(self, page_number):
        """
        Retrieve information about a specific page.
        :param page_number: int, the page number to fetch information about
        :return: dict, containing page information such as current page number, total pages, etc.
        >>> page_util = PageUtil([1, 2, 3, 4], 1)
        >>> page_util.get_page_info(1)
        >>> {
        >>>     "current_page": 1,
        >>>     "per_page": 1,
        >>>     "total_pages": 4,
        >>>     "total_items": 4,
        >>>     "has_previous": False,
        >>>     "has_next": True,
        >>>     "data": [1]
        >>> }

        """
        page_data = self.get_page(page_number)
        return {
            "current_page": page_number,
            "per_page": self.page_size,
            "total_pages": self.total_pages,
            "total_items": self.total_items,
            "has_previous": page_number > 1,
            "has_next": page_number < self.total_pages,
            "data": page_data
        }

    def search(self, keyword):
        """
        Search for items in the data that contain the given keyword.
        :param keyword: str, the keyword to search for
        :return: dict, containing search information such as total results and matching items
        >>> page_util = PageUtil([1, 2, 3, 4], 1)
        >>> page_util.search("1")
        >>> search_info = {
        >>>     "keyword": "1",
        >>>     "total_results": 1,
        >>>     "total_pages": 1,
        >>>     "results": [1]
        >>> }
        """
        results = [item for item in self.data if keyword in str(item)]
        total_results = len(results)
        total_pages = (total_results + self.page_size - 1) // self.page_size if total_results > 0 else 0
        return {
            "keyword": keyword,
            "total_results": total_results,
            "total_pages": total_pages,
            "results": results
        }

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
