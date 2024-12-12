
\c postgres

-- Create user if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'test_admin') THEN
        CREATE ROLE test_admin WITH LOGIN PASSWORD 'test1234';
        RAISE NOTICE 'User "test_admin" created.';
    ELSE
        RAISE NOTICE 'User "test_admin" already exists.';
    END IF;
END $$;

-- Create the database if it doesn't exist (run outside of a function)
-- First, check if the database exists, and if not, create it
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'test_database') THEN
        RAISE NOTICE 'Database "test_database" does not exist. It will be created.';
    ELSE
        RAISE NOTICE 'Database "test_database" already exists.';
    END IF;
END $$;

-- Create the database as a standalone statement
CREATE DATABASE test_database OWNER test_admin;

