class Interpolation:
    def __init__(self):
        pass

    @staticmethod
    def interpolate_1d(x, y, x_interp):
        interpolated = []
        n = min(len(x), len(y))
        if n < 2:
            return interpolated

        for x_val in x_interp:
            for i in range(n - 1):
                x0, x1 = x[i], x[i + 1]
                y0, y1 = y[i], y[i + 1]

                if x0 <= x_val <= x1 or x1 <= x_val <= x0:
                    if x1 == x0:
                        interpolated.append(y0)
                    else:
                        t = (x_val - x0) / (x1 - x0)
                        interpolated.append(y0 + t * (y1 - y0))
                    break
        return interpolated

    @staticmethod
    def interpolate_2d(x, y, z, x_interp, y_interp):
        interpolated = []
        nx = len(x)
        ny = len(y)
        if nx < 2 or ny < 2:
            return interpolated

        for xi, yi in zip(x_interp, y_interp):
            found = False
            for i in range(nx - 1):
                x0, x1 = x[i], x[i + 1]
                if not (x0 <= xi <= x1 or x1 <= xi <= x0):
                    continue
                if x1 == x0:
                    tx = 0.0
                else:
                    tx = (xi - x0) / (x1 - x0)

                for j in range(ny - 1):
                    y0, y1 = y[j], y[j + 1]
                    if not (y0 <= yi <= y1 or y1 <= yi <= y0):
                        continue
                    if y1 == y0:
                        ty = 0.0
                    else:
                        ty = (yi - y0) / (y1 - y0)

                    z00 = z[i][j]
                    z10 = z[i + 1][j]
                    z01 = z[i][j + 1]
                    z11 = z[i + 1][j + 1]

                    z_interp = (
                        (1 - tx) * (1 - ty) * z00
                        + tx * (1 - ty) * z10
                        + (1 - tx) * ty * z01
                        + tx * ty * z11
                    )
                    interpolated.append(z_interp)
                    found = True
                    break
                if found:
                    break
        return interpolated

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


class InterpolationTestMain(unittest.TestCase):
    def test_main(self):
        interpolation = Interpolation()
        self.assertEqual(interpolation.interpolate_1d([1, 2, 3], [1, 2, 3], [1.5, 2.5]), [1.5, 2.5])
        self.assertEqual(
            interpolation.interpolate_2d([1, 2, 3], [1, 2, 3], [[1, 2, 3], [4, 5, 6], [7, 8, 9]], [1.5, 2.5],
                                         [1.5, 2.5]), [3.0, 7.0])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
