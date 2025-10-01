'''bash script to connect to RDS, create tables and seed initial data'''
source .env
export PGPASSWORD=$DB_PASSWORD 
psql -h $DB_HOST -p 5432 -U $DB_USERNAME $DB_NAME -f schema.sql