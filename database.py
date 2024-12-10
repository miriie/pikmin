import sqlite3
from datetime import datetime

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
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        profile_picture TEXT
    );'''


    create_table_reviews = '''
    CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id INTEGER NOT NULL,
    rating INTEGER NOT NULL,
    review TEXT,
    title TEXT,
    date TEXT NOT NULL,
    username TEXT NOT NULL,
    FOREIGN KEY (game_id) REFERENCES games(id) ON DELETE CASCADE
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

    connection.commit()
    connection.close()
    
    print('database is created successfully and data is inserted')

initialize_database()

def add_game_entries():
    connection = sqlite3.connect('my-database.db')
    cursor = connection.cursor()

    # List of new games you want to add
    game_data = [
    ("Pikmin 4", "On a peculiar far away planet, a group of space travellers are stranded and awaiting rescue. Are you the right rescuer for the job? Pick up their SOS signals and explore an uncharted world inhabited by a curious crop of creatures. Meet the Pikmin and grow, gather and guide them to tackle tasks big and small. Explore, hunt for treasure in vast open areas, battle wild critters, solve puzzles and rescue the stranded travellers together.", 5.0, "images/pikmin4.jpg"),
    ("The Legend of Zelda: Tears of the Kingdom", "Explore the vast land - and skies - of Hyrule. In this sequel to the Legend of Zelda: Breath of the Wild game, you'll decide your own path through the sprawling landscapes of Hyrule and the mysterious islands floating in the vast skies above. Can you harness the power of Link's new abilities to fight back against the malevolent forces that threaten the kingdom?", 4.6, "images/tears_of_kingdom.jpg"),
    ("Mario Party Superstars", "Set out to become a superstar in Mario Party mode, a fun-packed board game where fortunes can change in the blink of an eye. Come out on top in free-for-all, four-player minigames, team up against the opposition in 2 vs. 2 and 1 vs. 3 minigames, or go head-to-head in Duel minigames.", 3.8, "images/mario_party_super.jpg"),
    ("Animal Crossing: New Horizons", "Escape to a deserted island and create your own paradise as you explore, create, and customise in the Animal Crossing: New Horizons game. Your island getaway has a wealth of natural resources that can be used to craft everything from tools to creature comforts. You can hunt down insects at the crack of dawn, decorate your paradise throughout the day, or enjoy sunset on the beach while fishing in the ocean.", 4.2, "images/new_horizons.jpg"),
    ("Pokémon Violet", "Journey together with friends as you explore freely in an open world inhabited by new Pokémon! Adventure awaits in the Paldea region, a sprawling land of vast open spaces dotted with lakes, towering peaks, wastelands and perilous mountain ranges. Beat the eight Gyms spread across the region - in any order - to prove your strength and aim for the Champion Rank!", 2.1, "images/pokemon_violet.jpg"),
    ("Kirby's Return to Dream Land Deluxe", "When Magolor's spaceship crashes onto Planet Popstar, it's Kirby and friends to the rescue! Help Magolor recover all of his ship's parts in an adventure that will take you all over Dream Land - from sunny scorching deserts to dark underwater depths. Jump into four-player fun or go at it solo in this deluxe version of the Wii platforming adventure, featuring new abilities and subgames", 3.5, "images/kirby_dream_land.jpg"),
    ("Splatoon 3", "Enter a sun-scorched desert inhabited by battle-hardened Inklings and Octolings. Ink, dive, swim, and splat your way to the top!", 4.1, "images/splatoon3.jpg"),
    ("Super Smash Bros. Ultimate", "A platform fighter for up to eight players featuring a massive roster of characters from Nintendo games and third-party franchises. Battle solo or with friends in chaotic, fast-paced matches across diverse stages, now with 74 fighters and more than 100 stages!", 4.5, "images/smash_bros_ultimate.jpg"),
    ("Cooking Mama: Cookstar", "Cook everything from classic Japanese recipes to today's most tasty comfort foods. Just follow Mama's instructions and create delicious and decadent treats that you can share with your friends. Chop, mince, slice, dice and roll with precision motion controls. With Mama's help, you will become the world's greatest culinary artist.", 0.9, "images/cooking_mama.jpg"),
    ("Nintendo Switch Sports", "Swing, kick and spike your way to victory! Grab a Joy-Con controller and use real-world movements to take part in a variety of sporting activities that'll get your body moving. Gather your friends and family to join in the fun on the same Nintendo Switch console, or seek out new competitors in online multiplayer!", 3.4, "images/switch_sports.jpg")
    ]
    # Insert new games only if they don't already exist
    for game in game_data:
        cursor.execute("SELECT COUNT(*) FROM games WHERE title = ?", (game[0],))
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO games (title, description, rating, image) VALUES (?, ?, ?, ?)", game)
            print(f"Game '{game[0]}' added to the database.")
        else:
            print(f"Game '{game[0]}' already exists. Skipping.")

    connection.commit()
    connection.close()
    print("New games have been added (if they weren't duplicates).")

def add_dummy_users():
    """Add dummy users to the database."""
    connection = get_db_connection()
    cursor = connection.cursor()

    users_data = [
        ("user1234", "password123", "images/clover.png"),
        ("zara fendy", "securepass", "images/clover.png"),
        ("user1", "mypassword", "images/clover.png"),
        ("user2", "letmein", "images/clover.png"),
        ("user3", "hunter2", "images/clover.png"),
        ("user4", "password4", "images/clover.png")
    ]

    # Insert users only if they don't already exist
    for user in users_data:
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", (user[0],))
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                "INSERT INTO users (username, password, profile_picture) VALUES (?, ?, ?)",
                user
            )
            print(f"User '{user[0]}' added to the database.")
        else:
            print(f"User '{user[0]}' already exists. Skipping.")

    connection.commit()
    connection.close()


def add_dummy_reviews():
    connection = get_db_connection()
    cursor = connection.cursor()

    reviews_data = [
        ('Pikmin 4', 5, 'Best game ever!', 'Epic Adventure', '2024-12-01', 'user1234'),
        ('Pikmin 4', 5, 'Simply amazing!', 'Masterpiece', '2024-12-02', 'zara fendy'),
        ("The Legend of Zelda: Tears of the Kingdom", 4, "Fantastic sequel!", "Challenging Fun", '2024-12-03', "user1"),
        ("Mario Party Superstars", 3, "Enjoyable with friends.", "Fun but Repetitive", '2024-12-03', "user2")
    ]

    for review in reviews_data:
        # Fetch game_id for the given game title
        cursor.execute("SELECT id FROM games WHERE title = ?", (review[0],))
        game_id_row = cursor.fetchone()

        # Fetch user_id for the given username
        cursor.execute("SELECT id FROM users WHERE username = ?", (review[5],))
        user_id_row = cursor.fetchone()

        if game_id_row and user_id_row:
            game_id = game_id_row[0]
            user_id = user_id_row[0]

            # Insert the review
            cursor.execute(
                "INSERT INTO reviews (game_id, rating, review, title, date, user_id) VALUES (?, ?, ?, ?, ?, ?)",
                (game_id, review[1], review[2], review[3], review[4], user_id)
            )
            print(f"Review for '{review[0]}' added by {review[5]}.")
        else:
            if not game_id_row:
                print(f"Game '{review[0]}' not found in the database. Skipping.")
            if not user_id_row:
                print(f"User '{review[5]}' not found in the database. Skipping.")

    connection.commit()
    connection.close()

if __name__ == "__main__":
    add_game_entries()
    add_dummy_users()
    add_dummy_reviews()

