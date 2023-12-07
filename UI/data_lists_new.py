from flask import Flask, jsonify, render_template
import mysql.connector

app = Flask(__name__)

# Replace these with your actual database details
mydb = mysql.connector.connect(
    host="localhost", user="root", password="password", database="movies_metadata"
)

@app.route("/")
def index():
    return render_template("index.html")

# Endpoint to fetch distinct actors
@app.route("/get-actors", methods=["GET"])
def get_actors():
    try:
        with mydb.cursor() as cursor:
            query = """SELECT DISTINCT A.name 
                       FROM actors A
                       ORDER BY A.name
            """
            cursor.execute(query)
            actors = [row[0] for row in cursor.fetchall()]
            return jsonify({"actors": actors})
    except Exception as e:
        return jsonify({"error": str(e)})
    
# Endpoint to fetch distinct characters
@app.route("/get-actors", methods=["GET"])
def get_actors():
    try:
        with mydb.cursor() as cursor:
            query = "SELECT DISTINCT A.name FROM actors A"
            cursor.execute(query)
            actors = [row[0] for row in cursor.fetchall()]
            return jsonify({"actors": actors})
    except Exception as e:
        return jsonify({"error": str(e)})

# Add similar endpoints for other data types: characters, production companies, genres, director, language

if __name__ == "__main__":
    app.run(debug=True)
