class VectorUtil:
    @staticmethod
    def similarity(vector_1, vector_2):
        import numpy as np
        from gensim.matutils import unitvec

        return float(np.dot(unitvec(vector_1), unitvec(vector_2)))

    @staticmethod
    def cosine_similarities(vector_1, vectors_all):
        import numpy as np

        vector_1 = np.asarray(vector_1)
        vectors_all = np.asarray(vectors_all)

        norms = np.linalg.norm(vectors_all, axis=1)
        vec1_norm = np.linalg.norm(vector_1)
        dots = np.dot(vectors_all, vector_1)
        return dots / (norms * vec1_norm)

    @staticmethod
    def n_similarity(vector_list_1, vector_list_2):
        import numpy as np
        from gensim.matutils import unitvec

        if not vector_list_1 or not vector_list_2:
            raise ZeroDivisionError("At least one of the input lists is empty.")

        mean_1 = np.mean(vector_list_1, axis=0)
        mean_2 = np.mean(vector_list_2, axis=0)
        return float(np.dot(unitvec(mean_1), unitvec(mean_2)))

    @staticmethod
    def compute_idf_weight_dict(total_num, number_dict):
        import math

        return {key: math.log((total_num + 1) / (count + 1)) for key, count in number_dict.items()}

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
