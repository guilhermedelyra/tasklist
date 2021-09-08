CREATE DATABASE todo;

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    task varchar NOT NULL,
    status varchar
);

INSERT INTO tasks (task, status) VALUES ('task no.1', 'Todo');
INSERT INTO tasks (task, status) VALUES ('task no.2', 'Todo');
INSERT INTO tasks (task, status) VALUES ('task no.3', 'Todo');