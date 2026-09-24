import sqlite3

class StudentDatabase:
    def __init__(self, filename):
        self.filename = filename

    def create_student_table(self):
        conn = sqlite3.connect(self.filename)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER,
                gender TEXT,
                grade TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def insert_student(self, student_dict):
        conn = sqlite3.connect(self.filename)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO students (name, age, gender, grade)
            VALUES (?, ?, ?, ?)
        ''', (student_dict['name'], student_dict['age'], student_dict['gender'], student_dict['grade']))
        conn.commit()
        conn.close()

    def search_student_by_name(self, name):
        conn = sqlite3.connect(self.filename)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM students WHERE name = ?
        ''', (name,))
        rows = cursor.fetchall()
        conn.close()
        return rows

    def delete_student_by_name(self, name):
        conn = sqlite3.connect(self.filename)
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM students WHERE name = ?
        ''', (name,))
        conn.commit()
        conn.close()

import unittest

class StudentDatabaseProcessorTestInsertStudent(unittest.TestCase):
    def setUp(self):
        self.processor = StudentDatabaseProcessor("test_database.db")
        self.processor.create_student_table()

    def tearDown(self):
        conn = sqlite3.connect("test_database.db")
        conn.execute("DROP TABLE IF EXISTS students")
        conn.commit()
        conn.close()

    def test_insert_student_1(self):
        student_data = {
            'name': 'Alice',
            'age': 20,
            'gender': 'female',
            'grade': 90
        }
        self.processor.insert_student(student_data)

        conn = sqlite3.connect("test_database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE name=?", ('Alice',))
        result = cursor.fetchall()
        conn.close()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], 'Alice')

    def test_insert_student_2(self):
        student_data = {
            'name': 'aaa',
            'age': 20,
            'gender': 'female',
            'grade': 90
        }
        self.processor.insert_student(student_data)

        conn = sqlite3.connect("test_database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE name=?", ('aaa',))
        result = cursor.fetchall()
        conn.close()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], 'aaa')

    def test_insert_student_3(self):
        student_data = {
            'name': 'bbb',
            'age': 20,
            'gender': 'female',
            'grade': 90
        }
        self.processor.insert_student(student_data)

        conn = sqlite3.connect("test_database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE name=?", ('bbb',))
        result = cursor.fetchall()
        conn.close()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], 'bbb')

    def test_insert_student_4(self):
        student_data = {
            'name': 'ccc',
            'age': 20,
            'gender': 'female',
            'grade': 90
        }
        self.processor.insert_student(student_data)

        conn = sqlite3.connect("test_database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE name=?", ('ccc',))
        result = cursor.fetchall()
        conn.close()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], 'ccc')

    def test_insert_student_5(self):
        student_data = {
            'name': 'ddd',
            'age': 20,
            'gender': 'female',
            'grade': 90
        }
        self.processor.insert_student(student_data)

        conn = sqlite3.connect("test_database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE name=?", ('ddd',))
        result = cursor.fetchall()
        conn.close()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], 'ddd')

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
