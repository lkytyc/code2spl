class ClassRegistrationSystem:
    def __init__(self):
        self.students = []
        self.students_registration_classes = {}

    def get_all_major(self):
        major_list = []
        for student in self.students:
            major_not_seen = student["major"] not in major_list
            if major_not_seen:
                major_list.append(student["major"])
        return major_list

    def get_most_popular_class_in_major(self, major):
        class_list = []
        for student in self.students:
            if student["major"] == major:
                class_list.extend(self.students_registration_classes[student["name"]])
        most_popular_class = max(set(class_list), key=class_list.count)
        return most_popular_class

    def get_students_by_major(self, major):
        student_list = []
        for student in self.students:
            if student["major"] == major:
                student_list.append(student["name"])
        return student_list

    def register_class(self, student_name, class_name):
        student_exists = student_name in self.students_registration_classes
        if student_exists:
            self.students_registration_classes[student_name].append(class_name)
        else:
            self.students_registration_classes[student_name] = [class_name]
        return self.students_registration_classes[student_name]

    def register_student(self, student):
        is_duplicate = student in self.students
        if is_duplicate:
            return 0
        self.students.append(student)
        return 1

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
