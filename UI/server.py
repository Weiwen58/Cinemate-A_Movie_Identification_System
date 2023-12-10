from flask import Flask, render_template, request, jsonify
import mysql.connector
from sqlalchemy import create_engine
from backend import compute_movies


app = Flask(__name__)

# Replace these with your actual database details
mydb = mysql.connector.connect(
    host="localhost", user="root", password="password", database="movies_metadata"
)

mycursor = mydb.cursor()
engine = create_engine("mysql+mysqlconnector://root:password@localhost/movies_metadata")

@app.route('/your_backend_endpoint', methods=['POST'])
def receiver_user_input():
    received_data = request.json
    movies_list = compute_movies(received_data)  # Assuming compute_movies() creates a list of movie strings
    movies = [{"title": movie} for movie in movies_list]
    return jsonify(movies)

@app.route("/get_characters", methods=["GET"])
def get_characters():
    try:
        actor_name = request.args.get('actor_name')
        # Establish your database connection
        mydb = mysql.connector.connect(
            host="localhost", user="root", password="password", database="movies_metadata"
        )
        mycursor = mydb.cursor()

        characters_query = """SELECT `character` 
                            FROM has_cast HC
                            JOIN actors A ON A.id = HC.actorId
                            WHERE A.name = %s
                            """

        mycursor.execute(characters_query, (actor_name,))
        characters = [row[0] for row in mycursor.fetchall()]

        # Close database connection
        mycursor.close()
        mydb.close()

        return jsonify({"characters": characters})

    except Exception as e:
        print(f"Error: {e}")  # Log the error to understand the issue
        return jsonify({"characters": []})  # Return an empty list or handle the error response appropriately

@app.route("/")
def index():
    # Connect to the database

    try:
        with mycursor as cursor:
            query = "SELECT DISTINCT A.name FROM actors A ORDER BY A.name"
            cursor.execute(query)
            actors = [row[0] for row in cursor.fetchall()]

            query = "SELECT DISTINCT HC.character FROM has_cast HC ORDER BY HC.character"
            cursor.execute(query)
            characters = [row[0] for row in cursor.fetchall()]
            
            query = "SELECT DISTINCT PC.name FROM productioncompanies PC ORDER BY PC.name"
            cursor.execute(query)
            production_companies = [row[0] for row in cursor.fetchall()]
            
            query = "SELECT DISTINCT G.name FROM genres G ORDER BY G.name"
            cursor.execute(query)
            genres = [row[0] for row in cursor.fetchall()]

            query = "SELECT DISTINCT D.name FROM director D ORDER BY D.name"
            cursor.execute(query)
            director = [row[0] for row in cursor.fetchall()]

    finally:
        mycursor.close()

    return render_template("index.html", actors=actors, characters=characters, production_companies = production_companies,genres = genres, director = director)

if __name__ == "__main__":
    app.run(debug=True)
