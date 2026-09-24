class Classroom:
    def __init__(self, id):
        self.id = id
        self.courses = []

    @staticmethod
    def _parse_time(time_str):
        hours, minutes = map(int, time_str.split(':'))
        return hours * 60 + minutes

    def add_course(self, course):
        if course not in self.courses:
            self.courses.append(course)

    def remove_course(self, course):
        if course in self.courses:
            self.courses.remove(course)

    def is_free_at(self, check_time):
        t = self._parse_time(check_time)
        for course in self.courses:
            start = self._parse_time(course['start_time'])
            end = self._parse_time(course['end_time'])
            if start < t < end:
                return False
        return True

    def check_course_conflict(self, new_course):
        new_start = self._parse_time(new_course['start_time'])
        new_end = self._parse_time(new_course['end_time'])
        for course in self.courses:
            start = self._parse_time(course['start_time'])
            end = self._parse_time(course['end_time'])
            if (start < new_start and end > new_start) or (start < new_end and end > new_end):
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
