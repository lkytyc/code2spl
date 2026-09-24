class Interpolation:
    def __init__(self):
        pass

    @staticmethod
    def interpolate_1d(x_known, y_known, x_interp):
        results = []
        for xq in x_interp:
            for i in range(len(x_known) - 1):
                if x_known[i] <= xq <= x_known[i + 1]:
                    t = (xq - x_known[i]) / (x_known[i + 1] - x_known[i])
                    y = y_known[i] + t * (y_known[i + 1] - y_known[i])
                    results.append(y)
                    break
        return results

    @staticmethod
    def interpolate_2d(x_known, y_known, z_grid, x_interp, y_interp):
        results = []
        for xq, yq in zip(x_interp, y_interp):
            xi = None
            for i in range(len(x_known) - 1):
                if x_known[i] <= xq <= x_known[i + 1]:
                    xi = i
                    break
            if xi is None:
                continue

            yi = None
            for j in range(len(y_known) - 1):
                if y_known[j] <= yq <= y_known[j + 1]:
                    yi = j
                    break
            if yi is None:
                continue

            x0, x1 = x_known[xi], x_known[xi + 1]
            y0, y1 = y_known[yi], y_known[yi + 1]

            z00 = z_grid[yi][xi]
            z10 = z_grid[yi][xi + 1]
            z01 = z_grid[yi + 1][xi]
            z11 = z_grid[yi + 1][xi + 1]

            tx = (xq - x0) / (x1 - x0)
            ty = (yq - y0) / (y1 - y0)

            z = (z00 * (1 - tx) * (1 - ty)
               + z10 * tx * (1 - ty)
               + z01 * (1 - tx) * ty
               + z11 * tx * ty)

            results.append(z)
        return results

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
