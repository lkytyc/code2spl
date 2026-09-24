import math

class AreaCalculator:
    def __init__(self, radius: number):
        self.radius = radius

    def calculate_annulus_area(self, inner_radius: numeric, outer_radius: numeric) -> float:
        outer_radius_squared = outer_radius ** 2
        inner_radius_squared = inner_radius ** 2
        radius_squared_difference = outer_radius_squared - inner_radius_squared
        annulus_area = radius_squared_difference * math.pi
        return annulus_area

    def calculate_circle_area(self) -> float:
        radius = self.radius
        radius_squared = radius ** 2
        area = math.pi * radius_squared
        return area

    def calculate_cylinder_area(self, height: numeric) -> numeric:
        area = 2 * math.pi * self.radius * (self.radius + height)
        return area

    def calculate_sector_area(self, angle: numeric) -> numeric:
        radius = self.radius
        radius_squared = radius ** 2
        product = radius_squared * angle
        sector_area = product / 2
        return sector_area

    def calculate_sphere_area(self) -> float:
        return_value = 4 * math.pi * self.radius ** 2
        return return_value

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
