class AssessmentSystem:
    def __init__(self):
        self.students = {}

    def add_student(self, name, grade, major):
        if name not in self.students:
            self.students[name] = {
                "grade": grade,
                "major": major,
                "scores": {}
            }

    def add_course_score(self, student_name, course, score):
        if student_name in self.students:
            self.students[student_name]["scores"][course] = score

    def get_gpa(self, student_name):
        if student_name not in self.students:
            return None
        scores = [
            score for score in self.students[student_name]["scores"].values()
            if score is not None
        ]
        if not scores:
            return None
        return sum(scores) / len(scores)

    def get_all_students_with_fail_course(self):
        result = []
        for name, data in self.students.items():
            if any(score is not None and score < 60 for score in data["scores"].values()):
                result.append(name)
        return result

    def get_course_average(self, course):
        total = 0
        count = 0
        for data in self.students.values():
            score = data["scores"].get(course)
            if score is not None:
                total += score
                count += 1
        if count == 0:
            return None
        return total / count

    def get_top_student(self):
        best_name = None
        best_gpa = None
        for name in self.students:
            gpa = self.get_gpa(name)
            if gpa is None:
                continue
            if best_gpa is None or gpa > best_gpa:
                best_gpa = gpa
                best_name = name
        return best_name

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
