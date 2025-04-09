# util/db_util.py
import mysql.connector
from mysql.connector import Error

def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="ordermanagement",
            auth_plugin='mysql_native_password'
        )
        print("Database connection successful")
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None