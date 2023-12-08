import mysql.connector
import pickle
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string_cleaning
from sklearn.preprocessing import normalize

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="movies_metadata"
)
mycursor = mydb.cursor()




web_query = string_cleaning.clean_string_ret_string()#here will be the user input, the function will return a string

with open('movie_ids.pkl', 'rb') as movie_ids_file:
    all_movie_ids = pickle.load(movie_ids_file)

# Load TF-IDF matrix and vectorizer
with open('tfidf_matrix.pkl', 'rb') as matrix_file:
    tfidf_matrix = pickle.load(matrix_file)

with open('tfidf_vectorizer.pkl', 'rb') as vectorizer_file:
    tfidf_vectorizer = pickle.load(vectorizer_file)

# Transform the query to a TF-IDF vector
query_vector = tfidf_vectorizer.transform([web_query])

#new code
filtered_movies_ids = []#just a place holder till we get the filtered movies
filtered_indices = [i for i, movie_id in enumerate(all_movie_ids) if movie_id in filtered_movies_ids]
filtered_tfidf_matrix = tfidf_matrix[filtered_indices, :]
filtered_movie_ids = [all_movie_ids[i] for i in filtered_indices]

# Fit and transform the filtered movie overviews to TF-IDF vectors
tfidf_matrix_filtered = tfidf_vectorizer.fit_transform(filtered_tfidf_matrix)
# Normalize the filtered TF-IDF matrix
tfidf_matrix_normalized_filtered = normalize(tfidf_matrix_filtered, norm='l2', axis=1)
cosine_similarities = cosine_similarity(query_vector, tfidf_matrix_normalized_filtered)
####

# Calculate cosine similarity between query and all movie overviews
# cosine_similarities = cosine_similarity(query_vector, tfidf_matrix) #commented and if testing goes well will be deleted



# Get the indices of movies sorted by their similarity to the query
similar_movies_indices = cosine_similarities.argsort()[0][::-1]

# Get movie IDs sorted by similarity to the query
similar_movie_ids = [filtered_movie_ids[idx] for idx in similar_movies_indices]

query = "SELECT title FROM movie WHERE id = %s"

titles = []
for movie_id in similar_movie_ids[:6]:
    mycursor.execute(query, (movie_id, ))
    result = mycursor.fetchone()
    if result:
        titles.append(result[0])

print(titles)

mycursor.close()
mydb.close()