import mysql.connector
import pandas as pd
import ast
from sqlalchemy import create_engine

mydb = mysql.connector.connect(
  host="localhost",
  user="sqluser",
  password="password",
  database="movies_metadata"
)
mycursor = mydb.cursor()
engine = create_engine('mysql+mysqlconnector://sqluser:password@localhost/movies_metadata')

# main dataset
# df = pd.read_csv("./data/new_movies_metadata.csv")
# dic_columns = ["genres", "production_companies", "production_countries", "spoken_languages",
#                "keywords", "cast", "crew"]
# for c in dic_columns:
#     df[c] = df[c].apply(lambda x: ast.literal_eval(x) if pd.notnull(x) and x != '[]' else [])


# movies table
# movie_columns = ["id", "imdb_id", "title", "language", "isAdult", "releaseDate", "runtimeMinutes"]
# movie_table = df[movie_columns]

# movie_table.to_sql(name="movies", con=engine, if_exists="append", index=False)



# productionCompanies table
# unique_companies = set()
# for company_list in df["production_companies"]:
#   for company in company_list:
#       unique_companies.add((company.get("id"), company.get("name")))

# for id, name in unique_companies:
#   query = "INSERT IGNORE INTO productionCompanies (id, name) VALUES (%s, %s);"
#   mycursor.execute(query, (id, name))

# mydb.commit()



# produce table (relationship)
# for _, row in df.iterrows():
#   movie_id = row["id"]
#   for company in row["production_companies"]:
#     company_id = company.get("id")
#     query = "INSERT IGNORE INTO produce (movieId, productionCompanyId) VALUES (%s, %s);"
#     mycursor.execute(query, (movie_id, company_id))

# mydb.commit()



# ratings table
# ratings_columns = ["id", "averageRating", "numVotes"]
# ratings_table = df[ratings_columns].rename(columns={"id": "movieId"})

# ratings_table.to_sql(name="ratings", con=engine, if_exists="append", index=False)



# genres table
# unique_genres = set()
# for genres_list in df["genres"]:
#   for genre in genres_list:
#       unique_genres.add((genre.get("id"), genre.get("name")))

# for id, name in unique_genres:
#   query = "INSERT IGNORE INTO genres (id, name) VALUES (%s, %s);"
#   mycursor.execute(query, (id, name))



# movie_genre table
# for _, row in df.iterrows():
#   movie_id = row["id"]
#   for genre in row["genres"]:
#       genre_id = genre.get("id")
#       query = "INSERT INTO movie_genres (movieId, genreId) VALUES (%s, %s);"
#       mycursor.execute(query, (movie_id, genre_id))

# mydb.commit()



# spokenLanguage table
# unique_languages = set()
# for l_list in df["spoken_languages"]:
#   for l in l_list:
#       unique_languages.add((l.get("iso_639_1"), l.get("name")))

# for language_code, name in unique_languages:
#   query = "INSERT IGNORE INTO spokenLanguage (languageCode, name) VALUES (%s, %s);"
#   mycursor.execute(query, (language_code, name))



# productionCountries table
# unique_countries = set()
# for countries_list in df["production_countries"]:
#   for country in countries_list:
#       unique_countries.add((country.get("iso_3166_1"), country.get("name")))

# for country_code, name in unique_countries:
#   query = "INSERT IGNORE INTO productionCountries (countryCode, name) VALUES (%s, %s);"
#   mycursor.execute(query, (country_code, name))

# mydb.commit()



# commercial table
# commercial_columns = ["popularity", "budget", "revenue", "status", "id"]
# commercial_table = df[commercial_columns].rename(columns={"id": "movieId"})
# commercial_table["popularity"] = commercial_table["popularity"].round(5)

# commercial_table.to_sql(name="commercial", con=engine, if_exists="append", index=False)



# commercial_productionCountries table
# fetch_query = "SELECT id FROM movies_metadata.commercial WHERE movieId = %s;"

# for _, row in df.iterrows():
#   movie_id = row["id"]
#   mycursor.execute(fetch_query, (movie_id,))
#   commercial_id = mycursor.fetchone()
#   query = "INSERT IGNORE INTO commercial_productionCountries (commercialId, productionCountryCode) VALUES (%s, %s);"
#   for country in row["production_countries"]:
#     country_code = country.get("iso_3166_1")
#     mycursor.execute(query, (commercial_id[0], country_code))

# mydb.commit()



