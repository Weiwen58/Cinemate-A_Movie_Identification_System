CREATE DATABASE movies_metadata;
USE movies_metadata;

CREATE TABLE movie (
    id INT PRIMARY KEY,
    imdb_id VARCHAR(20),
    title VARCHAR(255),
    releaseDate DATE,
    runtimeMinutes INT,
    overview VARCHAR(1024),
    popularity DECIMAL(10,5)
);

CREATE TABLE genres (
    id INT PRIMARY KEY,
    name VARCHAR(255)
);

CREATE TABLE movie_genres (
    movieId INT,
    genreId INT,
    FOREIGN KEY (movieId) REFERENCES movie(id) ON DELETE CASCADE,
    FOREIGN KEY (genreId) REFERENCES genres(id) ON DELETE CASCADE,
    PRIMARY KEY (movieId, genreId)
);

CREATE TABLE keywords (
    id INT PRIMARY KEY,
    name VARCHAR(255)
);

CREATE TABLE movie_keywords (
    movieId INT,
    keywordId INT,
    FOREIGN KEY (movieId) REFERENCES movie(id) ON DELETE CASCADE,
    FOREIGN KEY (keywordId) REFERENCES keywords(id) ON DELETE CASCADE,
    PRIMARY KEY (movieId, keywordId)
);

CREATE TABLE spokenLanguage (
    languageCode VARCHAR(20) PRIMARY KEY,
    name VARCHAR(255)
);

CREATE TABLE movies_spokenLanguage (
    movieId INT,
    languageCode VARCHAR(20),
    FOREIGN KEY (languageCode) REFERENCES spokenLanguage(languageCode) ON DELETE CASCADE,
    FOREIGN KEY (movieId) REFERENCES movie(id) ON DELETE CASCADE,
    PRIMARY KEY (movieId, languageCode)
);

CREATE TABLE productionCompanies (
    id INT PRIMARY KEY,
    name VARCHAR(255)
);

CREATE TABLE produce (
    movieId INT,
    pcId INT,
    FOREIGN KEY (movieId) REFERENCES movie(id) ON DELETE CASCADE,
    FOREIGN KEY (pcId) REFERENCES productionCompanies(id) ON DELETE CASCADE,
    PRIMARY KEY (movieId, pcId)
);

CREATE TABLE actors (
    id INT PRIMARY KEY,
    name VARCHAR(64)
);

CREATE TABLE has_cast (
    `character` VARCHAR(64),
    gender VARCHAR(20),
    actorId INT,
    movieId INT,
    FOREIGN KEY (actorId) REFERENCES actors(id) ON DELETE CASCADE,
    FOREIGN KEY (movieId) REFERENCES movie(id) ON DELETE CASCADE,
    PRIMARY KEY (actorId, movieId)
);

CREATE TABLE director (
    id INT PRIMARY KEY,
    name VARCHAR(64)
);

CREATE TABLE directs (
    directorId INT,
    movieId INT UNIQUE,
    FOREIGN KEY (directorId) REFERENCES director(id) ON DELETE CASCADE,
    FOREIGN KEY (movieId) REFERENCES movie(id) ON DELETE CASCADE,
    PRIMARY KEY (directorId, movieId)
);

CREATE TABLE overviewTokens (
    id int PRIMARY KEY AUTO_INCREMENT,
    movieId int,
    token varchar(64),
    FOREIGN KEY (movieId) REFERENCES movie (id) ON DELETE CASCADE
);
