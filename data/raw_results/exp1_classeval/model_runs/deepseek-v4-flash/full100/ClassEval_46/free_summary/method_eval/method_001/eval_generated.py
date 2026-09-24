class Interpolation:
    @staticmethod
    def interpolate_1d(x, y, x_query):
        results = []
        for xq in x_query:
            if xq <= x[0]:
                results.append(y[0])
            elif xq >= x[-1]:
                results.append(y[-1])
            else:
                for i in range(len(x) - 1):
                    if x[i] <= xq <= x[i + 1]:
                        t = (xq - x[i]) / (x[i + 1] - x[i])
                        results.append(y[i] + t * (y[i + 1] - y[i]))
                        break
        return results

    @staticmethod
    def interpolate_2d(x, y, z, x_query, y_query):
        results = []
        for xq, yq in zip(x_query, y_query):
            if xq <= x[0]:
                xi = 0
            elif xq >= x[-1]:
                xi = len(x) - 2
            else:
                for i in range(len(x) - 1):
                    if x[i] <= xq <= x[i + 1]:
                        xi = i
                        break
            if yq <= y[0]:
                yi = 0
            elif yq >= y[-1]:
                yi = len(y) - 2
            else:
                for j in range(len(y) - 1):
                    if y[j] <= yq <= y[j + 1]:
                        yi = j
                        break
            x0, x1 = x[xi], x[xi + 1]
            y0, y1 = y[yi], y[yi + 1]
            tx = (xq - x0) / (x1 - x0)
            ty = (yq - y0) / (y1 - y0)
            z00 = z[yi][xi]
            z10 = z[yi][xi + 1]
            z01 = z[yi + 1][xi]
            z11 = z[yi + 1][xi + 1]
            z_top = z00 + tx * (z10 - z00)
            z_bottom = z01 + tx * (z11 - z01)
            results.append(z_top + ty * (z_bottom - z_top))
        return results

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
