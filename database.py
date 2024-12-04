import sqlite3

connection = sqlite3.connect('my-database.db')
cursor = connection.cursor()

create_table_users = '''
CREATE TABLE IF NOT EXISTS users (
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT NOT NULL,
email TEXT UNIQUE NOT NULL,
password TEXT NOT NULL
);'''

cursor.execute(create_table_users)
connection.commit
connection.close()

print('database is created successfully')