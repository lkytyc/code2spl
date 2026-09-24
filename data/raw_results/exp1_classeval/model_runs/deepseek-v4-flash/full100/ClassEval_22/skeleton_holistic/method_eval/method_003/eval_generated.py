class ClassRegistrationSystem:
    def __init__(self):
        self.students = []
        self.students_registration_classes = {}

    def register_student(self, student):
        for existing_student in self.students:
            if existing_student["name"] == student["name"]:
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
        majors = []
        for student in self.students:
            if student["major"] not in majors:
                majors.append(student["major"])
        return majors

    def get_most_popular_class_in_major(self, major):
        class_counts = {}
        most_popular_class = None
        max_count = 0

        for student in self.students:
            if student["major"] == major:
                for class_name in self.students_registration_classes.get(student["name"], []):
                    class_counts[class_name] = class_counts.get(class_name, 0) + 1
                    count = class_counts[class_name]
                    if count > max_count:
                        max_count = count
                        most_popular_class = class_name

        return most_popular_class

import unittest

class ClassRegistrationSystemTestGetMajor(unittest.TestCase):

    def setUp(self):
        self.registration_system = ClassRegistrationSystem()

    def test_get_all_major(self):
        self.registration_system.students = [{"name": "John", "major": "Computer Science"},
                                             {"name": "Bob", "major": "Computer Science"}]

        majors = self.registration_system.get_all_major()

        self.assertEqual(majors, ["Computer Science"])

    def test_get_all_major2(self):
        self.registration_system.students = [{"name": "John", "major": "Computer Science"},
                                             {"name": "Bob", "major": "Computer Science"},
                                             {"name": "Alice", "major": "Mathematics"}]

        majors = self.registration_system.get_all_major()

        self.assertEqual(majors, ["Computer Science", "Mathematics"])

    def test_get_all_major3(self):
        self.registration_system.students = [{"name": "John", "major": "Computer Science"},
                                             {"name": "Bob", "major": "Computer Science"},
                                             {"name": "Alice", "major": "Mathematics"},
                                             {"name": "Tom", "major": "Mathematics"},
                                             {"name": "Jerry", "major": "Physics"}]

        majors = self.registration_system.get_all_major()

        self.assertEqual(majors, ["Computer Science", "Mathematics", "Physics"])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
