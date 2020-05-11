import psycopg2
from psycopg2.extras import RealDictCursor

POSTGRESQL_CONNECTION = "host=localhost dbname=umkm user=postgres password="

def execute(query):
    ps_conn = psycopg2.connect(POSTGRESQL_CONNECTION)
    ps_cursor = ps_conn.cursor()
    ps_cursor.execute(query)
    ps_conn.commit()
    ps_conn.close()
    return True

def update(dict_query):

    ps_conn = psycopg2.connect(POSTGRESQL_CONNECTION)
    ps_cursor = ps_conn.cursor()
    update_query = ''
    for key, value in dict_query['data'].items():
        if isinstance(value, str):
            value = "'"+value+"'"
        else:
            value = str(value)
        # isinstance(s, str)
        update_query +=key +' = '+value+','

    update_query = update_query[:-1]
    query = 'update '+dict_query['table']+' set '+ update_query +' where '+dict_query['condition']
    ps_cursor.execute(query)
    ps_conn.commit()
    ps_conn.close()
    return True

def insert(query):
    ps_conn = psycopg2.connect(POSTGRESQL_CONNECTION)
    ps_cursor = ps_conn.cursor()
    final_query = query+' RETURNING id'
    ps_cursor.execute(final_query)
    ps_conn.commit()
    id_of_new_row = ps_cursor.fetchone()[0]
    ps_conn.close()
    return id_of_new_row


def fetchall(query):
    ps_conn = psycopg2.connect(POSTGRESQL_CONNECTION)
    ps_cursor = ps_conn.cursor(cursor_factory=RealDictCursor)
    ps_cursor.execute(query)
    my_record = ps_cursor.fetchall()
    ps_conn.close()
    return my_record

def fetch(query):
    ps_conn = psycopg2.connect(POSTGRESQL_CONNECTION)
    ps_cursor = ps_conn.cursor(cursor_factory=RealDictCursor)
    ps_cursor.execute(query)
    my_record = ps_cursor.fetchone()
    ps_conn.close()
    return my_record

