import math


class AreaCalculator:
    def __init__(self, radius):
        self.radius = radius

    def calculate_circle_area(self):
        radius = self.radius
        squared_radius = radius ** 2
        area = math.pi * squared_radius
        return area

    def calculate_sphere_area(self):
        radius = self.radius
        radius_squared = radius ** 2
        pi_radius_squared = radius_squared * math.pi
        sphere_area = pi_radius_squared * 4
        return sphere_area

    def calculate_cylinder_area(self, height):
        radius_plus_height = self.radius + height
        cylinder_area = 2 * math.pi * self.radius * radius_plus_height
        return cylinder_area

    def calculate_sector_area(self, angle):
        radius = self.radius
        squared_radius = radius ** 2
        scaled_area = squared_radius * angle
        result = scaled_area / 2
        return result

    def calculate_annulus_area(self, inner_radius, outer_radius):
        outer_radius_squared = outer_radius ** 2
        inner_radius_squared = inner_radius ** 2
        area_difference = outer_radius_squared - inner_radius_squared
        result = area_difference * math.pi
        return result

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
