class ClassRegistrationSystem:
    def __init__(self):
        self.students = []
        self.registrations = {}

    def register_student(self, student):
        name = student.get('name')
        if any(s.get('name') == name for s in self.students):
            return 0
        self.students.append(student)
        return 1

    def register_class(self, student_name, class_name):
        if student_name not in self.registrations:
            self.registrations[student_name] = []
        self.registrations[student_name].append(class_name)
        return self.registrations[student_name]

    def get_students_by_major(self, major):
        return [s['name'] for s in self.students if s.get('major') == major]

    def get_all_major(self):
        return list({s['major'] for s in self.students if 'major' in s})

    def get_most_popular_class_in_major(self, major):
        from collections import Counter

        students = self.get_students_by_major(major)
        classes = []
        for student_name in students:
            classes.extend(self.registrations.get(student_name, []))

        if not classes:
            return None

        counter = Counter(classes)
        return max(counter, key=counter.get)

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
