import math


class AreaCalculator:
    def __init__(self, radius):
        self.radius = radius

    def calculate_annulus_area(self, inner_radius: float, outer_radius: float) -> float:
        area = math.pi * (outer_radius ** 2 - inner_radius ** 2)
        return area

    def calculate_circle_area(self) -> float:
        area = math.pi * self.radius ** 2
        return area

    def calculate_cylinder_area(self, height):
        radius = self.radius
        radius_plus_height = radius + height
        double_pi_radius = 2 * math.pi * radius
        area = double_pi_radius * radius_plus_height
        return area

    def calculate_sector_area(self, angle):
        return_value = self.radius ** 2 * angle / 2
        return return_value

    def calculate_sphere_area(self):
        radius = self.radius
        radius_squared = radius ** 2
        surface_area = 4 * math.pi * radius_squared
        return surface_area

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
