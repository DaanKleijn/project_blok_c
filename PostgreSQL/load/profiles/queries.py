# This file is dedicated to queries, used to fetch profile information out of the SQL database.

def profile_id_buid_query():
    """
    Returns a query that selects the profile id associated with a buid.
    Uses new formatting because of an unfixed bug with the old style.
    """
    return """SELECT profile__id FROM buids WHERE buid = '{}'"""
