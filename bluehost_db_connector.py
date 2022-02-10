#!bin/env python
import mysql.connector
from mysql.connector import Error

DATABASES = []
DB_QUERY = """
select table_schema as database_name from information_schema.tables
where table_type = 'BASE TABLE'
      and table_schema not in ('information_schema', 'sys',
                               'performance_schema', 'mysql')
group by table_schema
order by table_schema;
"""

BLUE_HOST_IP = "198.1.75.23"


def main():
    bh_user_name = input("Enter bluehost user name: ")
    bh_password = input("Enter bluehost password: ")

    wordpress_user_name = input("User name of the wordpress user: ")
    new_wordpress_pass = input("New Password: ")
    main_connection = create_server_connection(
        BLUE_HOST_IP, bh_user_name, bh_password, "information_schema"
    )
    db_query_results = read_query(main_connection, DB_QUERY)
    for db_query_result in db_query_results:
        DATABASES.append(db_query_result[0])
    print(DATABASES)

    for database in DATABASES:

        db_connection = create_server_connection(
            BLUE_HOST_IP, bh_user_name, bh_password, database
        )
        user_tables_query = f"SELECT table_name from information_schema.tables WHERE table_name like '%users%' AND table_schema LIKE '{database}'"
        user_tables_query_results = read_query(main_connection, user_tables_query)
        for user_tables_query_result in user_tables_query_results:
            update_pass_query = f"UPDATE {database}.{user_tables_query_result[0]} SET user_pass = MD5('{new_wordpress_pass}') WHERE user_login = '{wordpress_user_name}';"
            execute_query(db_connection, update_pass_query)


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


def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
    except Error as err:
        print("error: ", err)
    return result


def execute_query(connection, query):
    cursor = connection.cursor(buffered=True)
    try:
        cursor.execute(query)
        connection.commit()
        print("Query Successful!")
    except Error as err:
        print("error: ", err)


main()
