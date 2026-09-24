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

class VectorUtilTestSimilarity(unittest.TestCase):
    def test_similarity_1(self):
        vector_1 = np.array([1, 1])
        vector_2 = np.array([1, 0])
        similarity = VectorUtil.similarity(vector_1, vector_2)
        self.assertAlmostEqual(similarity, 0.7071067811865475)

    def test_similarity_2(self):
        vector_1 = np.array([1, 1])
        vector_2 = np.array([0, 0])
        similarity = VectorUtil.similarity(vector_1, vector_2)
        self.assertAlmostEqual(similarity, 0.0)

    def test_similarity_3(self):
        vector_1 = np.array([1, 1])
        vector_2 = np.array([1, 1])
        similarity = VectorUtil.similarity(vector_1, vector_2)
        self.assertAlmostEqual(similarity, 1.0)

    def test_similarity_4(self):
        vector_1 = np.array([1, 1, 0, 1, 0, 1, 0, 1])
        vector_2 = np.array([1, 0, 0, 1, 0, 1, 0, 1])
        similarity = VectorUtil.similarity(vector_1, vector_2)
        self.assertAlmostEqual(similarity, 0.8944271909999159)

    def test_similarity_5(self):
        vector_1 = np.array([1, 1, 1, 1, 1, 1, 1, 1])
        vector_2 = np.array([0, 0, 0, 0, 0, 0, 0, 0])
        similarity = VectorUtil.similarity(vector_1, vector_2)
        self.assertAlmostEqual(similarity, 0.0)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
