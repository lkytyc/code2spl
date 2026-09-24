class Interpolation:
    def __init__(self):
        pass

    @staticmethod
    def interpolate_1d(x, y, x_interp):
        interpolated = []
        for xi in x_interp:
            for i in range(len(x) - 1):
                if x[i] <= xi <= x[i + 1]:
                    x0, x1 = x[i], x[i + 1]
                    y0, y1 = y[i], y[i + 1]
                    if x1 == x0:
                        yi = y0
                    else:
                        yi = y0 + (xi - x0) * (y1 - y0) / (x1 - x0)
                    interpolated.append(yi)
                    break
        return interpolated

    @staticmethod
    def interpolate_2d(x, y, z, x_interp, y_interp):
        interpolated = []
        for xi, yi in zip(x_interp, y_interp):
            found = False
            for i in range(len(x) - 1):
                if x[i] <= xi <= x[i + 1]:
                    for j in range(len(y) - 1):
                        if y[j] <= yi <= y[j + 1]:
                            x0, x1 = x[i], x[i + 1]
                            y0, y1 = y[j], y[j + 1]

                            z00 = z[i][j]
                            z01 = z[i][j + 1]
                            z10 = z[i + 1][j]
                            z11 = z[i + 1][j + 1]

                            if x1 == x0 and y1 == y0:
                                zi = z00
                            elif x1 == x0:
                                zi = z00 + (yi - y0) * (z01 - z00) / (y1 - y0)
                            elif y1 == y0:
                                zi = z00 + (xi - x0) * (z10 - z00) / (x1 - x0)
                            else:
                                zi = (
                                    z00 * (x1 - xi) * (y1 - yi) +
                                    z10 * (xi - x0) * (y1 - yi) +
                                    z01 * (x1 - xi) * (yi - y0) +
                                    z11 * (xi - x0) * (yi - y0)
                                ) / ((x1 - x0) * (y1 - y0))

                            interpolated.append(zi)
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

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
