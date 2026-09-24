class ClassRegistrationSystem:
    def __init__(self):
        self.students = []
        self.students_registration_classes = {}

    def register_student(self, student):
        if student in self.students:
            return 0
        self.students.append(student)
        return 1

    def register_class(self, student_name, class_name):
        if student_name not in self.students_registration_classes:
            self.students_registration_classes[student_name] = []
        self.students_registration_classes[student_name].append(class_name)
        return self.students_registration_classes[student_name]

    def get_students_by_major(self, major):
        return [student["name"] for student in self.students if student["major"] == major]

    def get_all_major(self):
        seen = []
        for student in self.students:
            if student["major"] not in seen:
                seen.append(student["major"])
        return seen

    def get_most_popular_class_in_major(self, major):
        class_counts = {}
        for student in self.students:
            if student["major"] == major:
                for class_name in self.students_registration_classes.get(student["name"], []):
                    class_counts[class_name] = class_counts.get(class_name, 0) + 1
        return max(class_counts, key=class_counts.get)

import unittest

class ClassRegistrationSystemTestRegisterClass(unittest.TestCase):

    def setUp(self):
        self.registration_system = ClassRegistrationSystem()

    def test_register_class(self):
        self.assertEqual(self.registration_system.register_class(student_name="John", class_name="CS101"), ["CS101"])

    def test_register_class2(self):
        self.registration_system.register_class(student_name="John", class_name="CS101")
        self.registration_system.register_class(student_name="John", class_name="CS102")
        self.assertEqual(self.registration_system.register_class(student_name="John", class_name="CS103"), ["CS101", "CS102", "CS103"])

    def test_register_class3(self):
        self.registration_system.register_class(student_name="John", class_name="CS101")
        self.registration_system.register_class(student_name="Tom", class_name="CS102")
        self.assertEqual(self.registration_system.register_class(student_name="John", class_name="CS103"), ["CS101", "CS103"])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
