class FitnessTracker:
    def __init__(self, height, weight, age, sex):
        self.height = height
        self.weight = weight
        self.age = age
        self.sex = sex.lower()
        self.bmi_standards = {
            "male": [20, 25],
            "female": [19, 24]
        }

    def get_BMI(self):
        return self.weight / (self.height ** 2)

    def condition_judge(self):
        bmi = self.get_BMI()
        lower, upper = self.bmi_standards[self.sex]
        if bmi > upper:
            return 1
        elif bmi < lower:
            return -1
        else:
            return 0

    def calculate_calorie_intake(self):
        if self.sex == "male":
            bmr = 10 * self.weight + 6.25 * (self.height * 100) - 5 * self.age + 5
        else:
            bmr = 10 * self.weight + 6.25 * (self.height * 100) - 5 * self.age - 161

        condition = self.condition_judge()
        if condition == 1:
            factor = 1.2
        elif condition == -1:
            factor = 1.6
        else:
            factor = 1.4

        return bmr * factor

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
