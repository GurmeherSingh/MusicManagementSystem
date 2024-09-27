from flask import Flask, jsonify
import mysql.connector
from flask import request

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

    try:
        connection = create_db_connection()
        cursor = connection.cursor()

        cursor.execute("INSERT INTO songs (title, artist, genre) VALUES (%s, %s, %s)", 
                       (title, artist, genre))
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({"message": "Song added successfully!"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400

@app.route('/songs/<int:song_id>', methods=['PUT'])
def update_song(song_id):
    connection = create_db_connection()
    cursor = connection.cursor()

    # Get updated song data from the request
    song_data = request.json
    title = song_data.get('title')
    artist = song_data.get('artist')
    album = song_data.get('album')
    year = song_data.get('year')

    # Update the song in the database
    cursor.execute("""
        UPDATE songs
        SET title = %s, artist = %s, album = %s, year = %s
        WHERE id = %s
    """, (title, artist, album, year, song_id))
    connection.commit()

    cursor.close()
    connection.close()
    return jsonify({"message": "Song updated successfully!"}), 200


if __name__ == '__main__':
    app.run(debug=True)
