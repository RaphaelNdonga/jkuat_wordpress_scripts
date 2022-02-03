#!bin/env python
import re
import mysql.connector
from mysql.connector import Error

EXECQUERY = """
UPDATE wp_users SET user_pass = MD5(12345678) WHERE user_login = 'ibr';
"""
# READQUERY = """
# show databases ;
# """
READQUERY = """
select table_schema as database_name from information_schema.tables
where table_type = 'BASE TABLE'
      and table_schema not in ('information_schema', 'sys',
                               'performance_schema', 'mysql')
group by table_schema
order by table_schema;
"""

DATABASES = []


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
    connection = create_server_connection(
        "localhost", "developer", "dev", "information_schema"
    )
    # execute_query(connection, EXECQUERY)
    results = read_query(connection, READQUERY)
    for result in results:
        DATABASES.append(list(result)[0])
    print(DATABASES)

    for i in DATABASES:
        exec_query = f"UPDATE {i}.wp_users SET user_pass = MD5(12345678) WHERE user_login = 'developer';"
        execute_query(connection, exec_query)


main()
