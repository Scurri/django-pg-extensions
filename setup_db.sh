export PGUSER=postgres
psql template1 -E <<- EOSQL
	CREATE EXTENSION IF NOT EXISTS hstore;
	CREATE EXTENSION IF NOT EXISTS citext;
	CREATE EXTENSION IF NOT EXISTS pg_trgm;
	CREATE USER dbuser WITH PASSWORD 'dbpass' CREATEDB;
	CREATE DATABASE test_db TEMPLATE template1 ENCODING 'UTF8';
	GRANT ALL PRIVILEGES ON DATABASE test_db TO dbuser;
EOSQL