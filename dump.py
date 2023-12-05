import mysql.connector
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer


mydb = mysql.connector.connect(
  host="localhost",
  user="sqluser",
  password="password",
  database="movies_metadata"
)
mycursor = mydb.cursor()

query = "SELECT movieId, GROUP_CONCAT(token SEPARATOR ' ') FROM overviewtokens GROUP BY movieId"
mycursor.execute(query)
tokenized_movies = mycursor.fetchall()

# Extract tokenized overviews and movie IDs
movie_ids = [data[0] for data in tokenized_movies]
tokenized_overviews = [data[1] for data in tokenized_movies]

# Initialize the TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer()

# Fit and transform the movie overviews to TF-IDF vectors
tfidf_matrix = tfidf_vectorizer.fit_transform(tokenized_overviews)

with open('movie_ids.pkl', 'wb') as movie_ids_file:
    pickle.dump(movie_ids, movie_ids_file)
    
with open('tfidf_matrix.pkl', 'wb') as matrix_file:
    pickle.dump(tfidf_matrix, matrix_file)

with open('tfidf_vectorizer.pkl', 'wb') as vectorizer_file:
    pickle.dump(tfidf_vectorizer, vectorizer_file)

mycursor.close()
mydb.close()