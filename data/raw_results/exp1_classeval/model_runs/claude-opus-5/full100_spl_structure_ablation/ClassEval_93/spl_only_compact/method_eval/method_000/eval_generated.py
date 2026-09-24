import numpy as np
from gensim import matutils


class VectorUtil:

    @staticmethod
    def compute_idf_weight_dict(total_num: int, number_dict: dict) -> dict:
        index_2_key_map = {}
        index = 0
        count_list = []

        for key, count in number_dict.items():
            index_2_key_map[index] = key
            count_list.append(count)
            index += 1

        a = np.array(count_list)
        a = np.log((total_num + 1) / (a + 1))

        result = {}
        for idx, w in enumerate(a):
            key = index_2_key_map[idx]
            result[key] = w

        return result

    def cosine_similarities(self, vector_1, vectors_all, dot):
        norm = np.linalg.norm(vector_1)
        all_norms = np.linalg.norm(vectors_all, axis=1)
        dot_products = dot(vectors_all, vector_1)
        similarities = dot_products / (norm * all_norms)
        return similarities

    def n_similarity(self, vector_list_1: list, vector_list_2: list) -> float:
        if not vector_list_1 or not vector_list_2:
            raise ZeroDivisionError("At least one of the passed list is empty.")

        array_1 = np.array(vector_list_1)
        centroid_1 = array_1.mean(axis=0)
        unit_centroid_1 = matutils.unitvec(centroid_1)

        array_2 = np.array(vector_list_2)
        centroid_2 = array_2.mean(axis=0)
        unit_centroid_2 = matutils.unitvec(centroid_2)

        similarity = np.dot(unit_centroid_1, unit_centroid_2)
        return similarity

    def similarity(self, vector_1, vector_2, dot):
        unit_vector_1 = matutils.unitvec(vector_1)
        unit_vector_2 = matutils.unitvec(vector_2)
        similarity_score = dot(unit_vector_1, unit_vector_2)
        return similarity_score

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
