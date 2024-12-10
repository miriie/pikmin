# SQL query written in Python code
popular_games_query = """
SELECT 
    games.title, 
    games.description, 
    games.rating AS average_rating, 
    games.image, 
    COUNT(reviews.id) AS review_count
FROM 
    games
LEFT JOIN 
    reviews ON games.id = reviews.game_id
GROUP BY 
    games.id
ORDER BY 
    average_rating DESC, review_count DESC
LIMIT 10;
"""

# Execute the query
connection = get_db_connection()
popular_games = connection.execute(popular_games_query).fetchall()  # Executes the query, returns results

# The query is still in the code, ready to be executed again if needed
connection.close()

# Continue with processing and using results
