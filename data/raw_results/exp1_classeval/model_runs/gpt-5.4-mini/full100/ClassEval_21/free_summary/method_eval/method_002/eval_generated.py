from datetime import datetime


class Classroom:
    def __init__(self, id):
        self.id = id
        self.courses = []

    def add_course(self, course):
        if course not in self.courses:
            self.courses.append(course)

    def remove_course(self, course):
        if course in self.courses:
            self.courses.remove(course)

    def is_free_at(self, check_time):
        check_t = datetime.strptime(check_time, "%H:%M").time()
        for course in self.courses:
            start_time = datetime.strptime(course["start_time"], "%H:%M").time()
            end_time = datetime.strptime(course["end_time"], "%H:%M").time()
            if start_time <= check_t <= end_time:
                return False
        return True

    def check_course_conflict(self, new_course):
        new_start = datetime.strptime(new_course["start_time"], "%H:%M").time()
        new_end = datetime.strptime(new_course["end_time"], "%H:%M").time()

        for course in self.courses:
            start_time = datetime.strptime(course["start_time"], "%H:%M").time()
            end_time = datetime.strptime(course["end_time"], "%H:%M").time()

            if start_time <= new_start <= end_time or start_time <= new_end <= end_time:
                return False

        return True

import unittest
from datetime import datetime

class ClassroomTestIsFreeAt(unittest.TestCase):
    def test_is_free_at_1(self):
        classroom = Classroom(1)
        course = {'name': 'math', 'start_time': '09:00', 'end_time': '10:00'}
        classroom.add_course(course)
        check_time = '11:00'
        result = classroom.is_free_at(check_time)
        self.assertTrue(result)

    def test_is_free_at_2(self):
        classroom = Classroom(1)
        course = {'name': 'math', 'start_time': '09:00', 'end_time': '10:00'}
        classroom.add_course(course)
        check_time = '09:30'
        result = classroom.is_free_at(check_time)
        self.assertFalse(result)

    def test_is_free_at_3(self):
        classroom = Classroom(1)
        course = {'name': 'math', 'start_time': '09:00', 'end_time': '10:00'}
        classroom.add_course(course)
        check_time = '12:00'
        result = classroom.is_free_at(check_time)
        self.assertTrue(result)

    def test_is_free_at_4(self):
        classroom = Classroom(1)
        course = {'name': 'math', 'start_time': '09:00', 'end_time': '10:00'}
        classroom.add_course(course)
        check_time = '14:00'
        result = classroom.is_free_at(check_time)
        self.assertTrue(result)

    def test_is_free_at_5(self):
        classroom = Classroom(1)
        course = {'name': 'math', 'start_time': '09:00', 'end_time': '10:00'}
        classroom.add_course(course)
        check_time = '09:40'
        result = classroom.is_free_at(check_time)
        self.assertFalse(result)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
