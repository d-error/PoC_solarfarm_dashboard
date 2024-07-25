CREATE DATABASE grafana;
\c grafana

CREATE TABLE test (
    id INT, 
    name VARCHAR(255)
);

CREATE TABLE tracker_data (
    id SERIAL PRIMARY KEY,
    time TIMESTAMP NOT NULL,
    tracker_id VARCHAR NOT NULL,
    value FLOAT NOT NULL
);

