import psycopg2
from psycopg2 import sql
"""
connects to database and display datatype inside it

result of running the file:
Table: coordonnee
Column Name             Data Type
---------------------------------
id                      integer
longitude                       real
latitude                        real
ip                      character varying
date                    date
"""

def create_user_and_connect_to_db():
    dbname = "coords"
    user = "cytech"
    password = 'password'
    host = "localhost"  # Change if your database is on a different host
    port = "5432"  # Change if your PostgreSQL is running on a different port
    # Establish a connection to the database
    connection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

    return connection

def display_database(connection):
    # Create a cursor object to interact with the database
    cursor = connection.cursor()

    # Fetch the column names and data types for the "coordonnee" table
    table_name = "coordonnee"
    cursor.execute(
        sql.SQL("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = %s;"),
        [table_name]
    )
    columns_info = cursor.fetchall()

    # Print information about the table structure
    print(f"Table: {table_name}")
    print("Column Name\t\tData Type")
    print("---------------------------------")
    for column_info in columns_info:
        print(f"{column_info[0]}\t\t\t{column_info[1]}")

    # Close the cursor and connection
    cursor.close()
    connection.close()

if __name__ == '__main__':
    connection = create_user_and_connect_to_db()
    display_database(connection)