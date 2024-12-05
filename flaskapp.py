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

    query = "SELECT title, description, rating, image FROM games WHERE name = ?"
    cursor.execute(query, (game_name,))
    game = cursor.fetchone()
    connection.close()

    if game:
        game_data = {
            "titles":game[0],
            "description": game[1],
            "rating": game[2],
            "image": game[3]
        }
        return render_template('game-page.html', game=game_data)
    else:
        return "Game not found", 404


@app.route('/add_review', methods=['POST'])
def add_review():
    data =request.json