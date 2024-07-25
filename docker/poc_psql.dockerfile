FROM postgres:latest

# Add the SQL script to the container
COPY init_db.sql /docker-entrypoint-initdb.d/
