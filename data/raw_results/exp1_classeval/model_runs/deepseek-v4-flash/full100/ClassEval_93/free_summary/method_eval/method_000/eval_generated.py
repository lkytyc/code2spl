import math
import numpy as np

class VectorUtil:
    @staticmethod
    def similarity(v1, v2):
        v1_norm = np.linalg.norm(v1)
        v2_norm = np.linalg.norm(v2)
        return float(np.dot(v1, v2) / (v1_norm * v2_norm))

    @staticmethod
    def cosine_similarities(vector_1, vectors_all):
        norm = np.linalg.norm(vector_1)
        all_norms = np.linalg.norm(vectors_all, axis=1)
        dot_products = np.dot(vectors_all, vector_1)
        return dot_products / (norm * all_norms)

    @staticmethod
    def n_similarity(vector_list_1, vector_list_2):
        if len(vector_list_1) == 0 or len(vector_list_2) == 0:
            raise ZeroDivisionError("Cannot compute n_similarity with an empty list")
        vector1 = np.mean(vector_list_1, axis=0)
        vector2 = np.mean(vector_list_2, axis=0)
        return VectorUtil.similarity(vector1, vector2)

    @staticmethod
    def compute_idf_weight_dict(total_num, idf_dict):
        return {term: math.log((total_num + 1) / (count + 1)) for term, count in idf_dict.items()}

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
