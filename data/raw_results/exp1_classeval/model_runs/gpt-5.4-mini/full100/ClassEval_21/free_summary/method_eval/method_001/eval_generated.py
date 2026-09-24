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

class ClassroomTestRemoveCourse(unittest.TestCase):
    def test_remove_course_1(self):
        classroom = Classroom(1)
        course = {'name': 'math', 'start_time': '09:00', 'end_time': '10:00'}
        classroom.add_course(course)
        classroom.remove_course(course)
        self.assertNotIn(course, classroom.courses)

    def test_remove_course_2(self):
        classroom = Classroom(1)
        course = {'name': 'Chinese', 'start_time': '10:00', 'end_time': '11:00'}
        classroom.add_course(course)
        classroom.remove_course(course)
        self.assertNotIn(course, classroom.courses)

    def test_remove_course_3(self):
        classroom = Classroom(1)
        course = {'name': 'English', 'start_time': '11:00', 'end_time': '12:00'}
        classroom.add_course(course)
        classroom.remove_course(course)
        self.assertNotIn(course, classroom.courses)

    def test_remove_course_4(self):
        classroom = Classroom(1)
        course = {'name': 'Art', 'start_time': '14:00', 'end_time': '15:00'}
        classroom.add_course(course)
        classroom.remove_course(course)
        self.assertNotIn(course, classroom.courses)

    def test_remove_course_5(self):
        classroom = Classroom(1)
        course = {'name': 'P.E.', 'start_time': '15:00', 'end_time': '16:00'}
        classroom.add_course(course)
        classroom.remove_course(course)
        self.assertNotIn(course, classroom.courses)

    def test_remove_course_6(self):
        classroom = Classroom(1)
        course = {'name': 'math', 'start_time': '09:00', 'end_time': '10:00'}
        classroom.remove_course(course)
        self.assertNotIn(course, classroom.courses)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
