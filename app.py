from flask import Flask, jsonify, request
import mysql.connector


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

@app.route('/songs', methods=['POST'])
def add_song():
    data = request.get_json()
    
    title = data.get('title')
    artist = data.get('artist')
    genre = data.get('genre')
    album = data.get('album')   # Include album
    year = data.get('year')     # Include year

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
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400


@app.route('/songs/<int:song_id>', methods=['PUT'])
def update_song(song_id):
    data = request.get_json()  # Use request.get_json() to parse incoming data

    title = data.get('title')
    artist = data.get('artist')
    album = data.get('album')   # Include album
    year = data.get('year')     # Include year

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
