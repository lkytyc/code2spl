class StudentDatabaseProcessor:
    def __init__(self, database_name):
        self.database_name = database_name

    def create_student_table(self):
        import sqlite3

        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        create_table_query = """
            CREATE TABLE IF NOT EXISTS students (
                name TEXT,
                age INTEGER,
                gender TEXT,
                grade TEXT
            )
        """
        cursor.execute(create_table_query)
        conn.commit()
        conn.close()

    def delete_student_by_name(self, name):
        import sqlite3

        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        delete_query = "DELETE FROM students WHERE name = ?"
        deleted_row_operation = cursor.execute(delete_query, (name,))
        commit_result = conn.commit()
        close_result = conn.close()

    def insert_student(self, student_data):
        import sqlite3

        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        insert_query = """
            INSERT INTO students (name, age, gender, grade)
            VALUES (?, ?, ?, ?)
        """
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

    def search_student_by_name(self, name):
        import sqlite3

        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        select_query = "SELECT * FROM students WHERE name = ?"
        query_execution = cursor.execute(select_query, (name,))
        result = cursor.fetchall()
        conn.close()
        return result

import unittest

class StudentDatabaseProcessorTestSearchStudentByName(unittest.TestCase):
    def setUp(self):
        self.processor = StudentDatabaseProcessor("test_database.db")
        self.processor.create_student_table()

    def tearDown(self):
        conn = sqlite3.connect("test_database.db")
        conn.execute("DROP TABLE IF EXISTS students")
        conn.commit()
        conn.close()

    def test_search_student_by_name_1(self):
        student_data = {
            'name': 'Bob',
            'age': 19,
            'gender': 'male',
            'grade': 85
        }
        self.processor.insert_student(student_data)

        result = self.processor.search_student_by_name('Bob')

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], 'Bob')

    def test_search_student_by_name_2(self):
        student_data = {
            'name': 'aaa',
            'age': 19,
            'gender': 'male',
            'grade': 85
        }
        self.processor.insert_student(student_data)

        result = self.processor.search_student_by_name('aaa')

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], 'aaa')

    def test_search_student_by_name_3(self):
        student_data = {
            'name': 'bbb',
            'age': 19,
            'gender': 'male',
            'grade': 85
        }
        self.processor.insert_student(student_data)

        result = self.processor.search_student_by_name('bbb')

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], 'bbb')

    def test_search_student_by_name_4(self):
        student_data = {
            'name': 'ccc',
            'age': 19,
            'gender': 'male',
            'grade': 85
        }
        self.processor.insert_student(student_data)

        result = self.processor.search_student_by_name('ccc')

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], 'ccc')

    def test_search_student_by_name_5(self):
        student_data = {
            'name': 'ddd',
            'age': 19,
            'gender': 'male',
            'grade': 85
        }
        self.processor.insert_student(student_data)

        result = self.processor.search_student_by_name('ddd')

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], 'ddd')

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
