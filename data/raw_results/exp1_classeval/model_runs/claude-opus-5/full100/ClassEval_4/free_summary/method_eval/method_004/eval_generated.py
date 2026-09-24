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
        if name not in self.students:
            return
        self.students[name]["courses"][course] = score

    def get_gpa(self, name):
        if name not in self.students:
            return None
        courses = self.students[name]["courses"]
        if not courses:
            return None
        scores = list(courses.values())
        return sum(scores) / len(scores)

    def get_all_students_with_fail_course(self):
        result = []
        for name, student in self.students.items():
            for score in student["courses"].values():
                if score < 60:
                    result.append(name)
                    break
        return result

    def get_course_average(self, course):
        valid_scores = []
        for student in self.students.values():
            if course in student["courses"]:
                score = student["courses"][course]
                if score is not None:
                    valid_scores.append(score)
        if not valid_scores:
            return None
        return sum(valid_scores) / len(valid_scores)

    def get_top_student(self):
        top_name = None
        top_gpa = 0
        for name in self.students:
            gpa = self.get_gpa(name)
            if gpa is not None and gpa > top_gpa:
                top_gpa = gpa
                top_name = name
        return top_name

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
