import math
import numpy as np
from gensim import matutils


class VectorUtil:
    @staticmethod
    def similarity(vector_1, vector_2):
        v1 = matutils.unitvec(np.asarray(vector_1, dtype=float))
        v2 = matutils.unitvec(np.asarray(vector_2, dtype=float))
        return float(np.dot(v1, v2))

    @staticmethod
    def cosine_similarities(vector_1, vectors_all):
        v1 = np.asarray(vector_1, dtype=float)
        va = np.asarray(vectors_all, dtype=float)

        v1_norm = np.linalg.norm(v1)
        va_norms = np.linalg.norm(va, axis=1)
        dots = np.dot(va, v1)

        with np.errstate(divide='ignore', invalid='ignore'):
            sims = dots / (va_norms * v1_norm)
        sims = np.where(np.isfinite(sims), sims, 0.0)
        return sims

    @staticmethod
    def n_similarity(vector_list_1, vector_list_2):
        if not vector_list_1 or not vector_list_2:
            raise ZeroDivisionError("At least one of the input vector lists is empty")

        mean_1 = np.asarray(vector_list_1, dtype=float).mean(axis=0)
        mean_2 = np.asarray(vector_list_2, dtype=float).mean(axis=0)

        mean_1 = matutils.unitvec(mean_1)
        mean_2 = matutils.unitvec(mean_2)

        return float(np.dot(mean_1, mean_2))

    @staticmethod
    def compute_idf_weight_dict(total_num, number_dict):
        return {
            key: math.log((total_num + 1) / (count + 1))
            for key, count in number_dict.items()
        }

import unittest

class VectorUtilTestComputeIdfWeightDict(unittest.TestCase):
    def test_compute_idf_weight_dict_1(self):
        num_dict = {'key1': 0.1, 'key2': 0.5}
        res = VectorUtil.compute_idf_weight_dict(2, num_dict)
        self.assertAlmostEqual(res['key1'], 1.0033021088637848)
        self.assertAlmostEqual(res['key2'], 0.6931471805599453)

    def test_compute_idf_weight_dict_2(self):
        num_dict = {'key1': 0.2, 'key2': 0.5}
        res = VectorUtil.compute_idf_weight_dict(2, num_dict)
        self.assertAlmostEqual(res['key1'], 0.9162907318741551)
        self.assertAlmostEqual(res['key2'], 0.6931471805599453)

    def test_compute_idf_weight_dict_3(self):
        num_dict = {'key1': 0.3, 'key2': 0.5}
        res = VectorUtil.compute_idf_weight_dict(2, num_dict)
        self.assertAlmostEqual(res['key1'], 0.8362480242006185)
        self.assertAlmostEqual(res['key2'], 0.6931471805599453)

    def test_compute_idf_weight_dict_4(self):
        num_dict = {'key1': 0.4, 'key2': 0.5}
        res = VectorUtil.compute_idf_weight_dict(2, num_dict)
        self.assertAlmostEqual(res['key1'], 0.7621400520468967)
        self.assertAlmostEqual(res['key2'], 0.6931471805599453)

    def test_compute_idf_weight_dict_5(self):
        num_dict = {'key1': 0.5, 'key2': 0.5}
        res = VectorUtil.compute_idf_weight_dict(2, num_dict)
        self.assertAlmostEqual(res['key1'], 0.6931471805599453)
        self.assertAlmostEqual(res['key2'], 0.6931471805599453)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
