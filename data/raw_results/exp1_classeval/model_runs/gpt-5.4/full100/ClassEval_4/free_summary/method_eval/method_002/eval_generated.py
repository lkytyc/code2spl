class AssessmentSystem:
    def __init__(self):
        self.students = {}

    def add_student(self, name, grade, major):
        self.students[name] = {
            "name": name,
            "grade": grade,
            "major": major,
            "courses": {}
        }

    def add_course_score(self, name, course, score):
        if name in self.students:
            self.students[name]["courses"][course] = score

    def get_gpa(self, name):
        if name not in self.students:
            return None
        courses = self.students[name]["courses"]
        if not courses:
            return None
        scores = list(courses.values())
        if not scores:
            return None
        return sum(scores) / len(scores)

    def get_all_students_with_fail_course(self):
        failed_students = []
        for name, student in self.students.items():
            for score in student["courses"].values():
                if score < 60:
                    failed_students.append(name)
                    break
        return failed_students

    def get_course_average(self, course):
        scores = []
        for student in self.students.values():
            if course in student["courses"]:
                score = student["courses"][course]
                if score is not None:
                    scores.append(score)
        if not scores:
            return None
        return sum(scores) / len(scores)

    def get_top_student(self):
        top_name = None
        top_gpa = None
        for name in self.students:
            gpa = self.get_gpa(name)
            if gpa is None:
                continue
            if top_gpa is None or gpa > top_gpa:
                top_gpa = gpa
                top_name = name
        return top_name

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
