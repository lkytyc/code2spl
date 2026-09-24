import math

class AreaCalculator:
    def __init__(self, radius):
        self.radius = radius

    def calculate_circle_area(self):
        radius = self.radius
        radius_squared = radius ** 2
        area = math.pi * radius_squared
        return area

    def calculate_sphere_area(self):
        return 4 * math.pi * self.radius ** 2

    def calculate_cylinder_area(self, height):
        area = 2 * math.pi * self.radius * (self.radius + height)
        return area

    def calculate_sector_area(self, angle):
        radius = self.radius
        radius_squared = radius ** 2
        product = radius_squared * angle
        sector_area = product / 2
        return sector_area

    def calculate_annulus_area(self, inner_radius, outer_radius):
        outer_radius_squared = outer_radius ** 2
        inner_radius_squared = inner_radius ** 2
        radius_squared_difference = outer_radius_squared - inner_radius_squared
        annulus_area = math.pi * radius_squared_difference
        return annulus_area

import unittest

class AreaCalculatorTestCalculateCylinderArea(unittest.TestCase):
    def test_calculate_cylinder_area(self):
        areaCalculator = AreaCalculator(2)
        self.assertAlmostEqual(50.27, areaCalculator.calculate_cylinder_area(2), delta=0.01)

    def test_calculate_cylinder_area_2(self):
        areaCalculator = AreaCalculator(2)
        self.assertAlmostEqual(25.13, areaCalculator.calculate_cylinder_area(0), delta=0.01)

    def test_calculate_cylinder_area_3(self):
        areaCalculator = AreaCalculator(0)
        self.assertAlmostEqual(0, areaCalculator.calculate_cylinder_area(2000), delta=0.01)

    def test_calculate_cylinder_area_4(self):
        areaCalculator = AreaCalculator(2.5)
        self.assertAlmostEqual(70.68, areaCalculator.calculate_cylinder_area(2), delta=0.01)

    def test_calculate_cylinder_area_5(self):
        areaCalculator = AreaCalculator(2.5)
        self.assertAlmostEqual(62.83, areaCalculator.calculate_cylinder_area(1.5), delta=0.01)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
