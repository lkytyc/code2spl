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

class VectorUtilTestCosineSimilarities(unittest.TestCase):
    def test_cosine_similarities_1(self):
        vector1 = np.array([1, 1])
        vectors_all = [np.array([1, 0]), np.array([1, 1])]
        similarities = VectorUtil.cosine_similarities(vector1, vectors_all)
        res = [0.7071067811865475, 1.0]
        for index, item in enumerate(similarities):
            self.assertAlmostEqual(item, res[index])

    def test_cosine_similarities_2(self):
        vector1 = np.array([1, 1, 0, 0, 1, 0, 1, 0])
        vectors_all = [np.array([1, 0, 0, 0, 1, 0, 1, 0]), np.array([1, 1, 0, 1, 1, 1, 1, 0])]
        similarities = VectorUtil.cosine_similarities(vector1, vectors_all)
        res = [0.8660254037844387, 0.8164965809277261]
        for index, item in enumerate(similarities):
            self.assertAlmostEqual(item, res[index])

    def test_cosine_similarities_3(self):
        vector1 = np.array([1, 1, 0, 0, 1, 0, 1, 0])
        vectors_all = [np.array([1, 0, 0, 0, 1, 0, 1, 0]), np.array([1, 1, 1, 1, 1, 1, 1, 0])]
        similarities = VectorUtil.cosine_similarities(vector1, vectors_all)
        res = [0.8660254037844387, 0.7559289460184544]
        for index, item in enumerate(similarities):
            self.assertAlmostEqual(item, res[index])

    def test_cosine_similarities_4(self):
        vector1 = np.array([1, 1, 0, 0, 1, 0, 1, 0])
        vectors_all = [np.array([1, 0, 0, 0, 1, 0, 1, 0]), np.array([1, 1, 1, 1, 1, 1, 1, 1])]
        similarities = VectorUtil.cosine_similarities(vector1, vectors_all)
        res = [0.8660254037844387, 0.7071067811865475]
        for index, item in enumerate(similarities):
            self.assertAlmostEqual(item, res[index])

    def test_cosine_similarities_5(self):
        vector1 = np.array([1, 1, 0, 0, 1, 0, 1, 0])
        vectors_all = [np.array([1, 0, 0, 0, 1, 0, 1, 0]), np.array([0, 1, 1, 1, 1, 1, 1, 1])]
        similarities = VectorUtil.cosine_similarities(vector1, vectors_all)
        res = [0.8660254037844387, 0.5669467095138409]
        for index, item in enumerate(similarities):
            self.assertAlmostEqual(item, res[index])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
