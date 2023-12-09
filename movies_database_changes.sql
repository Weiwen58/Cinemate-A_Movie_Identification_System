DELETE FROM movies_metadata.movie 
WHERE YEAR(releaseDate) >= 2018;

UPDATE movies_metadata.actors A
SET A.name = REGEXP_REPLACE(A.name, '\t', '')
WHERE A.name LIKE '%\t%';

UPDATE movies_metadata.actors A
SET A.name = TRIM(LEADING ' ' FROM A.name);

UPDATE movies_metadata.director D
SET D.name = REGEXP_REPLACE(D.name, '\t', '')
WHERE D.name LIKE '%\t%';

UPDATE movies_metadata.director D
SET D.name = TRIM(LEADING ' ' FROM D.name);

UPDATE movies_metadata.productioncompanies PC
SET PC.name = REGEXP_REPLACE(PC.name, '\t', '')
WHERE PC.name LIKE '%\t%';

UPDATE movies_metadata.productioncompanies PC
SET PC.name = REGEXP_REPLACE(PC.name, '^•[,#]+', '')
WHERE PC.name REGEXP '^•[,#]+';

UPDATE movies_metadata.productioncompanies PC
SET PC.name = TRIM(LEADING ' ' FROM PC.name);

UPDATE movies_metadata.has_cast HC
SET HC.character = REGEXP_REPLACE(HC.character, '\t', '')
WHERE HC.character LIKE '%\t%';

UPDATE movies_metadata.has_cast HC
SET HC.character = REPLACE(REPLACE(REPLACE(REPLACE(HC.character, '-', ''), '?', ''), ':', ''), '.', '');

UPDATE movies_metadata.has_cast HC
SET HC.character = TRIM(LEADING ' ' FROM HC.character);

-- CREATE TEMPORARY TABLE TempMovieIDs AS
-- SELECT movieId
-- FROM movies_metadata.movies_spokenLanguage
-- WHERE languageCode = 'en';

-- DELETE FROM movies_metadata.movie M
-- WHERE M.id NOT IN (SELECT movieId FROM TempMovieIDs);

-- DROP TEMPORARY TABLE IF EXISTS TempMovieIDs;

SHOW TABLES;
