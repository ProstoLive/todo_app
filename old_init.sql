CREATE DATABASE IF NOT EXISTS todo_app;
CREATE ROLE IF NOT EXISTS postgres WITH PASSWORD 'postgres';
GRANT ALL PRIVILEGES ON DATABASE todo_app TO postgres;
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username varchar NOT NULL,
    hashed_password varchar NOT NULL,
    email varchar NOT NULL,
    first_name varchar DEFAULT=NULL,

)