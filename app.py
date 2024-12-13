import random
from flask import Flask, render_template, redirect, url_for, session, request
from datetime import datetime
import pytz
import sqlite3
import string
import unicodedata

app = Flask(__name__)
app.secret_key = 'your_secret_key'

#
# trang stuff
#

def get_db_connection():
    connection = sqlite3.connect('my-database.db')
    connection.row_factory = sqlite3.Row  # Use Row to get dictionary-like access
    return connection

@app.route('/game/<int:game_id>', methods=['GET', 'POST'])
def game_page(game_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    # calculate avg rating from reviews
    cursor.execute("SELECT AVG(rating) FROM reviews WHERE game_id = ?", (game_id,))
    average_rating = cursor.fetchone()[0]
    cursor.execute("UPDATE games SET rating = ? WHERE id = ?", (average_rating, game_id))

    if request.method == 'POST':
        # Handle the form submission for adding a review
        username = session['username']
        rating = int(request.form['rating'])
        review_title = request.form['review_title']
        review_text = request.form['review']
        profile_picture = session['profile_picture']
        
        # Get the current time in Sydney, Australia
        sydney_tz = pytz.timezone('Australia/Sydney')
        current_date = datetime.now(sydney_tz).strftime('%Y-%m-%d')

        # Insert the new review into the database
        insert_review_query = '''
        INSERT INTO reviews (game_id, rating, review, title, date, profile_picture, username)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        '''

        # update new avg rating
        cursor.execute("UPDATE games SET rating = ? WHERE id = ?", (average_rating, game_id))

        connection.execute(insert_review_query, (game_id, rating, review_text, review_title, current_date, profile_picture, username))
        connection.commit()
        return redirect(url_for('game_page', game_id=game_id))
    
    # Fetch game information based on the game ID
    query_game = "SELECT title, description, tags, rating, image FROM games WHERE id = ?"
    game = connection.execute(query_game, (game_id,)).fetchone()

    # Fetch reviews for the game
    query_reviews = '''
    SELECT username, profile_picture, title AS review_title, 
           review, rating, date
    FROM reviews
    WHERE game_id = ?
    '''
    reviews = connection.execute(query_reviews, (game_id,)).fetchall()

    connection.close()

    if game:
        # sorting tags
        tags = sorted(game['tags'].split(','))
        # display game data
        game_data = {
            "title": game['title'],
            "description": game['description'],
            "tags": tags,
            "rating": game['rating'] if reviews else "N/A",
            "image": game['image'],  
            "reviews": [
                {
                    "username": r['username'],
                    "profile_picture": r['profile_picture'],
                    "review_title": r['review_title'],
                    "review": r['review'],
                    "rating": r['rating'],
                    "date": r['date']
                } for r in reviews
            ]
        }

        return render_template('gamepage.html', game=game_data, tags=tags)
    else:
        return "Page not found", 404


@app.route('/')
def homepage():
    connection = get_db_connection()

    popular_games_query = '''
    SELECT games.*, COUNT(reviews.id) AS review_count
    FROM games
    LEFT JOIN reviews ON reviews.game_id = games.id  -- Correct the join condition here
    GROUP BY games.id
    ORDER BY review_count DESC
    LIMIT 3;
    '''
    popular_games = connection.execute(popular_games_query).fetchall()

    # Fetch random games for Explore section
    all_games = connection.execute("SELECT * FROM games").fetchall()
    explore_games = random.sample(all_games, min(len(all_games), 3))  # Pick 3 random games

    connection.close()

    return render_template("homepage.html", popular_games=popular_games, explore_games=explore_games)

# fendy editing this now

@app.route('/search', methods=['GET', 'POST'])
def search():
    connection = get_db_connection()
    cursor = connection.cursor()

    # Fetch games ordered alphabetically by title
    cursor.execute("SELECT id, title, description, rating, image FROM games ORDER BY title ASC")
    games = cursor.fetchall()
    tags = sorted([
            "Multi-player", 
            "Single-player", 
            "Strategy", 
            "Platformer", 
            "Adventure", 
            "Open-world", 
            "Combat", 
            "Competitive",
            "Mini-games",
            "Casual",
            "Life-simulator",
            "Cooking",
            "Sports"
        ])
    
    selected_tags = request.args.getlist('tags') or request.form.getlist('tags') # get selected tags from game page buttons or from search filter
    searched_name = request.form.get('search-bar', '') if request.method == 'POST' else '' 
    
    if searched_name:
        banned_punctuation = string.punctuation + ":'" # get rid of inconsistencies when user searches up a term
        searched_name = unicodedata.normalize('NFD', searched_name).encode('ascii', 'ignore').decode('utf-8') # bruh i had to add this specific case just for Pokémon Violet :(
        searched_name = searched_name.replace(" ", "").translate(str.maketrans("", "", banned_punctuation)).lower()
        searched_name = f"%{searched_name}%" # if the searched name is partially typed up, and is in one of the databases' game titles, the search works
    
        # haha what a hot mess (again homogenising game titles and getting rid of grammar so it's easier to match)
        cursor.execute("""SELECT id, title, description, rating, image 
        FROM games WHERE LOWER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE 
            (title, 
            ' ', ''),
            ',', ''), 
            '.', ''),
            ':', ''),
            "'", ''),
            'é', 'e')
            ) LIKE ?""",
            (searched_name,))
        existing_game = cursor.fetchall()
        
        # check if game name searched exists in the database
        if existing_game:
            games = existing_game
            searched_name = request.form["search-bar"]
            return render_template("search.html", games=games, tags=tags, message= f'Showing results for "{searched_name}":')
        else:
            searched_name = request.form["search-bar"]
            return render_template("search.html", games="", tags=tags, message= f'Error: No games found for "{searched_name}":')

    # filter games that fit selected tags
    elif selected_tags:
        tags_conditions = " AND ".join([f"tags LIKE '%{tag}%'" for tag in selected_tags])
        cursor.execute(f"""SELECT id, title, description, rating, image FROM games WHERE {tags_conditions}""")
        existing_game = cursor.fetchall()
        if existing_game:
            games = existing_game
            return render_template("search.html", games=games, tags=tags, message= f'Showing results for tags: "{", ".join(selected_tags)}":')
        else:
            return render_template("search.html", games="", tags=tags, message= f'Error: No games found for tags: "{", ".join(selected_tags)}":')
    
    connection.close()
    return render_template('search.html', games=games, tags=tags, message= f'All Games:')

#
# end trang stuff
#

#
# fendy stuff
#

@app.route("/login", methods= ["GET", "POST"])
def login():
    connection = get_db_connection()
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        cursor = connection.cursor()
        cursor.execute("SELECT username, password, profile_picture FROM users WHERE username = ?", (username,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            db_password = existing_user[1]
            if password == db_password:
                session["username"] = username
                session["profile_picture"] = existing_user[2]
                session["logged_in"] = True
                return redirect(url_for('homepage'))
            else:
                return render_template("login.html", message="Error: Wrong username or password")
        else:
            return render_template("login.html", message= "Error: User does not exist")
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('homepage'))

@app.route("/register", methods= ["GET", "POST"])
def register():
    connection = get_db_connection()
    
    images = [
        "clover.png", 
        "redpik.png", 
        "bluepik.png", 
        "yellowpik.png",
        "purplepik.png",
        "whitepik.png",
        "rockpik.png",
        "icepik.png",
        "wingpik.png",
        "glowpik.png"
    ]

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        re_password = request.form["re-password"]
        profile_picture = "images/" + request.form["pikpic"]

        cursor = connection.cursor()
        cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        existing_user = cursor.fetchone()
        
        # user taken
        if existing_user:
            return render_template("register.html", message= "Error: Username already taken", images=images)

        # password min length
        if len(password) < 8:
            return render_template("register.html", message= "Error: Password must be at least 8 characters long", images=images)

        # passwords match
        if password != re_password:
            return render_template("register.html", message= "Error: Passwords do not match", images=images)
        
        # successful registration 
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users(username, password, profile_picture) VALUES (?, ?, ?)", (username, password, profile_picture))
        connection.commit()
        session["username"] = username
        session["profile_picture"] = profile_picture
        session["logged_in"] = True
        return redirect(url_for('homepage'))
    return render_template("register.html", images=images)



#
# end fendy's stuff
#

if __name__ == "__main__":
    app.run(debug=True)
