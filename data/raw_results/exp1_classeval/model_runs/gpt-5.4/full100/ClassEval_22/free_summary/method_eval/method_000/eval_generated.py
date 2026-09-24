class ClassRegistrationSystem:
    def __init__(self):
        self.students = []
        self.students_registration_classes = {}

    def register_student(self, student):
        if student not in self.students:
            self.students.append(student)
            return 1
        return 0

    def register_class(self, student_name, class_name):
        if student_name in self.students_registration_classes:
            self.students_registration_classes[student_name].append(class_name)
        else:
            self.students_registration_classes[student_name] = [class_name]
        return self.students_registration_classes[student_name]

    def get_students_by_major(self, major):
        return [student["name"] for student in self.students if student["major"] == major]

    def get_all_major(self):
        majors = []
        for student in self.students:
            major = student["major"]
            if major not in majors:
                majors.append(major)
        return majors

    def get_most_popular_class_in_major(self, major):
        major_students = self.get_students_by_major(major)
        classes = []
        for student_name in major_students:
            classes.extend(self.students_registration_classes[student_name])

        class_counts = {}
        for class_name in classes:
            class_counts[class_name] = class_counts.get(class_name, 0) + 1

        most_popular_class = None
        max_count = -1
        for class_name, count in class_counts.items():
            if count > max_count:
                max_count = count
                most_popular_class = class_name

        return most_popular_class

import unittest

class ClassRegistrationSystemTestRegisterStudent(unittest.TestCase):

    def setUp(self):
        self.registration_system = ClassRegistrationSystem()

    def test_register_student(self):
        student1 = {"name": "John", "major": "Computer Science"}
        self.assertEqual(self.registration_system.register_student(student1), 1)

    def test_register_student2(self):
        student1 = {"name": "John", "major": "Computer Science"}
        self.registration_system.register_student(student1)
        self.assertEqual(self.registration_system.register_student(student1), 0)

    def test_register_student3(self):
        student1 = {"name": "John", "major": "Computer Science"}
        student2 = {"name": "Alice", "major": "Mathematics"}
        self.assertEqual(self.registration_system.register_student(student1), 1)
        self.assertEqual(self.registration_system.register_student(student2), 1)
        self.assertEqual(self.registration_system.register_student(student2), 0)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
