CREATE TABLE IF NOT EXISTS "user" (id varchar PRIMARY KEY, name varchar NOT NULL, email varchar UNIQUE NOT NULL, profile_pic varchar NOT NULL);

CREATE TABLE IF NOT EXISTS "tasks" (id SERIAL PRIMARY KEY, task varchar NOT NULL,   status varchar,   user_id varchar NOT NULL,   CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES "user"(id));
