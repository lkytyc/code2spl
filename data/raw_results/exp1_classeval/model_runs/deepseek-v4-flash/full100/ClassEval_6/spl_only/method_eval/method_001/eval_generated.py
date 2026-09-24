class AvgPartition:
    def __init__(self, lst, limit):
        self.lst = lst
        self.limit = limit

    def setNum(self):
        size = len(self.lst) // self.limit
        remainder = len(self.lst) % self.limit
        return (size, remainder)

    def get(self, index):
        size, remainder = self.setNum()
        start = index * size + min(index, remainder)
        end = start + size
        if index + 1 <= remainder:
            end += 1
        return self.lst[start:end]

import unittest

class AvgPartitionTestGet(unittest.TestCase):

    def test_get(self):
        a = AvgPartition([1, 2, 3, 4], 2)
        self.assertEqual(a.get(0), [1, 2])

    def test_get_2(self):
        a = AvgPartition([1, 2, 3, 4], 2)
        self.assertEqual(a.get(1), [3, 4])

    def test_get_3(self):
        a = AvgPartition([1, 2, 3, 4, 5], 2)
        self.assertEqual(a.get(0), [1, 2, 3])

    def test_get_4(self):
        a = AvgPartition([1, 2, 3, 4, 5], 2)
        self.assertEqual(a.get(1), [4, 5])

    def test_get_5(self):
        a = AvgPartition([1, 2, 3, 4, 5], 3)
        self.assertEqual(a.get(0), [1, 2])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
