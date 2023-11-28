CREATE DATABASE movies_metadata;
USE movies_metadata;

CREATE TABLE movie (
    id INT PRIMARY KEY,
    imdb_id VARCHAR(20),
    title VARCHAR(255),
    language VARCHAR(20),
    isAdult BOOLEAN,
    releaseDate DATE,
    runtimeMinutes INT
);

CREATE TABLE genres (
    id INT PRIMARY KEY,
    name VARCHAR(255)
);

CREATE TABLE movie_genres (
    movieId INT,
    genreId INT,
    FOREIGN KEY (movieId) REFERENCES movie(id),
    FOREIGN KEY (genreId) REFERENCES genres(id)
);

CREATE TABLE keywords (
    id INT PRIMARY KEY,
    name VARCHAR(255)
);

CREATE TABLE movie_keywords (
    movieId INT,
    keywordId INT,
    FOREIGN KEY (movieId) REFERENCES movie(id),
    FOREIGN KEY (keywordId) REFERENCES keywords(id)
);

CREATE TABLE ratings (
    movieId INT PRIMARY KEY,
    averageRating DECIMAL(3,1),
    numVotes INT,
    FOREIGN KEY (movieId) REFERENCES movie(id)
);

CREATE TABLE details (
    detailId INT PRIMARY KEY AUTO_INCREMENT,
    originalTitle VARCHAR(255),
    overview VARCHAR(1024),
    tagline VARCHAR(1024),
    startYear INT,
    movieId INT UNIQUE,
    FOREIGN KEY (movieId) REFERENCES movie(id)
);

CREATE TABLE spokenLanguage (
    languageCode VARCHAR(20) PRIMARY KEY,
    name VARCHAR(255)
);

CREATE TABLE details_spokenLanguage (
    detailId INT,
    languageCode VARCHAR(20),
    FOREIGN KEY (detailId) REFERENCES details(detailId),
    FOREIGN KEY (languageCode) REFERENCES spokenLanguage(languageCode)
);

CREATE TABLE commercial (
    id INT AUTO_INCREMENT PRIMARY KEY,
    popularity DECIMAL(10,5),
    budget INT,
    revenue INT,
    status VARCHAR(20),
    movieId INT UNIQUE,
    FOREIGN KEY (movieId) REFERENCES movie(id)
);

CREATE TABLE productionCompanies (
    id INT PRIMARY KEY,
    name VARCHAR(255)
);

CREATE TABLE productionCountries (
    countryCode VARCHAR(20) PRIMARY KEY,
    name VARCHAR(255)
);

CREATE TABLE commercial_productionCompanies (
    commercialId INT,
    productionCompanyId INT,
    FOREIGN KEY (commercialId) REFERENCES commercial(id),
    FOREIGN KEY (productionCompanyId) REFERENCES productionCompanies(id)
);

CREATE TABLE commercial_productionCountries (
    commercialId INT,
    productionCountryCode VARCHAR(20),
    FOREIGN KEY (commercialId) REFERENCES commercial(id),
    FOREIGN KEY (productionCountryCode) REFERENCES productionCountries(countryCode)
);

CREATE TABLE actors (
    id INT PRIMARY KEY,
    name VARCHAR(64),
    gender VARCHAR(20)
);

CREATE TABLE has_cast (
    castId INT,
    `character` VARCHAR(64),
    creditId VARCHAR(32),
    `order` INT,
    actorId INT,
    movieId INT,
    PRIMARY KEY (actorId, movieId),
    FOREIGN KEY (actorId) REFERENCES actors(id),
    FOREIGN KEY (movieId) REFERENCES movie(id)
);

CREATE TABLE crew (
    id INT PRIMARY KEY,
    job VARCHAR(32),
    department VARCHAR(32),
    creditId VARCHAR(32),
    gender VARCHAR(20),
    name VARCHAR(64)
);

CREATE TABLE has_crew (
    crewId INT,
    movieId INT,
    PRIMARY KEY (crewId, movieId),
    FOREIGN KEY (crewId) REFERENCES crew(id),
    FOREIGN KEY (movieId) REFERENCES movie(id)
);

SHOW TABLES;

-- DELETE FROM movies_metadata.details_spokenLanguage;
-- DELETE FROM movies_metadata.productioncountries;
-- USE movies_metadata;
