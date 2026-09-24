class AssessmentSystem:
    def __init__(self):
        self.students = {}

    def add_student(self, name, grade, major):
        self.students[name] = {
            "name": name,
            "grade": grade,
            "major": major,
            "course_scores": {}
        }

    def add_course_score(self, name, course, score):
        if name in self.students:
            self.students[name]["course_scores"][course] = score

    def get_gpa(self, name):
        if name not in self.students:
            return None
        scores = [
            score for score in self.students[name]["course_scores"].values()
            if score is not None
        ]
        if not scores:
            return None
        return sum(scores) / len(scores)

    def get_all_students_with_fail_course(self):
        failed_students = []
        for name, record in self.students.items():
            for score in record["course_scores"].values():
                if score is not None and score < 60:
                    failed_students.append(name)
                    break
        return failed_students

    def get_course_average(self, course):
        scores = []
        for record in self.students.values():
            course_scores = record["course_scores"]
            if course in course_scores and course_scores[course] is not None:
                scores.append(course_scores[course])
        if not scores:
            return None
        return sum(scores) / len(scores)

    def get_top_student(self):
        top_student = None
        top_gpa = None
        for name in self.students:
            gpa = self.get_gpa(name)
            if gpa is None:
                continue
            if top_gpa is None or gpa > top_gpa:
                top_gpa = gpa
                top_student = name
        return top_student

import unittest

class AssessmentSystemTestGetCourseAverage(unittest.TestCase):

    def test_get_course_average_1(self):
        assessment_system = AssessmentSystem()
        assessment_system.students = {'Alice': {'name': 'Alice', 'grade': 3, 'major': 'Mathematics', 'courses': {'Mathematics': 90, 'Science': 80}},
                                'Bob': {'name': 'Bob', 'grade': 4, 'major': 'Physics', 'courses': {'Physics': 90}},
                                'Charlie': {'name': 'Charlie', 'grade': 2, 'major': 'Chemistry', 'courses': {'Chemistry': 70,'Physics': 80}}
                                           }
        self.assertEqual(assessment_system.get_course_average("Physics"), 85.0)

    def test_get_course_average_2(self):
        assessment_system = AssessmentSystem()
        assessment_system.students = {'Alice': {'name': 'Alice', 'grade': 3, 'major': 'Mathematics',
                                                'courses': {'Mathematics': 90, 'Science': 80}},
                                      'Bob': {'name': 'Bob', 'grade': 4, 'major': 'Physics',
                                              'courses': {'Physics': 85}},
                                      'Charlie': {'name': 'Charlie', 'grade': 2, 'major': 'Chemistry',
                                                  'courses': {'Chemistry': 70,'Physics': None }}
                                      }
        self.assertEqual(assessment_system.get_course_average('Physics'), 85)

    def test_get_course_average_3(self):
        assessment_system = AssessmentSystem()
        assessment_system.students = {'Alice': {'name': 'Alice', 'grade': 3, 'major': 'Mathematics',
                                                'courses': {'Mathematics': 90, 'Science': 80}},
                                      'Bob': {'name': 'Bob', 'grade': 4, 'major': 'Physics',
                                              'courses': {'Physics': 85}},
                                      'Charlie': {'name': 'Charlie', 'grade': 2, 'major': 'Chemistry',
                                                  'courses': {'Chemistry': 70, 'Physics': 80}}
                                      }
        self.assertEqual(assessment_system.get_course_average('Computer'), None)

    def test_get_course_average_4(self):
        assessment_system = AssessmentSystem()
        assessment_system.students = {}
        self.assertEqual(assessment_system.get_course_average('Computer'), None)

    def test_get_course_average_5(self):
        assessment_system = AssessmentSystem()
        assessment_system.students = {'Alice': {'name': 'Alice', 'grade': 3, 'major': 'Mathematics',
                                                'courses': {'Mathematics': 90, 'Science': 80}},
                                      'Bob': {'name': 'Bob', 'grade': 4, 'major': 'Physics',
                                              'courses': {'Physics': 85}},
                                      'Charlie': {'name': 'Charlie', 'grade': 2, 'major': 'Chemistry',
                                                  'courses': {'Chemistry': 70, 'Physics': 80}}
                                      }
        self.assertEqual(assessment_system.get_course_average('Mathematics'), 90)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
