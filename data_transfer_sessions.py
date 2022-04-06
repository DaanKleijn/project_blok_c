import psycopg2.extras
import psycopg2.errors
import MongoDB.connect_mongodb as mdb_c
import PostgreSQL.connect_postgresql_database as sql_c
import transfer_functions as shared
import time
import load_data_sql as sql_l

# TODO: save compiled sql insert statement before exiting # TODO: save compiled sql insert statement before exiting code
# TODO: compile (ddl?) file to work around memory problem and still execute in one go. (or find better solution)
# TODO: and compress for more speedy execution (maybe?)


# queries
def create_session_query():
    """
    Creates an sql query to insert the following data in the sessions table:
    - session_id
    - profile_id
    - session end
    Returns this query.
    Products that have been viewed and bought during a single session will only be recorded under 'bought'
    """
    return """
    INSERT INTO sessions (session__id, profile__id, session_end) 
    
    VALUES (%s, %s, %s);
    """


def create_event_products_query():
    """
    Creates an sql query to insert the following data in the ordered_products table:
    - session_id
    - product_id
    Returns this query.
    """
    # source where exists/for share clause: Erwin Brandstetter
    # https://dba.stackexchange.com/questions/252875/how-to-make-on-conflict-work-for-compound-foreign-key-columns
    return """INSERT INTO event_products (session__id, product__id, event_type) 
                   SELECT ep.*
                   FROM  (VALUES (%s, %s, %s)) ep(session__id, product__id, event_type)
                
                   WHERE  EXISTS (
                   SELECT FROM products p                                 
                   WHERE p.product__id = ep.product__id 
                   FOR    SHARE)
                   ON CONFLICT DO NOTHING;
                   """


# fetch values
def get_session_values(session, profile_id):
    """
    Takes session_data (dict) and profile_id (str) as input.
    Selects the following data from the session:
    - session_id
    - session end
    Returns these values together with the profile_id (tuple).
    """
    wanted_values = (str(session['_id']),
                     profile_id,
                     session['session_end'])

    return wanted_values


def all_values_session(session, profile_id):
    """
    Takes a profile (dict) and the active sql_cursor as input.

    Selects where present the wanted data from the profile.
    Wanted data is data we want to upload to the following sql tables:
    - sessions
    - event (viewed or ordered) products (if present)

    Returns session_values, event__products_values, (tuple) ([], [])
    """
    events = shared.secure_dict_fetch(session, 'events')
    if not events:
        return (list(),) * 2

    # creates the lists we are going to fill and return
    session_values = [get_session_values(session, profile_id)]  # fetches session values
    event_products = list()

    session_id = session_values[0][0]

    # selects order values for every order associated with the session. Adds them to the order value list
    order = shared.secure_dict_fetch(session, 'order')
    if order:
        for product in order['products']:
            product_id = product['id']
            event_products.append((session_id, product_id, 'ordered'))

    # selects event values for every event associated with the session. Adds them to the event value list
    for event in events:
        viewed_product_id = shared.secure_dict_fetch(event, 'product')
        if viewed_product_id:
            event_products.append((session_id, viewed_product_id, 'viewed'))

    return session_values, event_products


# upload
def upload_session(session):
    """
    Takes an active sql_cursor and a session (dict) as input.
    Creates several sql queries to upload the profile data to the following sql tables:
    - sessions
    - event (viewed or ordered) products (if present)
    Executes the sql queries.
    """
    # skips the sessions if there are no events linked to the session.
    sql_connection, sql_cursor = sql_c.connect()
    # creates queries for tables
    session_query = create_session_query()
    event_products_query = create_event_products_query()

    profile_id_query = sql_l.profile_id_buid_query()
    buid = shared.secure_dict_fetch(dict(session), 'buid')
    # doesn't do anything if there is no associated buid.
    if not buid:
        return None
    # extracts buid from (nested) lists
    while isinstance(buid, list):
        buid = buid[0]
    sql_cursor.execute(profile_id_query.format(str(buid)))
    try:
        profile_id = sql_cursor.fetchone()[0]
    except TypeError:
        return None
    session_values, event_products_values = all_values_session(session, profile_id)

    sql_cursor.execute(session_query, session_values)
    sql_cursor.execute(event_products_query, event_products_values)
    sql_connection.commit()

    sql_c.disconnect(sql_connection, sql_cursor)


def upload_all_sessions():
    """Loads all sessions from the local mongodb database. Uploads the sessions to the local sql database."""
    start_time = time.time()
    database = mdb_c.connect()
    session_collection = database.sessions
    sql_connection, sql_cursor = sql_c.connect()
    print('busy')

    # creates queries for tables
    session_query = create_session_query()
    event_products_query = create_event_products_query()

    session_values = list()
    event_product_values = list()

    # fetches data to put into all tables for all documents and loads this into the cursor
    for session in session_collection.find():
        profile_id_query = sql_l.profile_id_buid_query()
        buid = shared.secure_dict_fetch(dict(session), 'buid')
        # doesn't do anything if there is no associated buid.
        if not buid:
            continue
        # extracts buid from (nested) lists
        while isinstance(buid, list):
            buid = buid[0]
        sql_cursor.execute(profile_id_query.format(str(buid)))
        try:
            profile_id = sql_cursor.fetchone()[0]
        # indexing returns TypeError when cursor returns None instead of list
        except TypeError:
            continue
        temp_session_values, temp_event_products_values = all_values_session(session, profile_id)
        if not temp_session_values:
            continue
        print(temp_session_values[0][0][:5])
        session_values += temp_session_values
        event_product_values += temp_event_products_values

    print('Data is compiled')

    psycopg2.extras.execute_batch(sql_cursor, session_query, session_values, page_size=10000)
    print('Sessions table has been updated')
    psycopg2.extras.execute_batch(sql_cursor, event_products_query, event_product_values, page_size=10000)
    print('Event products table has been updated')
    sql_connection.commit()
    print('\nData is committed')
    sql_c.disconnect(sql_connection, sql_cursor)

    return time.time() - start_time


if __name__ == '__main__':
    print('upload took {:.1f} minutes'.format(upload_all_sessions() / 60))
