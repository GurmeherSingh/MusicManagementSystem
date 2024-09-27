from flask import Flask, jsonify
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

if __name__ == '__main__':
    app.run(debug=True)
