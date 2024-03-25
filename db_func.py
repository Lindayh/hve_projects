import sqlite3

def run_query(query):            
    with sqlite3.connect('personalregister.db') as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute(query)
        connection.commit()

        data = [dict(row) for row in cursor.fetchall()]
    return data