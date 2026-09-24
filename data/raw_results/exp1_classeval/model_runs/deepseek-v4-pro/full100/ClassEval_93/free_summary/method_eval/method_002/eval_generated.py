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

class VectorUtilTestNSimilarity(unittest.TestCase):
    def test_n_similarity_1(self):
        vector_list1 = [np.array([1, 0]), np.array([0, 1])]
        vector_list2 = [np.array([0, 0]), np.array([1, 1])]
        similarity = VectorUtil.n_similarity(vector_list1, vector_list2)
        self.assertAlmostEqual(similarity, 1.0)

    def test_n_similarity_2(self):
        vector_list1 = [np.array([1, 1]), np.array([0, 1])]
        vector_list2 = [np.array([0, 0]), np.array([1, 1])]
        similarity = VectorUtil.n_similarity(vector_list1, vector_list2)
        self.assertAlmostEqual(similarity, 0.9486832980505137)

    def test_n_similarity_3(self):
        vector_list1 = [np.array([1, 0]), np.array([1, 1])]
        vector_list2 = [np.array([0, 0]), np.array([1, 1])]
        similarity = VectorUtil.n_similarity(vector_list1, vector_list2)
        self.assertAlmostEqual(similarity, 0.9486832980505137)

    def test_n_similarity_4(self):
        vector_list1 = [np.array([1, 0]), np.array([0, 1])]
        vector_list2 = [np.array([1, 0]), np.array([1, 1])]
        similarity = VectorUtil.n_similarity(vector_list1, vector_list2)
        self.assertAlmostEqual(similarity, 0.9486832980505137)

    def test_n_similarity_5(self):
        vector_list1 = [np.array([1, 0]), np.array([0, 1])]
        vector_list2 = [np.array([0, 1]), np.array([1, 1])]
        similarity = VectorUtil.n_similarity(vector_list1, vector_list2)
        self.assertAlmostEqual(similarity, 0.9486832980505137)

    def test_n_similarity_6(self):
        try:
            vector_list1 = []
            vector_list2 = []
            similarity = VectorUtil.n_similarity(vector_list1, vector_list2)
        except:
            pass

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
