import math


class AreaCalculator:
    def __init__(self, radius):
        self.radius = radius

    @staticmethod
    def calculate_annulus_area(inner_radius, outer_radius):
        outer_radius_squared = outer_radius ** 2
        inner_radius_squared = inner_radius ** 2
        squared_diff = outer_radius_squared - inner_radius_squared
        annulus_area = squared_diff * math.pi
        return annulus_area

    def calculate_circle_area(self):
        radius_value = self.radius
        radius_squared = radius_value ** 2
        circle_area = math.pi * radius_squared
        return circle_area

    def calculate_cylinder_area(self, height):
        radius_value = self.radius
        height_value = height
        inner_sum = radius_value + height_value
        surface_area = 2 * math.pi * self.radius * inner_sum
        return surface_area

    def calculate_sector_area(self, angle):
        radius = self.radius
        radius_squared = radius ** 2
        product = radius_squared * angle
        area = product / 2
        return area

    def calculate_sphere_area(self):
        radius_value = self.radius
        radius_squared = radius_value ** 2
        pi_times_radius_squared = radius_squared * math.pi
        area = pi_times_radius_squared * 4
        return area

import unittest

class AreaCalculatorTestCalculateCircleArea(unittest.TestCase):
    def test_calculate_circle_area(self):
        areaCalculator = AreaCalculator(2)
        self.assertAlmostEqual(12.56, areaCalculator.calculate_circle_area(), delta=0.01)
    def test_calculate_circle_area_2(self):
        areaCalculator = AreaCalculator(2.5)
        self.assertAlmostEqual(19.63, areaCalculator.calculate_circle_area(), delta=0.01)

    def test_calculate_circle_area_3(self):
        areaCalculator = AreaCalculator(2000)
        self.assertAlmostEqual(12566370.61, areaCalculator.calculate_circle_area(), delta=0.01)

    def test_calculate_circle_area_4(self):
        areaCalculator = AreaCalculator(0)
        self.assertAlmostEqual(0, areaCalculator.calculate_circle_area(), delta=0.01)

    def test_calculate_circle_area_5(self):
        areaCalculator = AreaCalculator(0.1)
        self.assertAlmostEqual(0.031, areaCalculator.calculate_circle_area(), delta=0.01)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
