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

class AssessmentSystemTestGetAllStudentsWithFailCourse(unittest.TestCase):
    def test_get_all_students_with_fail_course(self):
        assessment_system = AssessmentSystem()
        assessment_system.students = {'Alice': {'name': 'Alice', 'grade': 3, 'major': 'Mathematics', 'courses': {'Mathematics': 90, 'Science': 80}},
                                'Bob': {'name': 'Bob', 'grade': 4, 'major': 'Physics', 'courses': {'Physics': 50}},
                                'Charlie': {'name': 'Charlie', 'grade': 2, 'major': 'Chemistry', 'courses': {'Chemistry': 70}},
                                'David': {'name': 'David', 'grade': 1, 'major': 'Physics', 'courses': {'Physics': 60}},
                                'Eve': {'name': 'Eve', 'grade': 3, 'major': 'Mathematics', 'courses': {'Mathematics': 90}}}
        self.assertEqual(assessment_system.get_all_students_with_fail_course(), ['Bob'])

    def test_get_all_students_with_fail_course_2(self):
        assessment_system = AssessmentSystem()
        assessment_system.students = {'Alice': {'name': 'Alice', 'grade': 3, 'major': 'Mathematics', 'courses': {'Mathematics': 90, 'Science': 80}},
                                'Bob': {'name': 'Bob', 'grade': 4, 'major': 'Physics', 'courses': {'Physics': 70}},
                                'Charlie': {'name': 'Charlie', 'grade': 2, 'major': 'Chemistry', 'courses': {'Chemistry': 70}},
                                'David': {'name': 'David', 'grade': 1, 'major': 'Physics', 'courses': {'Physics': 70}},
                                'Eve': {'name': 'Eve', 'grade': 3, 'major': 'Mathematics', 'courses': {'Mathematics': 90}}}
        self.assertEqual(assessment_system.get_all_students_with_fail_course(), [])

    def test_get_all_students_with_fail_course_3(self):
        assessment_system = AssessmentSystem()
        assessment_system.students = {}
        self.assertEqual(assessment_system.get_all_students_with_fail_course(), [])

    def test_get_all_students_with_fail_course_4(self):
        assessment_system = AssessmentSystem()
        assessment_system.students = {'Alice': {'name': 'Alice', 'grade': 3, 'major': 'Mathematics', 'courses': {}}}
        self.assertEqual(assessment_system.get_all_students_with_fail_course(), [])

    def test_get_all_students_with_fail_course_5(self):
        assessment_system = AssessmentSystem()
        assessment_system.students = {'Alice': {'name': 'Alice', 'grade': 3, 'major': 'Mathematics', 'courses': {'Mathematics': 90, 'Science': 50}},
                                'Bob': {'name': 'Bob', 'grade': 4, 'major': 'Physics', 'courses': {'Physics': 50}},
                                'Charlie': {'name': 'Charlie', 'grade': 2, 'major': 'Chemistry', 'courses': {'Chemistry': 70}},
                                'David': {'name': 'David', 'grade': 1, 'major': 'Physics', 'courses': {'Physics': 70}},
                                'Eve': {'name': 'Eve', 'grade': 3, 'major': 'Mathematics', 'courses': {'Mathematics': 90}}}
        self.assertEqual(assessment_system.get_all_students_with_fail_course(), ['Alice', 'Bob'])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
