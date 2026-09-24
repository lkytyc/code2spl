class VectorUtil:
    @staticmethod
    def similarity(vector_1, vector_2):
        normalized_vector_1 = matutils.unitvec(vector_1)
        normalized_vector_2 = matutils.unitvec(vector_2)
        dot_product = float(numpy.dot(normalized_vector_1, normalized_vector_2))
        return dot_product

    @staticmethod
    def cosine_similarities(vector_1, vectors_all):
        norm = numpy.linalg.norm(vector_1)
        all_norms = numpy.linalg.norm(vectors_all, axis=1)
        dot_products = numpy.dot(vectors_all, vector_1)
        similarities = dot_products / (norm * all_norms)
        return similarities

    @staticmethod
    def n_similarity(vector_list_1, vector_list_2):
        if not (len(vector_list_1) and len(vector_list_2)):
            raise ZeroDivisionError("At least one of the passed list is empty.")
        mean_vector_1 = numpy.array(vector_list_1).mean(axis=0)
        unit_mean_vector_1 = matutils.unitvec(mean_vector_1)
        mean_vector_2 = numpy.array(vector_list_2).mean(axis=0)
        unit_mean_vector_2 = matutils.unitvec(mean_vector_2)
        return float(numpy.dot(unit_mean_vector_1, unit_mean_vector_2))

    @staticmethod
    def compute_idf_weight_dict(total_num, number_dict):
        index_2_key_map = {}
        index = 0
        count_list = []
        for key, count in number_dict.items():
            index_2_key_map[index] = key
            count_list.append(count)
            index += 1
        a = numpy.array(count_list)
        a = numpy.log((total_num + 1) / (a + 1))
        result = {}
        for index, w in enumerate(a):
            key = index_2_key_map[index]
            result[key] = w
        return result

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
