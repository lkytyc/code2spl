class AssessmentSystem:
    def __init__(self):
        self.students = {}

    def add_student(self, name, grade, major):
        student_record = {
            'name': name,
            'grade': grade,
            'major': major,
            'courses': {}
        }
        self.students[name] = student_record

    def add_course_score(self, name, course, score):
        name_exists = name in self.students
        if name_exists:
            self.students[name]['courses'][course] = score

    def get_all_students_with_fail_course(self):
        students = []
        for name, student in self.students.items():
            for course, score in student['courses'].items():
                fail_condition = score < 60
                if fail_condition:
                    students.append(name)
                    break
        return students

    def get_course_average(self, course):
        total = 0
        count = 0
        for student in self.students.values():
            if course not in student['courses']:
                continue
            score = student['courses'][course]
            if score is not None:
                total += score
                count += 1
        if count > 0:
            return total / count
        return None

    def get_gpa(self, name):
        student_exists = name in self.students
        if student_exists and self.students[name]['courses']:
            grades_sum = sum(self.students[name]['courses'].values())
            course_count = len(self.students[name]['courses'])
            gpa = grades_sum / course_count
            return gpa
        return None

    def get_top_student(self):
        top_student = None
        top_gpa = 0
        for name, student in self.students.items():
            gpa = self.get_gpa(name)
            condition_result = gpa is not None and gpa > top_gpa
            if condition_result:
                top_gpa = gpa
                top_student = name
        return top_student

import unittest

class AssessmentSystemTestAddStudent(unittest.TestCase):
    def test_add_student(self):
        assessment_system = AssessmentSystem()
        assessment_system.add_student("Alice", 3, "Mathematics")
        self.assertEqual(assessment_system.students["Alice"],
                         {'name': 'Alice', 'grade': 3, 'major': 'Mathematics', 'courses': {}})

    def test_add_student_2(self):
        assessment_system = AssessmentSystem()
        assessment_system.add_student("Alice", 3, "Mathematics")
        assessment_system.add_student("Bob", 2, "Science")
        self.assertEqual(assessment_system.students,
                         {'Alice': {'name': 'Alice', 'grade': 3, 'major': 'Mathematics', 'courses': {}},
                          'Bob': {'name': 'Bob', 'grade': 2, 'major': 'Science', 'courses': {}}})

    def test_add_student_3(self):
        assessment_system = AssessmentSystem()
        assessment_system.add_student("Alice", 3, "Mathematics")
        assessment_system.add_student("Bob", 2, "Science")
        assessment_system.add_student("Charlie", 4, "Chemistry")
        self.assertEqual(assessment_system.students,
                         {'Alice': {'name': 'Alice', 'grade': 3, 'major': 'Mathematics', 'courses': {}},
                          'Bob': {'name': 'Bob', 'grade': 2, 'major': 'Science', 'courses': {}},
                          'Charlie': {'name': 'Charlie', 'grade': 4, 'major': 'Chemistry', 'courses': {}}})

    def test_add_student_4(self):
        assessment_system = AssessmentSystem()
        assessment_system.add_student("Alice", 3, "Mathematics")
        assessment_system.add_student("Bob", 2, "Science")
        assessment_system.add_student("Charlie", 4, "Chemistry")
        assessment_system.add_student("David", 1, "Physics")
        self.assertEqual(assessment_system.students,
                            {'Alice': {'name': 'Alice', 'grade': 3, 'major': 'Mathematics', 'courses': {}},
                                'Bob': {'name': 'Bob', 'grade': 2, 'major': 'Science', 'courses': {}},
                                'Charlie': {'name': 'Charlie', 'grade': 4, 'major': 'Chemistry', 'courses': {}},
                                'David': {'name': 'David', 'grade': 1, 'major': 'Physics', 'courses': {}}})

    def test_add_student_5(self):
        assessment_system = AssessmentSystem()
        assessment_system.add_student("Alice", 3, "Mathematics")
        assessment_system.add_student("Bob", 2, "Science")
        assessment_system.add_student("Charlie", 4, "Chemistry")
        assessment_system.add_student("David", 1, "Physics")
        assessment_system.add_student("Eve", 3, "Mathematics")
        self.assertEqual(assessment_system.students,
                            {'Alice': {'name': 'Alice', 'grade': 3, 'major': 'Mathematics', 'courses': {}},
                                'Bob': {'name': 'Bob', 'grade': 2, 'major': 'Science', 'courses': {}},
                                'Charlie': {'name': 'Charlie', 'grade': 4, 'major': 'Chemistry', 'courses': {}},
                                'David': {'name': 'David', 'grade': 1, 'major': 'Physics', 'courses': {}},
                                'Eve': {'name': 'Eve', 'grade': 3, 'major': 'Mathematics', 'courses': {}}})

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
