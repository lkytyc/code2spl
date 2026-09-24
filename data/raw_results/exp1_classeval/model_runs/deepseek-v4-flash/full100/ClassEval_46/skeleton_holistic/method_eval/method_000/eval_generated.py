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
        result = []
        for xi in x_interp:
            # Find the interval containing xi
            for i in range(len(x) - 1):
                if x[i] <= xi <= x[i+1]:
                    # Linear interpolation formula
                    t = (xi - x[i]) / (x[i+1] - x[i])
                    yi = y[i] + t * (y[i+1] - y[i])
                    result.append(yi)
                    break
            else:
                # If xi is outside the range, extrapolate using the nearest interval
                if xi < x[0]:
                    t = (xi - x[0]) / (x[1] - x[0])
                    yi = y[0] + t * (y[1] - y[0])
                else:
                    t = (xi - x[-2]) / (x[-1] - x[-2])
                    yi = y[-2] + t * (y[-1] - y[-2])
                result.append(yi)
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
        result = []
        for xi, yi in zip(x_interp, y_interp):
            # Find the x interval
            for i in range(len(x) - 1):
                if x[i] <= xi <= x[i+1]:
                    x_idx = i
                    break
            else:
                if xi < x[0]:
                    x_idx = 0
                else:
                    x_idx = len(x) - 2

            # Find the y interval
            for j in range(len(y) - 1):
                if y[j] <= yi <= y[j+1]:
                    y_idx = j
                    break
            else:
                if yi < y[0]:
                    y_idx = 0
                else:
                    y_idx = len(y) - 2

            # Bilinear interpolation
            x0, x1 = x[x_idx], x[x_idx+1]
            y0, y1 = y[y_idx], y[y_idx+1]
            z00 = z[x_idx][y_idx]
            z01 = z[x_idx][y_idx+1]
            z10 = z[x_idx+1][y_idx]
            z11 = z[x_idx+1][y_idx+1]

            # Interpolate in x direction
            z0 = z00 + (z10 - z00) * (xi - x0) / (x1 - x0)
            z1 = z01 + (z11 - z01) * (xi - x0) / (x1 - x0)
            # Interpolate in y direction
            zi = z0 + (z1 - z0) * (yi - y0) / (y1 - y0)
            result.append(zi)
        return result

import unittest

class InterpolationTestInterpolate1d(unittest.TestCase):
    def test_interpolate_1d(self):
        interpolation = Interpolation()
        self.assertEqual(interpolation.interpolate_1d([1, 2, 3], [1, 2, 3], [1.5, 2.5]), [1.5, 2.5])

    def test_interpolate_1d_2(self):
        interpolation = Interpolation()
        self.assertEqual(interpolation.interpolate_1d([1, 6, 4], [1, 2, 5], [1.5, 2.5]), [1.1, 1.3])

    def test_interpolate_1d_3(self):
        interpolation = Interpolation()
        self.assertEqual(interpolation.interpolate_1d([1, 6, 4], [1, 7, 5], [1.5, 2.5]), [1.6, 2.8])

    def test_interpolate_1d_4(self):
        interpolation = Interpolation()
        self.assertEqual(interpolation.interpolate_1d([1, 6, 4], [1, 2, 5], [2, 3]), [1.2, 1.4])

    def test_interpolate_1d_5(self):
        interpolation = Interpolation()
        self.assertEqual(interpolation.interpolate_1d([1, 6, 4], [1, 7, 5], [2, 3]), [2.2, 3.4])

    def test_interpolate_1d_6(self):
        interpolation = Interpolation()
        self.assertEqual(interpolation.interpolate_1d([1, 6, 4], [1, 7, 5], []), [])

    def test_interpolate_1d_7(self):
        interpolation = Interpolation()
        self.assertEqual(interpolation.interpolate_1d([], [], [[], []]), [])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
