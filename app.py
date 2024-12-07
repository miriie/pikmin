from flask import Flask, request, jsonify, render_template
from database import get_db_connection, initialize_database
import sqlite3

app = Flask(__name__)
# creating an instance of the flask application which will serve as the webserver

# using a variable to handle multiple games dynamically
@app.route('/game/<game_name>')
def game_page(game_name):
    connection = sqlite3.connect('database.py')
    cursor = connection.cursor()

    #fetching game information
    query = "SELECT title, description, rating, image FROM games WHERE name = ?"
    cursor.execute(query, (game_name,))
    game = cursor.fetchone()

    # fetching reviews from the reviews table (in the same file tho)
    query_reviews = "SELECT username, review_text, rating FROM revoews WHERE game_name = ?"
    cursor.execute(query_reviews, (game_name,))
    reviews = cursor.fetchall

    connection.close()


    if game:
        game_data = {
            "titles":game[0],
            "description": game[1],
            "rating": game[2],
            "image": game[3],
            "reviews": [{"username": r[0], "text": r[1], "rating": r[2]} for r in reviews]
        }
        return render_template('gamepage.html', game=game_data)
    else:
        return "Game not found", 404


# @app.route('/add_review', methods=['POST'])
# def add_review():
#     data =request.json