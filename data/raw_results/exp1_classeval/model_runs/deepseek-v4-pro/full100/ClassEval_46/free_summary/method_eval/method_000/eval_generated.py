class Interpolation:
    @staticmethod
    def interpolate_1d(x, y, x_interp):
        result = []
        for xq in x_interp:
            if xq <= x[0]:
                i = 0
            elif xq >= x[-1]:
                i = len(x) - 2
            else:
                i = 0
                while i < len(x) - 1 and not (x[i] <= xq <= x[i + 1]):
                    i += 1
            t = (xq - x[i]) / (x[i + 1] - x[i])
            yq = y[i] * (1 - t) + y[i + 1] * t
            result.append(yq)
        return result

    @staticmethod
    def interpolate_2d(x, y, z, x_interp, y_interp):
        result = []
        for xq, yq in zip(x_interp, y_interp):
            if xq <= x[0]:
                i = 0
            elif xq >= x[-1]:
                i = len(x) - 2
            else:
                i = 0
                while i < len(x) - 1 and not (x[i] <= xq <= x[i + 1]):
                    i += 1

            if yq <= y[0]:
                j = 0
            elif yq >= y[-1]:
                j = len(y) - 2
            else:
                j = 0
                while j < len(y) - 1 and not (y[j] <= yq <= y[j + 1]):
                    j += 1

            tx = (xq - x[i]) / (x[i + 1] - x[i])
            ty = (yq - y[j]) / (y[j + 1] - y[j])

            z00 = z[j][i]
            z10 = z[j][i + 1]
            z01 = z[j + 1][i]
            z11 = z[j + 1][i + 1]

            zq = (z00 * (1 - tx) * (1 - ty) +
                  z10 * tx * (1 - ty) +
                  z01 * (1 - tx) * ty +
                  z11 * tx * ty)
            result.append(zq)
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
