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

class FitnessTrackerTestGetBMI(unittest.TestCase):
    def test_get_BMI(self):
        fitnessTracker = FitnessTracker(1.8, 70, 20, "male")
        self.assertEqual(fitnessTracker.get_BMI(), 21.604938271604937)

    def test_get_BMI_2(self):
        fitnessTracker = FitnessTracker(1.8, 50, 20, "male")
        self.assertEqual(fitnessTracker.get_BMI(), 15.432098765432098)

    def test_get_BMI_3(self):
        fitnessTracker = FitnessTracker(1.72, 53, 20, "male")
        self.assertEqual(fitnessTracker.get_BMI(), 17.915089237425637)

    def test_get_BMI_4(self):
        fitnessTracker = FitnessTracker(1.72, 60, 20, "male")
        self.assertEqual(fitnessTracker.get_BMI(), 20.281233098972418)

    def test_get_BMI_5(self):
        fitnessTracker = FitnessTracker(1.72, 65, 20, "male")
        self.assertEqual(fitnessTracker.get_BMI(), 21.971335857220122)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
