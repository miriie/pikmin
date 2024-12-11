cursor.execute("SELECT id FROM games WHERE title = ?", (review[0],))
game_id_row = cursor.fetchone()
print(f"Game ID row for {review[0]}: {game_id_row}")  # Debugging line

cursor.execute("SELECT username FROM users WHERE username = ?", (review[5],))
username_row = cursor.fetchone()
print(f"Username row for {review[5]}: {username_row}")  # Debugging line
