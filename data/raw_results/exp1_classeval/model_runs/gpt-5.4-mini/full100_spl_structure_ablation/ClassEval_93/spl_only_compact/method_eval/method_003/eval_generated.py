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

class VectorUtilTestComputeIdfWeightDict(unittest.TestCase):
    def test_compute_idf_weight_dict_1(self):
        num_dict = {'key1': 0.1, 'key2': 0.5}
        res = VectorUtil.compute_idf_weight_dict(2, num_dict)
        self.assertAlmostEqual(res['key1'], 1.0033021088637848)
        self.assertAlmostEqual(res['key2'], 0.6931471805599453)

    def test_compute_idf_weight_dict_2(self):
        num_dict = {'key1': 0.2, 'key2': 0.5}
        res = VectorUtil.compute_idf_weight_dict(2, num_dict)
        self.assertAlmostEqual(res['key1'], 0.9162907318741551)
        self.assertAlmostEqual(res['key2'], 0.6931471805599453)

    def test_compute_idf_weight_dict_3(self):
        num_dict = {'key1': 0.3, 'key2': 0.5}
        res = VectorUtil.compute_idf_weight_dict(2, num_dict)
        self.assertAlmostEqual(res['key1'], 0.8362480242006185)
        self.assertAlmostEqual(res['key2'], 0.6931471805599453)

    def test_compute_idf_weight_dict_4(self):
        num_dict = {'key1': 0.4, 'key2': 0.5}
        res = VectorUtil.compute_idf_weight_dict(2, num_dict)
        self.assertAlmostEqual(res['key1'], 0.7621400520468967)
        self.assertAlmostEqual(res['key2'], 0.6931471805599453)

    def test_compute_idf_weight_dict_5(self):
        num_dict = {'key1': 0.5, 'key2': 0.5}
        res = VectorUtil.compute_idf_weight_dict(2, num_dict)
        self.assertAlmostEqual(res['key1'], 0.6931471805599453)
        self.assertAlmostEqual(res['key2'], 0.6931471805599453)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
