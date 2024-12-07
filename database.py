import sqlite3

connection = sqlite3.connect('my-database.db')
cursor = connection.cursor()


def get_db_connection():
    """Connect to the SQLite database and return the connection object."""
    connection = sqlite3.connect('my-database.db')
    connection.row_factory = sqlite3.Row 
    return connection


def initialize_database():

    create_table_users = '''
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
    );'''

    create_table_reviews = '''
    CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game TEXT NOT NULL,
    rating INTERGER NOT NULL,
    review TEXT,
    username TEXT NOT NULL
    );'''

    create_table_games = '''
    CREATE TABLE IF NOT EXISTS games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    rating INTEGER NOT NULL,
    image TEXT NOT NULL
    );'''

    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute(create_table_users)
    cursor.execute(create_table_games)
    cursor.execute(create_table_reviews)

    games_data = [
        ("Pikmin 4", "insert description here", 4.5, "images/pikmin4.jpg"),
        ("The Legend of Zelda: Tears of the Kingdom", "insert description here", 4.3, "images/tears_of_the_kingdom.jpg"),
        ("Mario Party Superstars", "insert description here", 4.8, "images/mario_party_main.jpg")
    ]

    reviews_data = [
    ("Pikmin 4", 4, "Great game!", "user1"),
    ("Pikmin 4", 5, "Love it!", "user2")]

    cursor.executemany("INSERT INTO reviews (game, rating, review, username) VALUES (?, ?, ?, ?)", reviews_data)
    cursor.executemany("INSERT INTO games (title, description, rating, image) VALUES (?, ?, ?, ?)", games_data)

    connection.commit()
    connection.close()
    
    print('database is created successfully and data is inserted')

initialize_database()