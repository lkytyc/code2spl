import math
import numpy as np

class VectorUtil:
    @staticmethod
    def similarity(vector_1, vector_2):
        vec1 = np.array(vector_1, dtype=float)
        vec2 = np.array(vector_2, dtype=float)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return float(np.dot(vec1 / norm1, vec2 / norm2))

    @staticmethod
    def cosine_similarities(vector_1, vectors_all):
        vec1 = np.array(vector_1, dtype=float)
        norm1 = np.linalg.norm(vec1)
        if norm1 == 0:
            return np.zeros(len(vectors_all))
        vec1_norm = vec1 / norm1
        sims = []
        for v in vectors_all:
            vec = np.array(v, dtype=float)
            norm = np.linalg.norm(vec)
            if norm == 0:
                sims.append(0.0)
            else:
                sims.append(float(np.dot(vec1_norm, vec / norm)))
        return np.array(sims)

    @staticmethod
    def n_similarity(vector_list_1, vector_list_2):
        if not vector_list_1 or not vector_list_2:
            raise ZeroDivisionError("One or both vector lists are empty")
        avg1 = np.mean(np.array(vector_list_1, dtype=float), axis=0)
        avg2 = np.mean(np.array(vector_list_2, dtype=float), axis=0)
        norm1 = np.linalg.norm(avg1)
        norm2 = np.linalg.norm(avg2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return float(np.dot(avg1 / norm1, avg2 / norm2))

    @staticmethod
    def compute_idf_weight_dict(total_num, number_dict):
        idf_dict = {}
        for term, count in number_dict.items():
            idf_dict[term] = math.log((total_num + 1) / (count + 1)) + 1
        return idf_dict

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
