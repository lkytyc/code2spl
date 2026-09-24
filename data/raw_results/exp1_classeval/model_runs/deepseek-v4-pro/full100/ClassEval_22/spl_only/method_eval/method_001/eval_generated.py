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
        if student_name in self.students_registration_classes:
            self.students_registration_classes[student_name].append(class_name)
        else:
            self.students_registration_classes[student_name] = [class_name]
        return self.students_registration_classes[student_name]

    def get_students_by_major(self, major):
        student_list = []
        for student in self.students:
            if student["major"] == major:
                student_list.append(student["name"])
        return student_list

    def get_all_major(self):
        major_list = []
        for student in self.students:
            if student["major"] not in major_list:
                major_list.append(student["major"])
        return major_list

    def get_most_popular_class_in_major(self, major):
        class_list = []
        for student in self.students:
            if student["major"] == major:
                class_list.extend(self.students_registration_classes[student["name"]])
        unique_classes = set(class_list)
        most_popular_class = max(unique_classes, key=class_list.count)
        return most_popular_class

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
