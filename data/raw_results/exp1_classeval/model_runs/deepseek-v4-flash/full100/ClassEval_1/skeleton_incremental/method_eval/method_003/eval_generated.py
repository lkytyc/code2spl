import math
class AreaCalculator:
    def __init__(self, radius):
        self.radius = radius

    def calculate_circle_area(self):
        return math.pi * self.radius ** 2

    def calculate_sphere_area(self):
        return 4 * math.pi * self.radius ** 2

    def calculate_cylinder_area(self, height):
        return 2 * math.pi * self.radius * (self.radius + height)

    def calculate_sector_area(self, angle):
        return self.radius ** 2 * angle / 2

    def calculate_annulus_area(self, inner_radius, outer_radius):
        return math.pi * (outer_radius ** 2 - inner_radius ** 2)

import unittest

class AreaCalculatorTestCalculateSectorArea(unittest.TestCase):
    def test_calculate_sector_area(self):
        areaCalculator = AreaCalculator(1.5)
        self.assertAlmostEqual(3.53, areaCalculator.calculate_sector_area(math.pi), delta=0.01)

    def test_calculate_sector_area_2(self):
        areaCalculator = AreaCalculator(2)
        self.assertAlmostEqual(3.14, areaCalculator.calculate_sector_area(math.pi/2), delta=0.01)

    def test_calculate_sector_area_3(self):
        areaCalculator = AreaCalculator(2)
        self.assertAlmostEqual(0, areaCalculator.calculate_sector_area(0), delta=0.01)

    def test_calculate_sector_area_4(self):
        areaCalculator = AreaCalculator(2)
        self.assertAlmostEqual(12.56, areaCalculator.calculate_sector_area(2*math.pi), delta=0.01)

    def test5_calculate_sector_area_5(self):
        areaCalculator = AreaCalculator(0)
        self.assertAlmostEqual(0, areaCalculator.calculate_sector_area(math.pi), delta=0.01)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
