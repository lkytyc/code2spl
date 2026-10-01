import math

class AreaCalculator:
    """
    This is a class for calculating the area of different shapes, including circle, sphere, cylinder, sector and annulus.
    """

    def __init__(self, radius):
        """
        Initialize the radius for shapes.
        :param radius: float
        """
        self.radius = radius

    def calculate_circle_area(self):
        """
        calculate the area of circle based on self.radius
        :return: area of circle, float
        >>> areaCalculator = AreaCalculator(2)
        >>> areaCalculator.calculate_circle_area()
        12.566370614359172
        """
        radius_value = self.radius
        radius_squared = radius_value ** 2
        circle_area = math.pi * radius_squared
        return circle_area

    def calculate_sphere_area(self):
        """
        calculate the area of sphere based on self.radius
        :return: area of sphere, float
        >>> areaCalculator = AreaCalculator(2)
        >>> areaCalculator.calculate_sphere_area()
        50.26548245743669
        """
        radius_value = self.radius
        radius_squared = radius_value ** 2
        pi_times_radius_squared = math.pi * radius_squared
        area = 4 * pi_times_radius_squared
        return area

    def calculate_cylinder_area(self, height):
        """
        calculate the area of cylinder based on self.radius and height
        :param height: height of cylinder, float
        :return: area of cylinder, float
        >>> areaCalculator = AreaCalculator(2)
        >>> areaCalculator.calculate_cylinder_area(3)
        62.83185307179586
        """
        radius_value = self.radius
        height_value = height
        inner_sum = radius_value + height_value
        surface_area = 2 * math.pi * radius_value * inner_sum
        return surface_area

    def calculate_sector_area(self, angle):
        """
        calculate the area of sector based on self.radius and angle
        :param angle: angle of sector, float
        :return: area of sector, float
        >>> areaCalculator = AreaCalculator(2)
        >>> areaCalculator.calculate_sector_area(math.pi)
        6.283185307179586
        """
        radius = self.radius
        radius_squared = radius ** 2
        product = radius_squared * angle
        area = product / 2
        return area

    def calculate_annulus_area(self, inner_radius, outer_radius):
        """
        calculate the area of annulus based on inner_radius and out_radius
        :param inner_radius: inner radius of sector, float
        :param outer_radius: outer radius of sector, float
        :return: area of annulus, float
        >>> areaCalculator.calculate_annulus_area(2, 3)
        15.707963267948966
        """
        outer_radius_squared = outer_radius ** 2
        inner_radius_squared = inner_radius ** 2
        squared_diff = outer_radius_squared - inner_radius_squared
        annulus_area = math.pi * squared_diff
        return annulus_area

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
