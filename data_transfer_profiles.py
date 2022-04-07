import MongoDB.connect_mongodb as mdb_c
import PostgreSQL.connect_postgresql_database as sql_c
import transfer_functions as shared
import psycopg2.extras


# queries
def create_profile_query():
    """
    Creates an sql query to insert the following data into the profile table:
    - profile id
    - the latest activity
    Returns this query (str).
    """
    return """INSERT INTO profiles (profile__id, latest_activity) 
    VALUES (%s, %s);"""


def create_buid_query():
    """"""
    # doesn't insert duplicate buids. Some buids are associated with two profiles. We will only associate them with one
    # because otherwise we can't couple a session with a profile. Isn't perfect because some sessions will be associated
    # with the wrong profile. The other option was to throw them all away, which is worse in my opinion.
    return """INSERT INTO buids (buid, profile__id) 
    VALUES (%s, %s) ON CONFLICT DO NOTHING"""


# fetch values
def get_profile_values(profile):
    """
    Takes a profile (dict) as input.

    Selects where present the wanted data from the profile.
    Wanted data is data we want to upload to the following sql tables:
    - profile__id
    - last activity
    Returns the profile_values (tuple) (str, datetime)
    """
    return [(str(profile['_id']),
            shared.secure_dict_fetch(profile, 'latest_activity'))]


# upload
def upload_profile(profile):
    """
    Takes an active sql_cursor and profile-data (dict) as input.
    Creates several sql queries to upload the profile data to the following sql tables:
    - profiles
    - buid
    Executes the sql queries.
    """
    sql_connection, sql_cursor = sql_c.connect()
    # selects all wanted values from profile and puts them in a lists.
    # One list contains values to insert into one table in sql
    profile_values = get_profile_values(profile)
    # Does nothing if there are no buids associated with the profile
    buids = shared.secure_dict_fetch(profile, 'buids')
    if buids:
        profile_query = create_profile_query()
        sql_cursor.execute(profile_query, profile_values)
        # inserts recommendations if they present in the profile
        sql_connection.commit()

    sql_c.disconnect(sql_connection, sql_cursor)


def upload_all_profiles():
    """Loads all profiles from the local mongodb database. Uploads the profiles to the local sql database."""
    database = mdb_c.connect()
    profile_collection = database.profiles
    sql_connection, sql_cursor = sql_c.connect()

    # creates queries
    profile_query = create_profile_query()
    buid_query = create_buid_query()

    # creates a value list for every sql table.
    # We can add a tuple to these lists for every row we want to insert into the sql table.
    all_profile_values = list()
    all_buid_values = list()

    for profile in profile_collection.find():
        buids = shared.secure_dict_fetch(profile, 'buids')
        # skips all profiles without associated buid
        if not buids:
            continue
        # selects all wanted values from the profile.
        profile_value = get_profile_values(profile)

        for buid in buids:
            all_buid_values += [(buid, profile_value[0][0])]

        # adds fetched values to the bigger value lists.
        all_profile_values += profile_value


    print('Compiling complete')

    # executes the insert statement for each sql table.
    psycopg2.extras.execute_batch(sql_cursor,
                                  profile_query,
                                  all_profile_values,
                                  page_size=10000)
    print('Profiles table is updated')
    sql_connection.commit()
    print('Profiles table is committed')
    psycopg2.extras.execute_batch(sql_cursor,
                                  buid_query,
                                  all_buid_values,
                                  page_size=10000)
    print('Buid table is updated')
    sql_connection.commit()
    print('Buid table is committed')
    sql_c.disconnect(sql_connection, sql_cursor)


if __name__ == '__main__':
    upload_all_profiles()
