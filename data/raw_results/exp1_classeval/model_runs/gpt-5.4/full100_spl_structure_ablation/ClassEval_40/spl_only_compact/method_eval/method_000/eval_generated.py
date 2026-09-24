class FitnessTracker:
    def __init__(self, height, weight, age, sex):
        self.height = height
        self.weight = weight
        self.age = age
        self.sex = sex
        self.BMI_std = [{"male": [20, 25]}, {"female": [19, 24]}]

    def calculate_calorie_intake(self):
        if self.sex == "male":
            BMR = 10 * self.weight + 6.25 * self.height - 5 * self.age + 5
        else:
            BMR = 10 * self.weight + 6.25 * self.height - 5 * self.age - 161

        if self.condition_judge() == 1:
            calorie_intake = BMR * 1.2
        elif self.condition_judge() == -1:
            calorie_intake = BMR * 1.6
        else:
            calorie_intake = BMR * 1.4

        return calorie_intake

    def condition_judge(self):
        BMI = self.get_BMI()
        sex_is_male = self.sex == "male"

        if sex_is_male:
            BMI_range = self.BMI_std[0]["male"]
        else:
            BMI_range = self.BMI_std[1]["female"]

        if BMI > BMI_range[1]:
            return 1
        if BMI < BMI_range[0]:
            return -1
        return 0

    def get_BMI(self):
        weight = self.weight
        height = self.height
        height_squared = height ** 2
        result = weight / height_squared
        return result

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
