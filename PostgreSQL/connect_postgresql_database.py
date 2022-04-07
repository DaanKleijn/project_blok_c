import psycopg2


def connect():
    """Connects to the local PostgreSQL database."""
    connection = None

    try:
        # establishes the  database connection
        connection = psycopg2.connect(host='localhost',
                                      database='huwebshop',
                                      user='postgres',
                                      password='postgres',
                                      port=5432
                                      )

        # creates cursor
        cursor = connection.cursor()
        return connection, cursor

    # raises exceptions
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return error


def disconnect(connection, cursor):
    """Takes an active cursor and connection with a PostgreSQL database as input. Closes the cursor and connection."""
    cursor.close()
    connection.close()
