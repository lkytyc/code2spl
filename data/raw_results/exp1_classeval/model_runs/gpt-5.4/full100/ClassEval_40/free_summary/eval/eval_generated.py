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


class FitnessTrackerTestMain(unittest.TestCase):
    def test_main(self):
        fitnessTracker = FitnessTracker(1.8, 70, 20, "male")
        self.assertEqual(fitnessTracker.get_BMI(), 21.604938271604937)
        self.assertEqual(fitnessTracker.condition_judge(), 0)
        self.assertEqual(fitnessTracker.calculate_calorie_intake(), 862.75)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
