class Interpolation:
    """
    This is a class that implements the Linear interpolation operation of one-dimensional and two-dimensional data
    """

    def __init__(self):
        pass

    @staticmethod
    def interpolate_1d(x, y, x_interp):
        """
        Linear interpolation of one-dimensional data
        :param x: The x-coordinate of the data point, list.
        :param y: The y-coordinate of the data point, list.
        :param x_interp: The x-coordinate of the interpolation point, list.
        :return: The y-coordinate of the interpolation point, list.
        >>> interpolation = Interpolation()
        >>> interpolation.interpolate_1d([1, 2, 3], [1, 2, 3], [1.5, 2.5])
        [1.5, 2.5]

        """
        if len(x) != len(y):
            raise ValueError("x and y must have the same length")
        if len(x) < 2:
            raise ValueError("at least two data points are required")

        n = len(x)
        for i in range(n - 1):
            if x[i] >= x[i + 1]:
                raise ValueError("x must be strictly increasing")

        result = []
        for xi in x_interp:
            if xi < x[0] or xi > x[-1]:
                raise ValueError("interpolation point out of range")

            if xi == x[-1]:
                result.append(float(y[-1]) if isinstance(y[-1], (int, float)) else y[-1])
                continue

            for i in range(n - 1):
                if x[i] <= xi <= x[i + 1]:
                    if xi == x[i]:
                        yi = y[i]
                    elif xi == x[i + 1]:
                        yi = y[i + 1]
                    else:
                        yi = y[i] + (y[i + 1] - y[i]) * (xi - x[i]) / (x[i + 1] - x[i])
                    result.append(float(yi) if isinstance(yi, (int, float)) else yi)
                    break

        return result

    @staticmethod
    def interpolate_2d(x, y, z, x_interp, y_interp):
        """
        Linear interpolation of two-dimensional data
        :param x: The x-coordinate of the data point, list.
        :param y: The y-coordinate of the data point, list.
        :param z: The z-coordinate of the data point, list.
        :param x_interp: The x-coordinate of the interpolation point, list.
        :param y_interp: The y-coordinate of the interpolation point, list.
        :return: The z-coordinate of the interpolation point, list.
        >>> interpolation = Interpolation()
        >>> interpolation.interpolate_2d([1, 2, 3], [1, 2, 3], [[1, 2, 3], [4, 5, 6], [7, 8, 9]], [1.5, 2.5], [1.5, 2.5])
        [3.0, 7.0]

        """
        if len(x) < 2 or len(y) < 2:
            raise ValueError("x and y must each contain at least two points")
        if len(x_interp) != len(y_interp):
            raise ValueError("x_interp and y_interp must have the same length")
        if len(z) != len(y):
            raise ValueError("z must have the same number of rows as y")
        for row in z:
            if len(row) != len(x):
                raise ValueError("each row of z must have the same length as x")

        for i in range(len(x) - 1):
            if x[i] >= x[i + 1]:
                raise ValueError("x must be strictly increasing")
        for i in range(len(y) - 1):
            if y[i] >= y[i + 1]:
                raise ValueError("y must be strictly increasing")

        def find_interval(arr, value):
            if value < arr[0] or value > arr[-1]:
                raise ValueError("interpolation point out of range")
            if value == arr[-1]:
                return len(arr) - 2
            for idx in range(len(arr) - 1):
                if arr[idx] <= value <= arr[idx + 1]:
                    return idx
            raise ValueError("failed to locate interpolation interval")

        result = []
        for xi, yi in zip(x_interp, y_interp):
            i = find_interval(x, xi)
            j = find_interval(y, yi)

            x1, x2 = x[i], x[i + 1]
            y1, y2 = y[j], y[j + 1]

            z11 = z[j][i]
            z21 = z[j][i + 1]
            z12 = z[j + 1][i]
            z22 = z[j + 1][i + 1]

            if x2 == x1 or y2 == y1:
                raise ValueError("grid spacing must be non-zero")

            tx = (xi - x1) / (x2 - x1)
            ty = (yi - y1) / (y2 - y1)

            z_interp = (
                z11 * (1 - tx) * (1 - ty) +
                z21 * tx * (1 - ty) +
                z12 * (1 - tx) * ty +
                z22 * tx * ty
            )
            result.append(float(z_interp) if isinstance(z_interp, (int, float)) else z_interp)

        return result

import unittest

class InterpolationTestInterpolate2d(unittest.TestCase):
    def test_interpolate_2d(self):
        interpolation = Interpolation()
        self.assertEqual(
            interpolation.interpolate_2d([1, 2, 3], [1, 2, 3], [[1, 2, 3], [4, 5, 6], [7, 8, 9]], [1.5, 2.5],
                                         [1.5, 2.5]), [3.0, 7.0])

    def test_interpolate_2d_2(self):
        interpolation = Interpolation()
        self.assertEqual(
            interpolation.interpolate_2d([1, 2, 3], [1, 2, 3], [[1, 2, 3], [4, 5, 6], [7, 8, 9]], [1.5, 2.5], [3, 4]),
            [4.5])

    def test_interpolate_2d_3(self):
        interpolation = Interpolation()
        self.assertEqual(
            interpolation.interpolate_2d([1, 2, 3], [1, 2, 3], [[1, 2, 3], [4, 5, 6], [7, 8, 9]], [3, 4], [1.5, 2.5]),
            [7.5])

    def test_interpolate_2d_4(self):
        interpolation = Interpolation()
        self.assertEqual(
            interpolation.interpolate_2d([1, 2, 3], [1, 2, 3], [[1, 2, 3], [4, 5, 6], [7, 8, 9]], [3, 4], [3, 4]),
            [9.0])

    def test_interpolate_2d_5(self):
        interpolation = Interpolation()
        self.assertEqual(
            interpolation.interpolate_2d([1, 2, 3], [1, 2, 3], [[1, 2, 3], [4, 5, 6], [7, 8, 9]], [1.5, 2.5],
                                         [1.5, 2.5]), [3.0, 7.0])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
