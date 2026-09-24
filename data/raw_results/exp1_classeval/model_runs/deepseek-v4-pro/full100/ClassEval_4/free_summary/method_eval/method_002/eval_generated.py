class AssessmentSystem:
    def __init__(self):
        self.students = {}

    def add_student(self, name, grade, major):
        self.students[name] = {
            'name': name,
            'grade': grade,
            'major': major,
            'courses': {}
        }

    def add_course_score(self, name, course, score):
        if name in self.students:
            self.students[name]['courses'][course] = score

    def calculate_gpa(self, name):
        if name not in self.students:
            return None
        scores = list(self.students[name]['courses'].values())
        if not scores:
            return None
        return sum(scores) / len(scores)

    def find_failing_students(self):
        failing = []
        for name, student in self.students.items():
            if any(score < 60 for score in student['courses'].values()):
                failing.append(name)
        return failing

    def average_score_for_course(self, course):
        scores = []
        for student in self.students.values():
            score = student['courses'].get(course)
            if score is not None:
                scores.append(score)
        if not scores:
            return None
        return sum(scores) / len(scores)

    def highest_gpa_student(self):
        best_student = None
        best_gpa = None
        for name in self.students:
            gpa = self.calculate_gpa(name)
            if gpa is not None:
                if best_gpa is None or gpa > best_gpa:
                    best_gpa = gpa
                    best_student = name
        return best_student

import unittest

class AssessmentSystemTestGetGPA(unittest.TestCase):
    def test_get_gpa_1(self):
        assessment_system = AssessmentSystem()
        assessment_system.students = {'Alice': {'name': 'Alice', 'grade': 3, 'major': 'Mathematics', 'courses': {'Mathematics': 90, 'Science': 80}}}
        self.assertEqual(assessment_system.get_gpa("Alice"), 85.0)


    # No such student
    def test_get_gpa_2(self):
        assessment_system = AssessmentSystem()
        self.assertEqual(assessment_system.get_gpa('Alice'), None)

    # student don't have any scores
    def test_get_gpa_3(self):
        assessment_system = AssessmentSystem()
        assessment_system.students = {'Alice': {'name': 'Alice', 'grade': 3, 'major': 'Mathematics', 'courses': {}}}
        self.assertEqual(assessment_system.get_gpa('Alice'), None)

    def test_get_gpa_4(self):
        assessment_system = AssessmentSystem()
        assessment_system.students = {'Alice': {'name': 'Alice', 'grade': 3, 'major': 'Mathematics', 'courses': {'Mathematics': 90}}}
        self.assertEqual(assessment_system.get_gpa('Bob'), None)

    def test_get_gpa_5(self):
        assessment_system = AssessmentSystem()
        assessment_system.students = {'Alice': {'name': 'Alice', 'grade': 3, 'major': 'Mathematics', 'courses': {'Mathematics': 90}}}
        self.assertEqual(assessment_system.get_gpa('Alice'), 90.0)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
