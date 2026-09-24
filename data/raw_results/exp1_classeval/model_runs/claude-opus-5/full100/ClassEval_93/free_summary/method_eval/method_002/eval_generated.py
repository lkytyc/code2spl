import numpy as np
from gensim.matutils import unitvec


class VectorUtil:

    @staticmethod
    def similarity(vector_1, vector_2):
        return np.dot(unitvec(vector_1), unitvec(vector_2))

    @staticmethod
    def cosine_similarities(vector_1, vectors_all):
        norm = np.linalg.norm(vector_1)
        all_norms = np.linalg.norm(vectors_all, axis=1)
        dot_products = np.dot(vectors_all, vector_1)
        similarities = dot_products / (norm * all_norms)
        return similarities

    @staticmethod
    def n_similarity(vector_list_1, vector_list_2):
        if not vector_list_1 or not vector_list_2:
            raise ZeroDivisionError("At least one of the vector lists is empty.")
        mean_1 = np.mean(vector_list_1, axis=0)
        mean_2 = np.mean(vector_list_2, axis=0)
        return VectorUtil.similarity(mean_1, mean_2)

    @staticmethod
    def compute_idf_weight_dict(total_num, count_dict):
        keys = list(count_dict.keys())
        counts = np.array([count_dict[k] for k in keys], dtype=float)
        idf_weights = np.log((total_num + 1) / (counts + 1))
        return {keys[i]: idf_weights[i] for i in range(len(keys))}

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
