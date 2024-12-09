from flask import Flask, render_template
import sqlite3
import random

app = Flask(__name__)

def get_db_connection():
    connection = sqlite3.connect('my-database.db')
    connection.row_factory = sqlite3.Row  # Use Row to get dictionary-like access
    return connection

@app.route('/game/<game_name>')
def game_page(game_name):
    connection = get_db_connection()

    # Fetching game information from the database
    query = "SELECT title, description, rating, image FROM games WHERE title = ?"
    game = connection.execute(query, (game_name,)).fetchone()

    # Fetching reviews from the reviews table
    query_reviews = '''
    SELECT users.username, users.profile_picture, reviews.review, reviews.rating
    FROM reviews
    JOIN users ON reviews.user_id = users.id
    WHERE reviews.game = ?
    '''
    reviews= connection.execute(query_reviews, (game_name,)).fetchall()

    connection.close()

    if game:
        game_data = {
            "title": game['title'],
            "description": game['description'],
            "rating": game['rating'],
            "image": game['image'],  
            "reviews": [{"username": r['username'], "profile_picture": r['profile_picture'], "review": r['review'], "rating": r['rating']} for r in reviews]        }
        return render_template('gamepage.html', game=game_data)
    else:
        return "Page not found", 404

@app.route('/')
def homepage():
    connection = get_db_connection()

    # Fetch popular games based on the number of reviews
    popular_games_query = '''
    SELECT games.*, COUNT(reviews.id) AS review_count
    FROM games
    LEFT JOIN reviews ON reviews.game = games.title
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

if __name__ == "__main__":
    app.run(debug=True)
