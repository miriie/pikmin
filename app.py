import random
from flask import Flask, render_template, redirect, url_for, session, request
from datetime import datetime
import pytz
import sqlite3

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

    if request.method == 'POST':
        # Handle the form submission for adding a review
        username = request.form['username']
        rating = int(request.form['rating'])
        review_title = request.form['review_title']
        review_text = request.form['review']
        
        # Get the current time in Sydney, Australia
        sydney_tz = pytz.timezone('Australia/Sydney')
        current_date = datetime.now(sydney_tz).strftime('%Y-%m-%d')

        # Fetch user ID based on username
        user_query = "SELECT id FROM users WHERE username = ?"
        user_id_row = connection.execute(user_query, (username,)).fetchone()

        if not user_id_row:
            return "User not found. Review not submitted.", 400
        
        user_id = user_id_row['id']

        # Insert the new review into the database
        insert_review_query = '''
        INSERT INTO reviews (game_id, rating, review, title, date, user_id)
        VALUES (?, ?, ?, ?, ?, ?)
        '''
        connection.execute(insert_review_query, (game_id, rating, review_text, review_title, current_date, user_id))
        connection.commit()
    
    # Fetch game information based on the game ID
    query_game = "SELECT title, description, rating, image FROM games WHERE id = ?"
    game = connection.execute(query_game, (game_id,)).fetchone()

    # Fetch reviews for the game
    query_reviews = '''
    SELECT users.username, users.profile_picture, reviews.title AS review_title, 
           reviews.review, reviews.rating, reviews.date
    FROM reviews
    JOIN users ON reviews.user_id = users.id
    WHERE reviews.game_id = ?
    '''
    reviews = connection.execute(query_reviews, (game_id,)).fetchall()

    connection.close()

    if game:
        game_data = {
            "title": game['title'],
            "description": game['description'],
            "rating": game['rating'],
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
        return render_template('gamepage.html', game=game_data)
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

# i moved the login and logout defs to my section

#
# end trang stuff
#

#
# fendy stuff
#

def init_db():
    with sqlite3.connect("users.db") as connection:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
                username TEXT UNIQUE,
                password TEXT
            )
        """)    
        connection.commit()

@app.route("/login", methods= ["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        with sqlite3.connect("users.db") as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT username, password FROM users WHERE username = ?", (username,))
            existing_user = cursor.fetchone()
        
        if existing_user:
            db_password = existing_user[1]
            if password == db_password:
                session["username"] = username
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
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        re_password = request.form["re-password"]

        with sqlite3.connect("users.db") as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
            existing_user = cursor.fetchone()
        
        # user taken
        if existing_user:
            return render_template("register.html", message= "Error: Username already taken")

        # password min length
        if len(password) <= 8:
            return render_template("register.html", message= "Error: Password must be at least 8 characters long")

        # passwords match
        if password != re_password:
            return render_template("register.html", message= "Error: Passwords do not match")
        
        # successful registration 
        with sqlite3.connect("users.db") as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO users(username, password) VALUES (?, ?)", 
                        (username, password))
            connection.commit()

        return render_template("register.html", message= "Registration successful")
    return render_template("register.html")

#
# end fendy's stuff
#

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
