import numpy as np
from gensim import matutils
from numpy import dot, array

class VectorUtil:

    @staticmethod
    def similarity(vector_1, vector_2):
        unit_vector_1 = matutils.unitvec(vector_1)
        unit_vector_2 = matutils.unitvec(vector_2)
        similarity_score = dot(unit_vector_1, unit_vector_2)
        return similarity_score

    @staticmethod
    def cosine_similarities(vector_1, vectors_all):
        norm = np.linalg.norm(vector_1)
        all_norms = np.linalg.norm(vectors_all, axis=1)
        dot_products = dot(vectors_all, vector_1)
        similarities = dot_products / (norm * all_norms)
        return similarities

    @staticmethod
    def n_similarity(vector_list_1, vector_list_2):
        if not (len(vector_list_1) and len(vector_list_2)):
            raise ZeroDivisionError("At least one of the passed list is empty.")
        array_1 = np.array(vector_list_1)
        centroid_1 = array_1.mean(axis=0)
        unit_vector_1 = matutils.unitvec(centroid_1)
        array_2 = np.array(vector_list_2)
        centroid_2 = array_2.mean(axis=0)
        unit_vector_2 = matutils.unitvec(centroid_2)
        similarity_score = dot(unit_vector_1, unit_vector_2)
        return similarity_score

    @staticmethod
    def compute_idf_weight_dict(total_num, number_dict):
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
        for index, w in enumerate(a):
            key = index_2_key_map[index]
            result[key] = w
        return result

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
