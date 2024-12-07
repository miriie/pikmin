from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/game/<game_name>')
def game_page(game_name):
    connection = sqlite3.connect('my-database.db')
    cursor = connection.cursor()

    # Fetching game information from the database
    query = "SELECT title, description, rating, image FROM games WHERE title = ?"
    cursor.execute(query, (game_name,))
    game = cursor.fetchone()

    # Fetching reviews from the reviews table (in the same file)
    query_reviews = "SELECT username, review, rating FROM reviews WHERE game = ?"
    cursor.execute(query_reviews, (game_name,))
    reviews = cursor.fetchall()

    connection.close()

    if game:
        game_data = {
            "title": game[0],
            "description": game[1],
            "rating": game[2],
            "image": game[3],  # The image filename (relative path)
            "reviews": [{"username": r[0], "review": r[1], "rating": r[2]} for r in reviews]
        }
        return render_template('gamepage.html', game=game_data)
    else:
        return "Game not found", 404

if __name__ == "__main__":
    app.run(debug=True)
