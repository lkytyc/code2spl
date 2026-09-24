class ClassRegistrationSystem:
    def __init__(self):
        self.students = []
        self.students_registration_classes = {}

    def register_student(self, student):
        for s in self.students:
            if s['name'] == student['name']:
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
        return [s['name'] for s in self.students if s['major'] == major]

    def get_all_major(self):
        return list(set(s['major'] for s in self.students))

    def get_most_popular_class_in_major(self, major):
        classes = []
        for s in self.students:
            if s['major'] == major:
                classes.extend(self.students_registration_classes.get(s['name'], []))
        if not classes:
            return None
        return max(set(classes), key=classes.count)

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
