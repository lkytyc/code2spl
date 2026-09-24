class AvgPartition:
    def __init__(self, lst, num):
        self.lst = lst
        self.num = num
        self.setNum()

    def setNum(self):
        self.base = len(self.lst) // self.num
        self.extra = len(self.lst) % self.num

    def get(self, index):
        start = index * self.base + min(index, self.extra)
        end = start + self.base + (1 if index < self.extra else 0)
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
