source .env
export PGPASSWORD=$DB_PASSWORD 
psql -h $DB_HOST -p 5432 -U $DB_USERNAME postgres -f schema.sql