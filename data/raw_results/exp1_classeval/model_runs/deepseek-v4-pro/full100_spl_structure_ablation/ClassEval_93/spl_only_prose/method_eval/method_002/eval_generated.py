import numpy as np
from gensim import matutils


class VectorUtil:

    def compute_idf_weight_dict(self, total_num, number_dict):
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

    def cosine_similarities(self, vector_1, vectors_all):
        norm = np.linalg.norm(vector_1)
        all_norms = np.linalg.norm(vectors_all, axis=1)
        dot_products = np.dot(vectors_all, vector_1)
        similarities = dot_products / (norm * all_norms)
        return similarities

    def n_similarity(self, vector_list_1, vector_list_2):
        if len(vector_list_1) == 0 or len(vector_list_2) == 0:
            raise ZeroDivisionError("At least one of the passed list is empty.")
        mean_vector_1 = np.mean(np.array(vector_list_1), axis=0)
        unit_vector_1 = matutils.unitvec(mean_vector_1)
        mean_vector_2 = np.mean(np.array(vector_list_2), axis=0)
        unit_vector_2 = matutils.unitvec(mean_vector_2)
        return_value = np.dot(unit_vector_1, unit_vector_2)
        return return_value

    def similarity(self, vector_1, vector_2):
        unit_vector_1 = matutils.unitvec(vector_1)
        unit_vector_2 = matutils.unitvec(vector_2)
        result = np.dot(unit_vector_1, unit_vector_2)
        return result

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
