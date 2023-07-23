import pytest
import psycopg2
import mysql.connector
from src.sql_insert_generator.main import generate_insert_statements_pg, generate_insert_statements_mysql, DEFAULT_VALUES

# replace your_script with the actual name of your script

@pytest.fixture(scope='module')
def postgres_db():
    # Setup: Creating test table for PostgreSQL
    connection_pg = psycopg2.connect(
        dbname='db',
        user='admin',
        password='password',
        host='localhost',
        port='5432'
    )
    cursor_pg = connection_pg.cursor()
    cursor_pg.execute("DROP TABLE IF EXISTS test;")
    cursor_pg.execute("CREATE TABLE test (id serial PRIMARY KEY, name varchar(10), time timestamp);")
    connection_pg.commit()

    yield connection_pg

    # Teardown: Dropping test table for PostgreSQL
    # cursor_pg.execute("DROP TABLE test;")
    # connection_pg.commit()

# @pytest.fixture(scope='module')
# def mysql_db():
#     # Setup: Creating test table for MySQL
#     connection_mysql = mysql.connector.connect(
#         database='test',
#         user='username',
#         password='password',
#         host='localhost',
#         port='3306'
#     )
#     cursor_mysql = connection_mysql.cursor()
#     cursor_mysql.execute("CREATE TABLE test (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(10), time DATETIME);")
#     connection_mysql.commit()

#     yield connection_mysql

#     # Teardown: Dropping test table for MySQL
#     cursor_mysql.execute("DROP TABLE test;")
#     connection_mysql.commit()

def test_generate_insert_statements_pg(postgres_db):
    expected_output = "INSERT INTO test (id, name, time) VALUES (1, 'aaaaaaaaaa', '2022-01-01 10:00:00+09'), (1, 'aaaaaaaaaa', '2022-01-01 10:00:00+09'), (1, 'aaaaaaaaaa', '2022-01-01 10:00:00+09'), (1, 'aaaaaaaaaa', '2022-01-01 10:00:00+09'), (1, 'aaaaaaaaaa', '2022-01-01 10:00:00+09'), (1, 'aaaaaaaaaa', '2022-01-01 10:00:00+09'), (1, 'aaaaaaaaaa', '2022-01-01 10:00:00+09'), (1, 'aaaaaaaaaa', '2022-01-01 10:00:00+09'), (1, 'aaaaaaaaaa', '2022-01-01 10:00:00+09'), (1, 'aaaaaaaaaa', '2022-01-01 10:00:00+09');"
    assert generate_insert_statements_pg(postgres_db, 'test') == expected_output

def test_generate_insert_statements_mysql(mysql_db):
    expected_output = "INSERT INTO test (id, name, time) VALUES (1, 'aaaaaaaaaa', '2022-01-01 10:00:00+09'), (1, 'aaaaaaaaaa', '2022-01-01 10:00:00+09'), (1, 'aaaaaaaaaa', '2022-01-01 10:00:00+09'), (1, 'aaaaaaaaaa', '2022-01-01 10:00:00+09'), (1, 'aaaaaaaaaa', '2022-01-01 10:00:00+09'), (1, 'aaaaaaaaaa', '2022-01-01 10:00:00+09'), (1, 'aaaaaaaaaa', '2022-01-01 10:00:00+09'), (1, 'aaaaaaaaaa', '2022-01-01 10:00:00+09'), (1, 'aaaaaaaaaa', '2022-01-01 10:00:00+09'), (1, 'aaaaaaaaaa', '2022-01-01 10:00:00+09');"
    assert generate_insert_statements_mysql(mysql_db, 'test') == expected_output
