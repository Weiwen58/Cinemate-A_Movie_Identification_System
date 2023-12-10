import mysql.connector
import pickle
from sklearn.preprocessing import normalize
from sklearn.metrics.pairwise import cosine_similarity
import string_cleaning
from collections import defaultdict
import re

def compute_movies(received_object):
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="movies_metadata"
    )
    mycursor = mydb.cursor()
    query=""
    final_result = []
    #test case
    #received_object= {"actor1":"Tom hanks" , "character1": "","actor2":"" , "character2": "","actor3":"" , "character3": "","actor4":"" , "character4": "","actor5":"" , "character5": "","production_company1":"","genre1":"","genre2":"","genre3":"","director1":"","year":"","overview":"Toys that plays"}
    
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
            query += f"SELECT M.Id, M.title FROM movie M, has_cast C WHERE M.id = C.movieId AND (C.character LIKE '%{char_val}%' OR C.character Like '{char_val}%')"
        elif(actor_val != '' and char_val !=''): # 3rd case
            if (query != ''):
                query += "\nINTERSECT\n"
            query += f"SELECT M.Id, M.title FROM movie M, has_cast C, actors A WHERE M.id = C.movieId AND C.actorId = A.id AND A.name = '{actor_val}' AND (C.character LIKE '%{char_val}%' OR C.character Like '{char_val}%')"
    
    
    
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
    user_query = user_query.lower()
    if user_query != '':
        if filtered_result == []:
            mycursor.execute("SELECT M.id From Movie M")
            filtered_movies_ids = [i[0] for i in mycursor.fetchall()]
        else:  
            filtered_movies_ids = [i[0] for i in filtered_result]#ids of the movies resulted from the above filtering
        #Keywords
        ids_str = ', '.join(map(str, filtered_movies_ids))
        #list of keywords for each of the filtered movies
        query_kw = f"SELECT M.id, K.name FROM movie_keywords MK, movie M, keywords K WHERE M.id = MK.movieId AND MK.keywordId = K.id AND M.id IN ({ids_str})"
        mycursor.execute(query_kw)
        list_id_kw = mycursor.fetchall()#list of tuples :(id,kw)
        id_kw_dict = defaultdict(list)#dict that contains id:[kws]
        #filled the dict
        for i in list_id_kw:
            id_kw_dict[i[0]].append(i[1])
        #check matches between the query and the keyword list
        movie_kw_match_dict = defaultdict(int)
        for k,v in id_kw_dict.items():
            for kw in v:
            # Escape special characters and use word boundaries (\b) for whole word matching
                pattern = re.compile(r'\b{}\b'.format(re.escape(kw)))
            # Use findall to find all matches in the user query
                matches = pattern.findall(user_query)
                if matches:
                    movie_kw_match_dict[k] += len(matches)
    
        #if the max number of keyword hits is greater than 1
        max_num_of_hits = 0
        if len(movie_kw_match_dict) > 0:
            _,max_num_of_hits = max(movie_kw_match_dict.items(), key=lambda x: x[1])
            
        if max_num_of_hits > 1:
            list_of_matches = [x for x in sorted(movie_kw_match_dict, key=movie_kw_match_dict.get, reverse=True) if x >= max_num_of_hits//2]#all the movie ids with more than half the max keyword hits
        else:
            list_of_matches = filtered_movies_ids #There is at most one hit which means we will use the overview 
        
            
    
        with open('movie_ids.pkl', 'rb') as movie_ids_file:
            all_movie_ids = pickle.load(movie_ids_file)

        # Load TF-IDF matrix and vectorizer
        with open('tfidf_matrix.pkl', 'rb') as matrix_file:
            tfidf_matrix = pickle.load(matrix_file)

        with open('tfidf_vectorizer.pkl', 'rb') as vectorizer_file:
            tfidf_vectorizer = pickle.load(vectorizer_file)

        clean_usr_query = string_cleaning.clean_string_ret_string(user_query)
        # Transform the query to a TF-IDF vector
        query_vector = tfidf_vectorizer.transform([clean_usr_query])

        #new code

        filtered_indices = [i for i, movie_id in enumerate(all_movie_ids) if movie_id in filtered_movies_ids]
        filtered_tfidf_matrix = tfidf_matrix[filtered_indices, :]
        filtered_movie_ids = [all_movie_ids[i] for i in filtered_indices]

        # Normalize the filtered TF-IDF matrix
        tfidf_matrix_normalized_filtered = normalize(filtered_tfidf_matrix, norm='l2', axis=1)
        # Normalize the filtered TF-IDF vector
        query_vector_normalized= normalize(query_vector, norm='l2', axis=1)
        cosine_similarities = cosine_similarity(query_vector, tfidf_matrix_normalized_filtered)
        ####

        # Get the indices of movies sorted by their similarity to the query
        similar_movies_indices = cosine_similarities.argsort()[0][::-1]

        # Filter movies based on the threshold
        min_similarity_threshold = 0.1
        #Initialize a maximum similarity threshold
        max_similarity_threshold = 0.99
        similar_movies_indices = [idx for idx in similar_movies_indices if cosine_similarities[0][idx] > min_similarity_threshold] # at least 10% similar
        similar_movie_ids = [filtered_movie_ids[idx] for idx in similar_movies_indices if cosine_similarities[0][idx] >= max_similarity_threshold]
         
        while len(similar_movie_ids) < 6 and max_similarity_threshold >= min_similarity_threshold:
            similar_movie_ids = [filtered_movie_ids[idx] for idx in similar_movies_indices if cosine_similarities[0][idx] >= max_similarity_threshold]
            max_similarity_threshold -= 0.01


        
        #get the movie ids with highest keyword hits and similarity
        prioritized_ids = [m_id for m_id in (set(similar_movie_ids) & set(list_of_matches))] #set intersection


        if(len(prioritized_ids) == 0):#no intersection between hits and 
            prioritized_ids = [m_id for m_id in list_of_matches if movie_kw_match_dict[m_id] == max_num_of_hits]
            if max_num_of_hits < 2:
                prioritized_ids.extend(similar_movie_ids)
        
    
        
        query = "SELECT title FROM movie WHERE id = %s"
        for movie_id in prioritized_ids:
            mycursor.execute(query, (movie_id, ))
            result = mycursor.fetchone()
            if result:
                titles.append(result[0])
        final_result = titles

        # for movie_id in similar_movie_ids:
        #     mycursor.execute(query, (movie_id, ))
        #     result = mycursor.fetchone()
        #     if result:
        #         titles.append(result[0])
        # final_result = titles
    else:
        final_result = [set(title[1] for title in filtered_result)]
        
    mycursor.close()
    mydb.close()
    return final_result[:10]


#print(compute_movies(""))