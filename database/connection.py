import mysql.connector
from mysql.connector import Error
from config import DATABASE_CONFIG

class Database:
    def __init__(self):
        self.connection = None
        self.config = DATABASE_CONFIG

    def connect(self):
        try:
            self.connection = mysql.connector.connect(**self.config, autocommit=True)
            if self.connection.is_connected():
                return True
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return False

    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
        self.connection = None

    def test_connection(self):
        if self.connect():
            print("Database connection successful.")
            self.disconnect()
        else:
            raise Exception("Failed to connect to database.")

    def execute_query(self, query, params=None, dictionary=False):
        if not self.connection or not self.connection.is_connected():
            self.connect()
        cursor = self.connection.cursor(dictionary=dictionary)
        try:
            cursor.execute(query, params or ())
            return cursor
        except Error as e:
            print(f"Error executing query: {e}")
            raise

    def fetch_one(self, query, params=None, dictionary=True):
        cursor = self.execute_query(query, params, dictionary=dictionary)
        result = cursor.fetchone()
        cursor.close()
        return result

    def fetch_all(self, query, params=None, dictionary=True):
        cursor = self.execute_query(query, params, dictionary=dictionary)
        result = cursor.fetchall()
        cursor.close()
        return result