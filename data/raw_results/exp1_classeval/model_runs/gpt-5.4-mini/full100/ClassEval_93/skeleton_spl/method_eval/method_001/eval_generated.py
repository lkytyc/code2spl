class VectorUtil:
    """
    The class provides vector operations, including calculating similarity, cosine similarities, average similarity, and IDF weights.
    """

    @staticmethod
    def similarity(vector_1, vector_2):
        """
        Compute the cosine similarity between one vector and another vector.
        :param vector_1: numpy.ndarray, Vector from which similarities are to be computed, expected shape (dim,).
        :param vector_2: numpy.ndarray, Vector from which similarities are to be computed, expected shape (dim,).
        :return: numpy.ndarray, Contains cosine distance between `vector_1` and `vector_2`
        >>> vector_1 = np.array([1, 1])
        >>> vector_2 = np.array([1, 0])
        >>> VectorUtil.similarity(vector_1, vector_2)
        0.7071067811865475
        """
        normalized_vector_1 = matutils.unitvec(vector_1)
        normalized_vector_2 = matutils.unitvec(vector_2)
        return dot(normalized_vector_1, normalized_vector_2)

    @staticmethod
    def cosine_similarities(vector_1, vectors_all):
        """
        Compute cosine similarities between one vector and a set of other vectors.
        :param vector_1: numpy.ndarray, Vector from which similarities are to be computed, expected shape (dim,).
        :param vectors_all: list of numpy.ndarray, For each row in vectors_all, distance from vector_1 is computed, expected shape (num_vectors, dim).
        :return: numpy.ndarray, Contains cosine distance between `vector_1` and each row in `vectors_all`, shape (num_vectors,).
        >>> vector1 = np.array([1, 2, 3])
        >>> vectors_all = [np.array([4, 5, 6]), np.array([7, 8, 9])]
        >>> VectorUtil.cosine_similarities(vector1, vectors_all)
        [0.97463185 0.95941195]
        """
        norm = np.linalg.norm(vector_1)
        all_norms = np.linalg.norm(vectors_all, axis=1)
        dot_products = np.dot(vectors_all, vector_1)
        similarities = dot_products / (norm * all_norms)
        return similarities

    @staticmethod
    def n_similarity(vector_list_1, vector_list_2):
        """
        Compute cosine similarity between two sets of vectors.
        :param vector_list_1: list of numpy vector
        :param vector_list_2: list of numpy vector
        :return: numpy.ndarray, Similarities between vector_list_1 and vector_list_2.
        >>> vector_list1 = [np.array([1, 2, 3]), np.array([4, 5, 6])]
        >>> vector_list2 = [np.array([7, 8, 9]), np.array([10, 11, 12])]
        >>> VectorUtil.n_similarity(vector_list1, vector_list2)
        0.9897287473881233
        """
        if not vector_list_1 or not vector_list_2:
            raise ZeroDivisionError("Indicates that at least one passed list is empty.")
        normalized_mean_1 = matutils.unitvec(array(vector_list_1).mean(axis=0))
        normalized_mean_2 = matutils.unitvec(array(vector_list_2).mean(axis=0))
        result = dot(normalized_mean_1, normalized_mean_2)
        return result

    @staticmethod
    def compute_idf_weight_dict(total_num, number_dict):
        """
        Calculate log(total_num+1/count+1) for each count in number_dict
        :param total_num: int
        :param number_dict: dict
        :return: dict
        >>> num_dict = {'key1':0.1, 'key2':0.5}
        >>> VectorUtil.compute_idf_weight_dict(2, num_dict)
        {'key1': 1.0033021088637848, 'key2': 0.6931471805599453}
        """
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
        for idx, weight in enumerate(a):
            result[index_2_key_map[idx]] = weight
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
