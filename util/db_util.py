import sqlite3

def get_connection(db_name='order_management.db'):
    return sqlite3.connect(db_name)
