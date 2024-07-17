-- Adding index 'FULLTEXT' on the table 'questions' to enable fts

USE medflow_db;
ALTER TABLE questions ADD FULLTEXT(title, body);
