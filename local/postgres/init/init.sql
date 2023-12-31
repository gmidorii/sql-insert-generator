CREATE USER admin WITH PASSWORD 'password';

GRANT ALL PRIVILEGES ON DATABASE db TO admin;

CREATE SCHEMA test AUTHORIZATION admin;

GRANT ALL PRIVILEGES ON SCHEMA public TO admin;
GRANT ALL PRIVILEGES ON SCHEMA test TO admin;

SET search_path TO hoge;

CREATE TABLE info (id varchar);

DO
$$
DECLARE
    table_name text;
BEGIN
    FOR table_name IN (SELECT tablename FROM pg_tables WHERE schemaname = 'test')
    LOOP
        EXECUTE format('GRANT ALL ON test.%I TO admin', table_name);
        EXECUTE format('ALTER TABLE %I OWNER TO admin', table_name);
    END LOOP;
END;
$$;