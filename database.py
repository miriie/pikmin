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

create_table_reviews = '''
CREATE TABLE IF NOT EXISTS reviews (
id INTERGER PRIMARY KEY AUTOINCREMENT
game TEXT UNIQUE NOT NULL
rating INTERGER NOT NULL
review TEXT
);'''

create_table_games = '''
CREATE TABLE IF NOT EXISTS games (
id INTERGER
name TEXT
title TEXT
description TEXT
rating INTERGER
image TEXT
);'''

cursor.execute(create_table_users)
connection.commit
connection.close()

print('database is created successfully')