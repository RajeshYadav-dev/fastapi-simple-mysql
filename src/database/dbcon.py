
import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

# Create 'user' table if not exists
try:
    mydb = get_db_connection()
    cursor = mydb.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100) NOT NULL,
        password VARCHAR(100) NOT NULL,
        email VARCHAR(50) NOT NULL
    )
    """)
    mydb.commit()
    print("Table 'user' created successfully.")
except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    cursor.close()
    mydb.close()    