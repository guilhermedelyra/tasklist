CREATE DATABASE todo;

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    task varchar NOT NULL,
    status varchar,
    added_at date NOT NULL,
    difficulty int NOT NULL,
    deadline int NOT NULL,
    importance int NOT NULL
);

INSERT INTO tasks (task, status, added_at, difficulty, deadline, importance) VALUES ('task no.1', 'Todo', '2020-01-01', 3, 1, 10);
INSERT INTO tasks (task, status, added_at, difficulty, deadline, importance) VALUES ('task no.2', 'Todo', '2020-01-01', 3, 1, 10);
INSERT INTO tasks (task, status, added_at, difficulty, deadline, importance) VALUES ('task no.3', 'Todo', '2020-01-01', 3, 1, 10);