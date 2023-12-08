from flask import Flask, render_template
import mysql.connector
from sqlalchemy import create_engine

app = Flask(__name__)

# Replace these with your actual database details
mydb = mysql.connector.connect(
    host="localhost", user="root", password="password", database="movies_metadata"
)

mycursor = mydb.cursor()
engine = create_engine("mysql+mysqlconnector://root:password@localhost/movies_metadata")


@app.route("/")
def index():
    # Connect to the database

    try:
        with mycursor as cursor:
            query = "SELECT DISTINCT A.name FROM actors A"
            cursor.execute(query)
            actors = [row[0] for row in cursor.fetchall()]

            query = "SELECT DISTINCT HC.character FROM has_cast HC"
            cursor.execute(query)
            characters = [row[0] for row in cursor.fetchall()]
            
            query = "SELECT DISTINCT PC.name FROM productioncompanies PC"
            cursor.execute(query)
            production_companies = [row[0] for row in cursor.fetchall()]
            
            query = "SELECT DISTINCT G.name FROM genres G"
            cursor.execute(query)
            genres = [row[0] for row in cursor.fetchall()]

            query = "SELECT DISTINCT D.name FROM director D"
            cursor.execute(query)
            director = [row[0] for row in cursor.fetchall()]

            query = "SELECT DISTINCT L.name FROM spokenlanguage L"
            cursor.execute(query)
            language = [row[0] for row in cursor.fetchall()]

    finally:
        mycursor.close()

    return render_template("index.html", actors=actors, characters=characters, production_companies = production_companies,genres = genres, director = director, language = language)


if __name__ == "__main__":
    app.run(debug=True)