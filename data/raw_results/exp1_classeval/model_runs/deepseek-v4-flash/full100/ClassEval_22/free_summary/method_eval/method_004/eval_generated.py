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

class ClassRegistrationSystemTestPopularClass(unittest.TestCase):

    def setUp(self):
        self.registration_system = ClassRegistrationSystem()

    def test_get_most_popular_class_in_major(self):
        self.registration_system.students = [{"name": "John", "major": "Computer Science"},
                                             {"name": "Bob", "major": "Computer Science"},
                                             {"name": "Alice", "major": "Computer Science"}]

        self.registration_system.students_registration_classes = {"John": ["Algorithms", "Data Structures"],
                                            "Bob": ["Operating Systems", "Data Structures", "Algorithms"],
                                            "Alice": ["Data Structures", "Operating Systems", "Calculus"]}

        cs_most_popular_class = self.registration_system.get_most_popular_class_in_major("Computer Science")

        self.assertEqual(cs_most_popular_class, "Data Structures")

    def test_get_most_popular_class_in_major2(self):
        self.registration_system.students = [{"name": "John", "major": "Computer Science"},
                                                {"name": "Bob", "major": "Computer Science"},
                                                {"name": "Alice", "major": "Computer Science"},
                                                {"name": "Tom", "major": "Mathematics"},
                                                {"name": "Jerry", "major": "Mathematics"}]

        self.registration_system.students_registration_classes = {"John": ["Algorithms", "Data Structures"],
                                                                  "Bob": ["Data Structures", "Algorithms",
                                                                          "Operating Systems"],
                                                                  "Alice": ["Data Structures", "Operating Systems",
                                                                            "Calculus"],
                                                                    "Tom": ["Calculus", "Linear Algebra"],
                                                                    "Jerry": ["Linear Algebra", "Statistics"]}

        cs_most_popular_class = self.registration_system.get_most_popular_class_in_major("Computer Science")
        math_most_popular_class = self.registration_system.get_most_popular_class_in_major("Mathematics")
        self.assertEqual(cs_most_popular_class, "Data Structures")
        self.assertEqual(math_most_popular_class, "Linear Algebra")

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
