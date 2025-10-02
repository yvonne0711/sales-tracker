# Database
This directory contains all the files required to set up a PostgreSQL database for this project.

## Description
- **`schema.sql`**  
  Contains the SQL commands to create all the tables defined in the project [ERD](../diagrams/database_erd.png).
- **`connect.zsh`**  
  Uses your database credentials (stored in a `.env` file) to connect to the database and run `schema.sql`, 
  creating the database schema and generating all necessary tables.

## Getting Started

### Environment Setup
Create a `.env` file with the following variables:

```env
DB_USERNAME=your_username
DB_PASSWORD=your_password
DB_HOST=your_host
```

### Requirements
- Access to a PostgreSQL database.
- `psql` installed and available in your PATH.

### Running the Setup
```bash connect.zsh```sh