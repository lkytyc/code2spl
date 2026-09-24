class StudentDatabaseProcessor:
    def __init__(self, database_name: object):
        self.database_name = database_name

    def create_student_table(self):
        import sqlite3
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        create_table_query = (
            "CREATE TABLE IF NOT EXISTS students ("
            "id INTEGER PRIMARY KEY, "
            "name TEXT, "
            "age INTEGER, "
            "gender TEXT, "
            "grade INTEGER)"
        )
        cursor.execute(create_table_query)
        conn.commit()
        conn.close()

    def delete_student_by_name(self, name: str):
        import sqlite3
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        delete_query = "DELETE FROM students WHERE name = ?"
        delete_execution = cursor.execute(delete_query, (name,))
        commit_result = conn.commit()
        close_result = conn.close()
        return close_result

    def insert_student(self, student_data: dict):
        import sqlite3
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        insert_query = "INSERT INTO students (name, age, gender, grade) VALUES (?, ?, ?, ?)"
        insert_result = cursor.execute(
            insert_query,
            (
                student_data["name"],
                student_data["age"],
                student_data["gender"],
                student_data["grade"],
            ),
        )
        commit_result = conn.commit()
        close_result = conn.close()
        return close_result

    def search_student_by_name(self, name: str) -> list:
        import sqlite3
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        select_query = "SELECT * FROM students WHERE name = ?"
        query_execution = cursor.execute(select_query, (name,))
        result = cursor.fetchall()
        conn.close()
        return result

import unittest

class StudentDatabaseProcessorTestDeleteStudentByName(unittest.TestCase):
    def setUp(self):
        self.processor = StudentDatabaseProcessor("test_database.db")
        self.processor.create_student_table()

    def tearDown(self):
        conn = sqlite3.connect("test_database.db")
        conn.execute("DROP TABLE IF EXISTS students")
        conn.commit()
        conn.close()

    def test_delete_student_by_name_1(self):
        student_data = {
            'name': 'Charlie',
            'age': 18,
            'gender': 'male',
            'grade': 95
        }
        self.processor.insert_student(student_data)

        self.processor.delete_student_by_name('Charlie')

        conn = sqlite3.connect("test_database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE name=?", ('Charlie',))
        result = cursor.fetchall()
        conn.close()

        self.assertEqual(len(result), 0)

    def test_delete_student_by_name_2(self):
        student_data = {
            'name': 'aaa',
            'age': 18,
            'gender': 'male',
            'grade': 95
        }
        self.processor.insert_student(student_data)

        self.processor.delete_student_by_name('aaa')

        conn = sqlite3.connect("test_database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE name=?", ('aaa',))
        result = cursor.fetchall()
        conn.close()

        self.assertEqual(len(result), 0)

    def test_delete_student_by_name_3(self):
        student_data = {
            'name': 'bbb',
            'age': 18,
            'gender': 'male',
            'grade': 95
        }
        self.processor.insert_student(student_data)

        self.processor.delete_student_by_name('bbb')

        conn = sqlite3.connect("test_database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE name=?", ('bbb',))
        result = cursor.fetchall()
        conn.close()

        self.assertEqual(len(result), 0)

    def test_delete_student_by_name_4(self):
        student_data = {
            'name': 'ccc',
            'age': 18,
            'gender': 'male',
            'grade': 95
        }
        self.processor.insert_student(student_data)

        self.processor.delete_student_by_name('ccc')

        conn = sqlite3.connect("test_database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE name=?", ('ccc',))
        result = cursor.fetchall()
        conn.close()

        self.assertEqual(len(result), 0)

    def test_delete_student_by_name_5(self):
        student_data = {
            'name': 'ddd',
            'age': 18,
            'gender': 'male',
            'grade': 95
        }
        self.processor.insert_student(student_data)

        self.processor.delete_student_by_name('ddd')

        conn = sqlite3.connect("test_database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE name=?", ('ddd',))
        result = cursor.fetchall()
        conn.close()

        self.assertEqual(len(result), 0)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
