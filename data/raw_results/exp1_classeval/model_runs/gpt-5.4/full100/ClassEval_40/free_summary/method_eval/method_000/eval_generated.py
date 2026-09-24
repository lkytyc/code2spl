class FitnessTracker:
    def __init__(self, height, weight, age, sex):
        self.height = height
        self.weight = weight
        self.age = age
        self.sex = sex
        self.bmi_ranges = {
            "male": (20, 25),
            "female": (19, 24)
        }

    def get_BMI(self):
        return self.weight / (self.height ** 2)

    def condition_judge(self):
        bmi = self.get_BMI()
        sex_key = str(self.sex).lower()
        if sex_key not in self.bmi_ranges:
            raise ValueError("Sex must be 'male' or 'female'.")
        lower, upper = self.bmi_ranges[sex_key]
        if bmi > upper:
            return 1
        elif bmi < lower:
            return -1
        return 0

    def calculate_calorie_intake(self):
        sex_key = str(self.sex).lower()
        if sex_key == "male":
            bmr = 10 * self.weight + 6.25 * (self.height * 100) - 5 * self.age + 5
        elif sex_key == "female":
            bmr = 10 * self.weight + 6.25 * (self.height * 100) - 5 * self.age - 161
        else:
            raise ValueError("Sex must be 'male' or 'female'.")

        condition = self.condition_judge()
        if condition == 1:
            multiplier = 1.2
        elif condition == -1:
            multiplier = 1.6
        else:
            multiplier = 1.4

        return bmr * multiplier

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
