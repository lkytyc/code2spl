class VectorUtil:
    @staticmethod
    def compute_idf_weight_dict(total_num, number_dict):
        import numpy as np

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
        for i, weight in enumerate(a):
            result[index_2_key_map[i]] = weight
        return result

    @staticmethod
    def cosine_similarities(vector_1, vectors_all):
        import numpy as np

        norm = np.linalg.norm(vector_1)
        all_norms = np.linalg.norm(vectors_all, axis=1)
        dot_products = np.dot(vectors_all, vector_1)
        similarities = dot_products / (norm * all_norms)
        return similarities

    @staticmethod
    def n_similarity(vector_list_1, vector_list_2):
        import numpy as np

        if not vector_list_1 or not vector_list_2:
            raise ZeroDivisionError(
                "Indicates that at least one passed list is empty."
            )
        normalized_mean_1 = np.mean(np.asarray(vector_list_1), axis=0)
        normalized_mean_1 = normalized_mean_1 / np.linalg.norm(normalized_mean_1)
        normalized_mean_2 = np.mean(np.asarray(vector_list_2), axis=0)
        normalized_mean_2 = normalized_mean_2 / np.linalg.norm(normalized_mean_2)
        result = np.dot(normalized_mean_1, normalized_mean_2)
        return result

    @staticmethod
    def similarity(vector_1, vector_2):
        try:
            from gensim import matutils
        except Exception:
            import numpy as np

            def _unitvec(v):
                v = np.asarray(v)
                n = np.linalg.norm(v)
                return v / n
            matutils = type("_M", (), {"unitvec": staticmethod(_unitvec)})

        inputs = (vector_1, vector_2)
        normalized_vector_1 = matutils.unitvec(vector_1)
        normalized_vector_2 = matutils.unitvec(vector_2)
        similarity_score = normalized_vector_1.dot(normalized_vector_2)
        return similarity_score

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
