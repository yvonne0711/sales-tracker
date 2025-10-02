# Database
This directory contains all the files required to set up a PostgreSQL database for this project.

## Description
- **`schema.sql`**  
  Contains the SQL commands to create all the tables defined in the project [ERD](diagrams/database_erd.png).
- **`connect.zsh`**  
  Uses your database credentials (stored in a `.env` file) to connect to the database and run `schema.sql`, 
  creating the database schema and generating all necessary tables.