# details table
# df = pd.read_csv("./new_basics.csv")
# details_columns = ["original_title", "overview", "tagline", "startYear", "id"]
# details_table = df[details_columns].rename(columns={"id": "movieId", "original_title": "originalTitle"})

# details_table.to_sql(name="details", con=engine, if_exists="append", index=False)



# details_spokenLanguage table
# fetch_query = "SELECT detailId FROM movies_metadata.details WHERE movieId = %s;"

# for _, row in df.iterrows():
#   movie_id = row["id"]
#   mycursor.execute(fetch_query, (movie_id,))
#   detail_id = mycursor.fetchone()
  
#   query = "INSERT IGNORE INTO details_spokenLanguage (detailId, languageCode) VALUES (%s, %s);"
#   for language in row["spoken_languages"]:
#     language_code = language.get("iso_639_1")
#     mycursor.execute(query, (detail_id[0], language_code))

# mydb.commit()



# keywords table
# keywords_df = pd.read_csv("./data/keywords.csv")
# dic_columns = ["keywords"]
# for c in dic_columns:
#     keywords_df[c] = keywords_df[c].apply(lambda x: ast.literal_eval(x) if x and x != '[]' else [])
# unique_keywords = set()
# for keywords_list in keywords_df["keywords"]:
#   for keyword in keywords_list:
#       unique_keywords.add((keyword.get("id"), keyword.get("name")))

# for id, name in unique_keywords:
#   query = "INSERT IGNORE INTO keywords (id, name) VALUES (%s, %s);"
#   mycursor.execute(query, (id, name))

# mydb.commit()



# movie_keywords table
# for _, row in df.iterrows():
#   movie_id = row["id"]
#   for keyword in row["keywords"]:
#     keyword_id = keyword.get("id")
#     query = "INSERT IGNORE INTO movie_keywords (movieId, keywordId) VALUES (%s, %s);"
#     mycursor.execute(query, (movie_id, keyword_id))

# mydb.commit()



# actor and has_cast table
# unique_casts = set()
# unique_actors = set()
# for _, row in df.iterrows():
#   movie_id = row["id"]
#   for cast in row["cast"]:
#     unique_casts.add((cast.get("cast_id"), cast.get("character"), cast.get("credit_id"), cast.get("order"), cast.get("id"), movie_id))
#     unique_actors.add((cast.get("id"), cast.get("name"), cast.get("gender")))

# for cast_id, name, gender in unique_actors:
#   query = "INSERT IGNORE INTO actors (id, name, gender) VALUES (%s, %s, %s);"
#   mycursor.execute(query, (cast_id, name, gender))

# for cast_id, character, credit_id, order, actorId, movieId in unique_casts:
#   query = "INSERT IGNORE INTO has_cast (castId, `character`, creditId, `order`, actorId, movieId) VALUES (%s, %s, %s, %s, %s, %s);"
#   mycursor.execute(query, (cast_id, character, credit_id, order, actorId, movieId))

# mydb.commit()



# crew table
# unique_crews = set()
# for crews_list in df["crew"]:
#   for crew in crews_list:
#     unique_crews.add((crew.get("id"), crew.get("job"), crew.get("department"), crew.get("credit_id"), crew.get("gender"), crew.get("name")))

# for id, job, department, credit_id, gender, name in unique_crews:
#   query = "INSERT IGNORE INTO crew (id, job, department, creditId, gender, name) VALUES (%s, %s, %s, %s, %s, %s);"
#   mycursor.execute(query, (id, job, department, credit_id, gender, name))

# mydb.commit()



# has_crew table
# for _, row in df.iterrows():
#   movie_id = row["id"]
#   for crew in row["crew"]:
#     crew_id = crew.get("id")
#     query = "INSERT IGNORE INTO has_crew (crewId, movieId) VALUES (%s, %s);"
#     mycursor.execute(query, (crew_id, movie_id))

# mydb.commit()

from nltk.tokenize import word_tokenize

mycursor.execute("SELECT id, overview FROM movies")
overview_data = mycursor.fetchall()

movie_ids = []
tokenized_overviews = []
for overview in overview_data:
  if overview[1]:
    movie_ids.append(overview[0])
    tokens = word_tokenize(overview[1])
    tokenized_overviews.append(tokens)

query = "INSERT INTO overviewtokens (movieId, token) VALUES (%s, %s)"

for i in range(len(movie_ids)):
  movie_id = movie_ids[i]
  for token in tokenized_overviews[i]:
    mycursor.execute(query, (movie_id, token))

mycursor.close()
mydb.close()