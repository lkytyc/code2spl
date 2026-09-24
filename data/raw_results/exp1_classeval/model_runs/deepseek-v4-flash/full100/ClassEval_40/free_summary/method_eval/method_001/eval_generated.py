class FitnessTracker:
    def __init__(self, height, weight, age, sex):
        self.height = height
        self.weight = weight
        self.age = age
        self.sex = sex

    def get_BMI(self):
        return self.weight / ((self.height / 100) ** 2)

    def condition_judge(self):
        bmi = self.get_BMI()
        if self.sex.lower() == 'male':
            if bmi > 25:
                return 1
            elif bmi < 20:
                return -1
            else:
                return 0
        else:
            if bmi > 24:
                return 1
            elif bmi < 19:
                return -1
            else:
                return 0

    def calculate_calorie_intake(self):
        if self.sex.lower() == 'male':
            bmr = 66 + 13.7 * self.weight + 5 * self.height - 6.8 * self.age
        else:
            bmr = 655 + 9.6 * self.weight + 1.8 * self.height - 4.7 * self.age

        factors = {1: 1.2, -1: 1.6, 0: 1.4}
        return bmr * factors[self.condition_judge()]

import unittest

class FitnessTrackerTestConditionJudge(unittest.TestCase):
    def test_condition_judge(self):
        fitnessTracker = FitnessTracker(1.8, 45, 20, "female")
        self.assertEqual(fitnessTracker.condition_judge(), -1)

    def test_condition_judge_2(self):
        fitnessTracker = FitnessTracker(1.72, 80, 22, "female")
        self.assertEqual(fitnessTracker.condition_judge(), 1)

    def test_condition_judge_3(self):
        fitnessTracker = FitnessTracker(1.72, 53, 22, "male")
        self.assertEqual(fitnessTracker.condition_judge(), -1)

    def test_condition_judge_4(self):
        fitnessTracker = FitnessTracker(1.72, 60, 22, "male")
        self.assertEqual(fitnessTracker.condition_judge(), 0)

    def test_condition_judge_5(self):
        fitnessTracker = FitnessTracker(1.72, 75, 22, "male")
        self.assertEqual(fitnessTracker.condition_judge(), 1)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
