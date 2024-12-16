# Cinemate - A Movie Identification System

I. INTRODUCTION

Cinemate is a movie identification system designed to be accurate, accessible, and adaptable. It focuses on helping users recall movie titles based on minimal input, such as actor, character, director, year watched, production company, or genre. It does not generate recommendations but presents movie titles ordered by relevance to the query, without providing trailers or external links.

The current project scope is to provide a streamlined movie recall system. Introducing user accounts, recommendations, or history tracking would significantly expand the scope and require robust user management features.

Cinemate achieves its goals through three key approaches:

Data Acquisition and Integration: Identifying and acquiring movie-related data sources, including datasets, APIs, and web scraping.
Advanced Algorithms: Implementing text-based search, fuzzy string matching, and efficient information retrieval to link user inputs to the database.
Rigorous Data Management: Importing, cleaning, and integrating data from diverse sources to ensure a comprehensive and reliable database.

II. DATA DESCRIPTION

The movie dataset used comes from Kaggle and includes over 45,000 movies with details like genres, title, release date, and more. Specific attributes used include:

● id

● imdb id

● title

● release date

● runtime

● overview

● popularity

● genre

● keywords

● spoken language

● production companies

● cast

● directors

III. METHOD

A. Database (MySQL)

● MySQL database named "movies_metadata" stores movie metadata.

● Schema uses primary and foreign keys to manage relationships between data.

● ON DELETE CASCADE constraints ensure data consistency.

B. Data Import (MySQL + Python)

● Python script connects to the MySQL database.

● Pandas library is used for data manipulation and analysis.

● SQLAlchemy is used for SQL toolkits and Object-Relational Mapping.

● Data from CSV files is imported into the database using pandas.to_sql.

C. Search Engine Logic (Python)

● Users can search for movies based on various parameters.

● Initial filtration uses SQL queries based on user input.

● Second filtration considers movie overviews using TF-IDF vectors and cosine similarity.

● Up to 10 movie titles are recommended based on user input and criteria.

D. Frontend (HTML, CSS, JavaScript, and Ajax)


● User Interface (UI) is built using HTML, CSS, and JavaScript.

● HTML defines the structure of the interface with input fields, labels, and a button.

● CSS styles the HTML elements for a visually appealing layout.


● JavaScript with jQuery adds interactivity and dynamic behavior:

● Character suggestions based on actor selection.

● Input validation for user-entered data.

● Sending validated user inputs to the backend via Fetch API.

● Receiving and displaying movie results.

E. Python Flask Backend

● Python Flask creates a RESTful API for movie search and character lookup.

● API Endpoints:

● POST Route (/cinemate_endpoint): Receives user input, processes it, and returns movie titles.

● GET Route (/get_characters): Retrieves character names for a specific actor.

● Integrates with frontend by rendering an HTML template with dropdowns for user input.

IV. RESULTS AND ANALYSIS

● Search algorithm is accurate and typically completes searches in under one second.

● Up to 10 relevant movie titles are returned.

● Users can enter partial information to select actors, characters, etc.

● Website is accessible by running the file server.py.

● Clean and straightforward interface allows for easy user input.

● Website may experience delays due to memory usage. Future improvements aim to enhance performance.

Additional Notes:

This ReadMe.md file provides a general overview of the Cinemate project.
For more detailed information, please refer to the project's code and documentation.
