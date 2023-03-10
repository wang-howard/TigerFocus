CREATE TABLE users(
	user_id serial PRIMARY KEY,
	first_name VARCHAR(20) NOT NULL,
	last_name VARCHAR(20) NOT NULL,
	last_login TIMESTAMP
);


