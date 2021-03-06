#!bin/env python
import mysql.connector
from mysql.connector import Error

EXECQUERY = """
UPDATE wp_users SET user_pass = MD5(12345678) WHERE user_login = 'ibr';
"""

DB_QUERY = """
select table_schema as database_name from information_schema.tables
where table_type = 'BASE TABLE'
      and table_schema not in ('information_schema', 'sys',
                               'performance_schema', 'mysql')
group by table_schema
order by table_schema;
"""

DATABASES = []
USER_TABLES = []


def create_server_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name, user=user_name, passwd=user_password, database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print("error : ", err)
    return connection


def execute_query(connection, query):
    cursor = connection.cursor(buffered=True)
    try:
        cursor.execute(query)
        connection.commit()
        print("Query Successful!")
    except Error as err:
        print("error: ", err)


def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
    except Error as err:
        print("error: ", err)
    return result


def main():
    main_connection = create_server_connection(
        "localhost", "developer", "dev", "information_schema"
    )
    # read_query tends to return a list of tuples.

    db_query_results = read_query(main_connection, DB_QUERY)
    for db_query_result in db_query_results:
        DATABASES.append(db_query_result[0])
    print(DATABASES)

    for database in DATABASES:

        db_connection = create_server_connection(
            "localhost", "developer", "dev", database
        )
        user_tables_query = f"SELECT table_name from information_schema.tables WHERE table_name like '%users%' AND table_schema LIKE '{database}'"
        user_tables_query_results = read_query(main_connection, user_tables_query)
        for user_tables_query_result in user_tables_query_results:
            update_pass_query = f"UPDATE {database}.{user_tables_query_result[0]} SET user_pass = MD5(1234567) WHERE user_login = 'developer';"
            execute_query(db_connection, update_pass_query)


main()
