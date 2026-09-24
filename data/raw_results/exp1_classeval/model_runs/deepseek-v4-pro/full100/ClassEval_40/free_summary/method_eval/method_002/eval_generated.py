class FitnessTracker:
    def __init__(self, height, weight, age, sex):
        self.height = height
        self.weight = weight
        self.age = age
        self.sex = sex.lower()

    def get_BMI(self):
        return self.weight / (self.height ** 2)

    def condition_judge(self):
        bmi = self.get_BMI()
        if self.sex == "male":
            if bmi > 25:
                return 1
            elif bmi < 20:
                return -1
            else:
                return 0
        elif self.sex == "female":
            if bmi > 24:
                return 1
            elif bmi < 19:
                return -1
            else:
                return 0
        else:
            raise ValueError("Sex must be 'male' or 'female'")

    def calculate_calorie_intake(self):
        if self.sex == "male":
            bmr = 88.362 + (13.397 * self.weight) + (4.799 * self.height * 100) - (5.677 * self.age)
        elif self.sex == "female":
            bmr = 447.593 + (9.247 * self.weight) + (3.098 * self.height * 100) - (4.330 * self.age)
        else:
            raise ValueError("Sex must be 'male' or 'female'")

        condition = self.condition_judge()
        if condition == 1:
            return bmr * 1.2
        elif condition == -1:
            return bmr * 1.6
        else:
            return bmr * 1.4

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
