import math


class AreaCalculator:
    def __init__(self, radius):
        self.radius = radius

    def calculate_annulus_area(self, inner_radius, outer_radius):
        radii = (inner_radius, outer_radius)
        squared_terms = (outer_radius ** 2, inner_radius ** 2)
        area_difference = squared_terms[0] - squared_terms[1]
        result = area_difference * math.pi
        return result

    def calculate_circle_area(self):
        radius = self.radius
        radius_squared = radius ** 2
        area = math.pi * radius_squared
        return area

    def calculate_cylinder_area(self, height):
        radius = self.radius
        pi = math.pi
        radius_plus_height = radius + height
        result = 2 * pi * radius * radius_plus_height
        return result

    def calculate_sector_area(self, angle):
        radius = self.radius
        radius_squared = radius ** 2
        scaled_area = radius_squared * angle
        result = scaled_area / 2
        return result

    def calculate_sphere_area(self):
        radius = self.radius
        radius_squared = radius ** 2
        pi_radius_squared = math.pi * radius_squared
        area = 4 * pi_radius_squared
        return area

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
