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

class FitnessTrackerTestCaculateCalorieIntake(unittest.TestCase):
    def test_calculate_calorie_intake(self):
        fitnessTracker = FitnessTracker(1.8, 70, 20, "female")
        self.assertEqual(fitnessTracker.calculate_calorie_intake(), 630.3499999999999)

    def test_calculate_calorie_intake_2(self):
        fitnessTracker = FitnessTracker(1.72, 80, 22, "female")
        self.assertEqual(fitnessTracker.calculate_calorie_intake(), 647.6999999999999)

    def test_calculate_calorie_intake_3(self):
        fitnessTracker = FitnessTracker(1.72, 53, 22, "male")
        self.assertEqual(fitnessTracker.calculate_calorie_intake(), 697.2)

    def test_calculate_calorie_intake_4(self):
        fitnessTracker = FitnessTracker(1.72, 60, 22, "male")
        self.assertEqual(fitnessTracker.calculate_calorie_intake(), 708.05)

    def test_calculate_calorie_intake_5(self):
        fitnessTracker = FitnessTracker(1.72, 75, 22, "male")
        self.assertEqual(fitnessTracker.calculate_calorie_intake(), 786.9)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
