import argparse
import re
import psycopg2
import mysql.connector

# Mapping PostgreSQL and MySQL data types to default values.
DEFAULT_VALUES = {
    'integer': '1',
    'int': '1',
    'int4': '1',
    'bigint': '1',
    'smallint': '1',
    'numeric': '1.0',
    'real': '1.0',
    'double precision': '1.0',
    'double': '1.0',
    'serial': '1',
    'bigserial': '1',
    'money': '1.0',
    'character varying': "'{}'",
    'varchar': "'{}'",
    'character': "'t'",
    'char': "'t'",
    'text': "'test'",
    'timestamp': "'2022-01-01 10:00:00+09'",
    'datetime': "'2022-01-01 10:00:00+09'",
    'date': "'2022-01-01'",
    'time': "'10:00:00'",
    'boolean': 'true',
    'bool': 'true',
    'tinyint': '1',
    'decimal': '1.0',
    'float': '1.0',
    # add more types if necessary...
}

def generate_default_value(column_type, column_type_length):
    default_value = DEFAULT_VALUES.get(column_type, None)
    if column_type in ['character varying', 'varchar'] and column_type_length:
        default_value = default_value.format('a' * int(column_type_length))
    return default_value

def generate_insert_statements_pg(connection, table):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT column_name, udt_name, character_maximum_length FROM information_schema.columns WHERE table_name = '{table}' order by ordinal_position;")
        columns = cursor.fetchall()

        insert_statement = f"INSERT INTO {table} ({', '.join([column[0] for column in columns])}) VALUES "
        value_statements = []
        for _ in range(10):
            y = [generate_default_value(column[1], column[2]) for column in columns]
            x = f"({', '.join(y)})"
            value_statements.append(x)

        return insert_statement + ', '.join(value_statements) + ';'

def generate_insert_statements_mysql(connection, table):
    cursor = connection.cursor()
    cursor.execute(f"SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}';")
    columns = cursor.fetchall()

    insert_statement = f"INSERT INTO {table} ({', '.join([column[0] for column in columns])}) VALUES "
    value_statements = []
    for _ in range(10):
        value_statements.append(f"({', '.join([generate_default_value(column[1], column[2]) for column in columns])})")

    return insert_statement + ', '.join(value_statements) + ';'

def main():
    parser = argparse.ArgumentParser(description='Generate INSERT statements for a specified PostgreSQL or MySQL table.')
    parser.add_argument('--dbtype', help='The type of the database. Can be either "mysql" or "pg".', required=True)
    parser.add_argument('--dbname', help='The name of the database.', required=True)
    parser.add_argument('--user', help='The username to connect to the database.', required=True)
    parser.add_argument('--password', help='The password to connect to the database.', required=True)
    parser.add_argument('--host', help='The host of the database.', required=True)
    parser.add_argument('--port', help='The port of the database.', default='5432')
    parser.add_argument('--table', help='The name of the table.', required=True)

    args = parser.parse_args()

    if args.dbtype == 'pg':
        connection = psycopg2.connect(
            dbname=args.dbname,
            user=args.user,
            password=args.password,
            host=args.host,
            port=args.port
        )
        try:
            print(generate_insert_statements_pg(connection, args.table))
        finally:
            connection.close()

    elif args.dbtype == 'mysql':
        connection = mysql.connector.connect(
            database=args.dbname,
            user=args.user,
            password=args.password,
            host=args.host,
            port=args.port
        )
        try:
            print(generate_insert_statements_mysql(connection, args.table))
        finally:
            connection.close()

    else:
        raise ValueError(f"Invalid dbtype {args.dbtype}. It must be either 'pg' for PostgreSQL or 'mysql' for MySQL.")

if __name__ == "__main__":
    main()
