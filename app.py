from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error


app = Flask(__name__)

# Database connection
def create_db_connection():
    connection = mysql.connector.connect(
        host='localhost',  
        user='root',  
        password='appleT@2024', 
        database='music_management'
    )
    return connection

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Music Management System!"})

@app.route('/songs', methods=['GET'])
def get_songs():
    try:
        connection = create_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM songs")
        songs = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(songs)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)})
    
def validate_song_data(data):
    errors = []
    
    # Check required fields
    

@app.route('/songs', methods=['POST'])
def add_song():
    data = request.get_json()
    
    title = data.get('title')
    artist = data.get('artist')
    genre = data.get('genre')
    album = data.get('album')   # Include album
    year = data.get('year')  
       
    if not title or not isinstance(title, str):
        return jsonify({"error": "Title is required and must be a string."}), 400
    if not artist or not isinstance(artist, str):
        return jsonify({"error": "Artist is required and must be a string."}), 400
    if not genre or not isinstance(genre, str):
        return jsonify({"error": "Genre is required and must be a string."}), 400
    
    if album and not isinstance(album, str):  # Album is optional but must be a string if provided
        return jsonify({"error": "Album must be a string."}), 400
    
    if year is not None:
        if not isinstance(year, int):  # Ensure year is an integer
            return jsonify({"error": "Year must be an integer."}), 400
        if year < 0 or year > 2024:  # Check for a valid year range
            return jsonify({"error": "Year must be between 0 and 2024."}), 400


    try:
        connection = create_db_connection()
        cursor = connection.cursor()

        # Insert all fields including album and year
        cursor.execute("""
            INSERT INTO songs (title, artist, genre, album, year) 
            VALUES (%s, %s, %s, %s, %s)
        """, (title, artist, genre, album, year))
        
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({"message": "Song added successfully!"}), 201
    except Error as err:
        return jsonify({"error": str(err)}), 400


@app.route('/songs/<int:song_id>', methods=['PUT'])
def update_song(song_id):
    data = request.get_json()  # Use request.get_json() to parse incoming data

    title = data.get('title')
    artist = data.get('artist')
    album = data.get('album')   # Include album
    year = data.get('year')   
    if not title or not isinstance(title, str):
        return jsonify({"error": "Title is required and must be a string."}), 400
    if not artist or not isinstance(artist, str):
        return jsonify({"error": "Artist is required and must be a string."}), 400
    if not genre or not isinstance(genre, str):
        return jsonify({"error": "Genre is required and must be a string."}), 400
    
    if album and not isinstance(album, str):  # Album is optional but must be a string if provided
        return jsonify({"error": "Album must be a string."}), 400
    
    if year is not None:
        if not isinstance(year, int):  # Ensure year is an integer
            return jsonify({"error": "Year must be an integer."}), 400
        if year < 0 or year > 2024:  # Check for a valid year range
            return jsonify({"error": "Year must be between 0 and 2024."}), 400


    try:
        connection = create_db_connection()
        cursor = connection.cursor()

        # Update all fields including album and year
        cursor.execute("""
            UPDATE songs
            SET title = %s, artist = %s, album = %s, release_year = %s
            WHERE id = %s
        """, (title, artist, album, year, song_id))
        
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({"message": "Song updated successfully!"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400
    
def not_found_error(e):
        return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(405)
def method_not_allowed_error(e):
        return jsonify({"error": "Method not allowed"}), 405


@app.route('/songs/<int:song_id>', methods=['DELETE'])
def delete_song(song_id):
    connection = create_db_connection()
    cursor = connection.cursor()

    # Delete the song from the database
    cursor.execute("DELETE FROM songs WHERE id = %s", (song_id,))
    connection.commit()

    cursor.close()
    connection.close()
    return jsonify({"message": "Song deleted successfully!"}), 200


if __name__ == '__main__':
    app.run(debug=True)


