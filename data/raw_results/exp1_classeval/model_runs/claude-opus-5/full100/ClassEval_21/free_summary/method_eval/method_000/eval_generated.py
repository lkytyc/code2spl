from datetime import datetime


class Classroom:
    def __init__(self, classroom_id):
        self.id = classroom_id
        self.courses = []

    def add_course(self, course):
        if course not in self.courses:
            self.courses.append(course)

    def remove_course(self, course):
        if course in self.courses:
            self.courses.remove(course)

    def is_free_at(self, check_time):
        check = datetime.strptime(check_time, "%H:%M")
        for course in self.courses:
            start = datetime.strptime(course["start_time"], "%H:%M")
            end = datetime.strptime(course["end_time"], "%H:%M")
            if start <= check <= end:
                return False
        return True

    def check_course_conflict(self, new_course):
        new_start = datetime.strptime(new_course["start_time"], "%H:%M")
        new_end = datetime.strptime(new_course["end_time"], "%H:%M")
        for course in self.courses:
            start = datetime.strptime(course["start_time"], "%H:%M")
            end = datetime.strptime(course["end_time"], "%H:%M")
            if start <= new_start <= end or start <= new_end <= end:
                return False
        return True

import unittest
from datetime import datetime

class ClassroomTestAddCourse(unittest.TestCase):
    def test_add_course_1(self):
        classroom = Classroom(1)
        course = {'name': 'math', 'start_time': '09:00', 'end_time': '10:00'}
        classroom.add_course(course)
        self.assertIn(course, classroom.courses)

    def test_add_course_2(self):
        classroom = Classroom(1)
        course = {'name': 'Chinese', 'start_time': '10:00', 'end_time': '11:00'}
        classroom.add_course(course)
        self.assertIn(course, classroom.courses)

    def test_add_course_3(self):
        classroom = Classroom(1)
        course = {'name': 'English', 'start_time': '11:00', 'end_time': '12:00'}
        classroom.add_course(course)
        self.assertIn(course, classroom.courses)

    def test_add_course_4(self):
        classroom = Classroom(1)
        course = {'name': 'Art', 'start_time': '14:00', 'end_time': '15:00'}
        classroom.add_course(course)
        self.assertIn(course, classroom.courses)

    def test_add_course_5(self):
        classroom = Classroom(1)
        course = {'name': 'P.E.', 'start_time': '15:00', 'end_time': '16:00'}
        classroom.add_course(course)
        self.assertIn(course, classroom.courses)

    def test_add_course_6(self):
        classroom = Classroom(1)
        course = {'name': 'math', 'start_time': '09:00', 'end_time': '10:00'}
        classroom.add_course(course)
        classroom.add_course(course)
        self.assertIn(course, classroom.courses)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
