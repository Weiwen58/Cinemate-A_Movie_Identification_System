from flask import Flask, render_template, request, jsonify
import mysql.connector
# from sqlalchemy import create_engine
from backend import compute_movies


app = Flask(__name__)

# Replace these with your actual database details
mydb = mysql.connector.connect(
    host="localhost", user="root", password="password", database="movies_metadata"
)

mycursor = mydb.cursor()
# engine = create_engine("mysql+mysqlconnector://root:password@localhost/movies_metadata")

@app.route('/your_backend_endpoint', methods=['POST'])
def receiver_user_input():
    received_data = request.json
    movies_list = compute_movies(received_data)  # Assuming compute_movies() creates a list of movie strings
    movies = [{"title": movie} for movie in movies_list]
    return jsonify(movies)

# @app.route('/get_movies')
# def get_movies(movies_list):
#     # Format the movies_list into a list of dictionaries
#     movies = [{"title": movie} for movie in movies_list]

#     return jsonify(movies)



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

            query = "SELECT DISTINCT L.name FROM spokenlanguage L ORDER BY L.name"
            cursor.execute(query)
            language = [row[0] for row in cursor.fetchall()]

    finally:
        mycursor.close()

    return render_template("index.html", actors=actors, characters=characters, production_companies = production_companies,genres = genres, director = director, language = language)


if __name__ == "__main__":
    app.run(debug=True)