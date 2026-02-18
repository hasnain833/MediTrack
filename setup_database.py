import mysql.connector
from mysql.connector import Error
import bcrypt
import getpass

def setup_database():
    root_password = getpass.getpass("Enter MySQL root password: ")

    try:
        root_conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password=root_password
        )
        root_cursor = root_conn.cursor()

        root_cursor.execute("CREATE DATABASE IF NOT EXISTS medical_store")
        print("Database 'medical_store' created.")

        root_cursor.execute("CREATE USER IF NOT EXISTS 'medical_user'@'localhost' IDENTIFIED BY 'your_password'")
        print("User 'medical_user' created.")

        root_cursor.execute("GRANT ALL PRIVILEGES ON medical_store.* TO 'medical_user'@'localhost'")
        root_cursor.execute("FLUSH PRIVILEGES")
        print("Permissions granted.")

        root_conn.commit()
        root_cursor.close()
        root_conn.close()

        from database.connection import Database
        db = Database()
        db.connect()

        users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            role ENUM('admin', 'user') DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """

        db.execute_query(users_table)
        print("Users table created.")

        admin_password = 'admin'
        hashed = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        insert_query = """
        INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE username=username
        """
        db.execute_query(insert_query, ('admin', hashed, 'admin'))
        db.connection.commit()
        print("Default admin user inserted.")

        db.disconnect()
        print("Database setup complete.")

    except Error as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    setup_database()
