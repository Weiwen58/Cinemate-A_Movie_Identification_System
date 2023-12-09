def compute_movies(received_object):
    import mysql.connector
    from sqlalchemy import create_engine
    import pickle
    from sklearn.preprocessing import normalize
    from sklearn.metrics.pairwise import cosine_similarity

    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="movies_metadata"
    )
    mycursor = mydb.cursor()
    engine = create_engine('mysql+mysqlconnector://sqluser:password@localhost/movies_metadata')
    query=""
    final_result = []
    
    #Actors and characters
    for i in range (1,6):
        actor_val= received_object.get(f"actor{i}")
        char_val= received_object.get(f"character{i}")
        # if (i == 1 and query != '') or (i > 1 and i <= 6-1): 
        #     query += "\nINTERSECT\n"
        if(actor_val != '' and char_val==''): # 1st case
            if (query != ''):
                query += "\nINTERSECT\n"
            query += f"SELECT M.Id, M.title FROM movie M, has_cast C, actors A WHERE M.id = C.movieId AND C.actorId = A.id AND A.name = '{actor_val}'"
        elif(actor_val == '' and char_val!=''): # 2nd case
            if (query != ''):
                query += "\nINTERSECT\n"
            query += f"SELECT M.Id, M.title FROM movie M, has_cast C WHERE M.id = C.movieId AND C.character = '{char_val}'"
        elif(actor_val != '' and char_val !=''): # 3rd case
            if (query != ''):
                query += "\nINTERSECT\n"
            query += f"SELECT M.Id, M.title FROM movie M, has_cast C, actors A WHERE M.id = C.movieId AND C.actorId = A.id AND A.name = '{actor_val}' AND C.character = '{char_val}'"
    
    
    
    # production company
    pc_val=received_object.get("production_company1")
    if(pc_val != ''):
        if (query != ''):
                query += "\nINTERSECT\n"
        query += f"SELECT M.Id, M.title FROM productionCompanies PC, movie M, produce P WHERE P.movieId = M.id AND P.pcId = PC.id AND PC.name = '{pc_val}'"
        
    
    # Genres
    for i in range(1,4):
        genre_val= received_object.get(f"genre{i}")
        if(genre_val != ''):
            if (query != ''):
                query += "\nINTERSECT\n"
            query += f"SELECT M.Id, M.title FROM movie M, movie_genres MG, genres G WHERE M.id = MG.movieId AND MG.genreId = G.id AND G.name = '{genre_val}'"
    
    
    
    # Director
    dir_val= received_object.get("director1")
    if(dir_val != ''):
        if (query != ''):
                query += "\nINTERSECT\n"
        query+=f"SELECT M.Id, M.title FROM movie M, directs MD, director D WHERE M.id = MD.movieId AND MD.directorId = D.id AND D.name= {dir_val}"
    
    
    # Time of Watch
    time= received_object.get("year")
    if(time != ''):
        if (query != ''):
                query += "\nINTERSECT\n"
        query+=f"SELECT M.Id, M.title FROM movie M WHERE YEAR(M.releaseDate) <= {time}"
    
    
    #Overview 
    filtered_result = []
    if query != '':
        mycursor.execute(query) #execute the query
        filtered_result = mycursor.fetchall()
    titles = []
    user_query = received_object.get("overview")
    if user_query != '':
        if filtered_result == []:
            mycursor.execute("SELECT M.id From Movie M")
            filtered_movies_ids = [i[0] for i in mycursor.fetchall()]
        else:  
            filtered_movies_ids = [i[0] for i in filtered_result]#ids of the movies resulted from the above filtering
        
        with open('movie_ids.pkl', 'rb') as movie_ids_file:
            all_movie_ids = pickle.load(movie_ids_file)

        # Load TF-IDF matrix and vectorizer
        with open('tfidf_matrix.pkl', 'rb') as matrix_file:
            tfidf_matrix = pickle.load(matrix_file)

        with open('tfidf_vectorizer.pkl', 'rb') as vectorizer_file:
            tfidf_vectorizer = pickle.load(vectorizer_file)

        # Transform the query to a TF-IDF vector
        query_vector = tfidf_vectorizer.transform([user_query])

        #new code

        filtered_indices = [i for i, movie_id in enumerate(all_movie_ids) if movie_id in filtered_movies_ids]
        filtered_tfidf_matrix = tfidf_matrix[filtered_indices, :]
        filtered_movie_ids = [all_movie_ids[i] for i in filtered_indices]

        # Normalize the filtered TF-IDF matrix
        tfidf_matrix_normalized_filtered = normalize(filtered_tfidf_matrix, norm='l2', axis=1)
        cosine_similarities = cosine_similarity(query_vector, tfidf_matrix_normalized_filtered)
        ####

        # Get the indices of movies sorted by their similarity to the query
        similar_movies_indices = cosine_similarities.argsort()[0][::-1]

        # Filter movies based on the threshold
        min_similarity_threshold = 0.1
        #Initialize a maximum similarity threshold
        max_similarity_threshold = 0.99
        similar_movies_indices = [idx for idx in similar_movies_indices if cosine_similarities[0][idx] > min_similarity_threshold] # at least 10% similar
        similar_movie_ids = [filtered_movie_ids[idx] for idx in similar_movies_indices if cosine_similarities[0][idx] > max_similarity_threshold]
         
        while len(similar_movie_ids) < 1 and max_similarity_threshold > 0.01:
            similar_movie_ids = [filtered_movie_ids[idx] for idx in similar_movies_indices if cosine_similarities[0][idx] > max_similarity_threshold]
            max_similarity_threshold -= 0.01


        query = "SELECT title FROM movie WHERE id = %s"

        for movie_id in similar_movie_ids:
            mycursor.execute(query, (movie_id, ))
            result = mycursor.fetchone()
            if result:
                titles.append(result[0])
        final_result = titles
    else:
        final_result=filtered_result
        
    mycursor.close()
    mydb.close()
    return final_result[:11]