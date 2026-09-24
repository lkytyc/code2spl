import math

class AreaCalculator:

    def __init__(self, radius):
        self.radius = radius

    def calculate_circle_area(self):
        radius_value = self.radius
        radius_squared = radius_value ** 2
        circle_area = math.pi * radius_squared
        return circle_area

    def calculate_sphere_area(self):
        radius_value = self.radius
        radius_squared = radius_value ** 2
        pi_times_radius_squared = math.pi * radius_squared
        area = 4 * pi_times_radius_squared
        return area

    def calculate_cylinder_area(self, height):
        inner_sum = self.radius + height
        surface_area = 2 * math.pi * self.radius * inner_sum
        return surface_area

    def calculate_sector_area(self, angle):
        radius = self.radius
        radius_squared = radius ** 2
        product = radius_squared * angle
        area = product / 2
        return area

    def calculate_annulus_area(self, inner_radius, outer_radius):
        outer_radius_squared = outer_radius ** 2
        inner_radius_squared = inner_radius ** 2
        squared_diff = outer_radius_squared - inner_radius_squared
        annulus_area = math.pi * squared_diff
        return annulus_area

import unittest

class AreaCalculatorTestCalculateAnnulusArea(unittest.TestCase):
    def test_calculate_annulus_area(self):
        areaCalculator = AreaCalculator(2)
        self.assertAlmostEqual(25.128, areaCalculator.calculate_annulus_area(1, 3), delta=0.01)

    def test_calculate_annulus_area_2(self):
        areaCalculator = AreaCalculator(2.5)
        self.assertAlmostEqual(0, areaCalculator.calculate_annulus_area(3, 3), delta=0.01)

    def test_calculate_annulus_area_3(self):
        areaCalculator = AreaCalculator(2000)
        self.assertAlmostEqual(3.14, areaCalculator.calculate_annulus_area(0, 1), delta=0.01)

    def test_calculate_annulus_area_4(self):
        areaCalculator = AreaCalculator(0)
        self.assertAlmostEqual(25.13, areaCalculator.calculate_annulus_area(1, 3), delta=0.01)

    def test_calculate_annulus_area_5(self):
        areaCalculator = AreaCalculator(2.5)
        self.assertAlmostEqual(25.13, areaCalculator.calculate_annulus_area(1, 3), delta=0.01)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
