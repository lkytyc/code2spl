class MovieTicketDB:
    def __init__(self, db_name):
        import sqlite3
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY,
                movie_name TEXT,
                theater_name TEXT,
                seat_number TEXT,
                customer_name TEXT
            )
            """
        )
        self.connection.commit()

    def insert_ticket(self, movie_name, theater_name, seat_number, customer_name):
        self.cursor.execute(
            """
            INSERT INTO tickets (movie_name, theater_name, seat_number, customer_name)
            VALUES (?, ?, ?, ?)
            """,
            (movie_name, theater_name, seat_number, customer_name),
        )
        self.connection.commit()

    def search_tickets_by_customer(self, customer_name):
        self.cursor.execute(
            """
            SELECT * FROM tickets
            WHERE customer_name = ?
            """,
            (customer_name,),
        )
        tickets = self.cursor.fetchall()
        return tickets

    def delete_ticket(self, ticket_id):
        self.cursor.execute(
            """
            DELETE FROM tickets
            WHERE id = ?
            """,
            (ticket_id,),
        )
        self.connection.commit()

import unittest
import os

class MovieTicketDBTestInsertTicket(unittest.TestCase):
    def setUp(self):
        self.db_name = 'test_database.db'
        self.db = MovieTicketDB(self.db_name)

    def tearDown(self):
        self.db.connection.close()
        os.remove(self.db_name)

    def test_insert_ticket_1(self):
        self.db.insert_ticket('Avengers: Endgame', 'Cinema 1', 'A1', 'John Doe')
        tickets = self.db.search_tickets_by_customer('John Doe')
        self.assertEqual(len(tickets), 1)
        ticket = tickets[0]
        self.assertEqual(ticket[1], 'Avengers: Endgame')
        self.assertEqual(ticket[2], 'Cinema 1')
        self.assertEqual(ticket[3], 'A1')
        self.assertEqual(ticket[4], 'John Doe')

    def test_insert_ticket_2(self):
        self.db.insert_ticket('Avengers: Endgame', 'Cinema 1', 'A1', 'aaa')
        tickets = self.db.search_tickets_by_customer('aaa')
        self.assertEqual(len(tickets), 1)
        ticket = tickets[0]
        self.assertEqual(ticket[1], 'Avengers: Endgame')
        self.assertEqual(ticket[2], 'Cinema 1')
        self.assertEqual(ticket[3], 'A1')
        self.assertEqual(ticket[4], 'aaa')

    def test_insert_ticket_3(self):
        self.db.insert_ticket('Avengers: Endgame', 'Cinema 1', 'A1', 'bbb')
        tickets = self.db.search_tickets_by_customer('bbb')
        self.assertEqual(len(tickets), 1)
        ticket = tickets[0]
        self.assertEqual(ticket[1], 'Avengers: Endgame')
        self.assertEqual(ticket[2], 'Cinema 1')
        self.assertEqual(ticket[3], 'A1')
        self.assertEqual(ticket[4], 'bbb')

    def test_insert_ticket_4(self):
        self.db.insert_ticket('Avengers: Endgame', 'Cinema 1', 'A1', 'ccc')
        tickets = self.db.search_tickets_by_customer('ccc')
        self.assertEqual(len(tickets), 1)
        ticket = tickets[0]
        self.assertEqual(ticket[1], 'Avengers: Endgame')
        self.assertEqual(ticket[2], 'Cinema 1')
        self.assertEqual(ticket[3], 'A1')
        self.assertEqual(ticket[4], 'ccc')

    def test_insert_ticket_5(self):
        self.db.insert_ticket('Avengers: Endgame', 'Cinema 1', 'A1', 'ddd')
        tickets = self.db.search_tickets_by_customer('ddd')
        self.assertEqual(len(tickets), 1)
        ticket = tickets[0]
        self.assertEqual(ticket[1], 'Avengers: Endgame')
        self.assertEqual(ticket[2], 'Cinema 1')
        self.assertEqual(ticket[3], 'A1')
        self.assertEqual(ticket[4], 'ddd')

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
