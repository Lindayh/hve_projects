import sqlite3


def connect_db(func):
    connection = sqlite3.connect('source/bookReviews.db')
    cursor = connection.cursor()
    func()
    connection.close()

def get_books():
    with sqlite3.connect('source/bookReviews.db') as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        query = f""" SELECT * FROM book """

        cursor.execute(query)
        connection.commit()

        book_data = [dict(row) for row in cursor.fetchall()]
    return book_data

def add_books(title, author, year, genre, summary):
    with sqlite3.connect('source/bookReviews.db') as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        query = f""" INSERT INTO book ('title','author','year','genre','summary')
        VALUES
        ('{title}','{author}','{year}','{genre}','{summary}')
        """
        print(query)

        cursor.execute(query)
        connection.commit()

def update_books(id, new_title, new_author, new_year, new_genre, new_summary):
    with sqlite3.connect('source/bookReviews.db') as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        query = f"""UPDATE book 
            SET title='{new_title}',author='{new_author}', year='{new_year}', genre='{new_genre}', summary='{new_summary}'
            WHERE book_ID LIKE {id}       """

        cursor.execute(query)
        connection.commit()

def delete_books(id):
 with sqlite3.connect('source/bookReviews.db') as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        query = f"""DELETE FROM book
            WHERE book_ID LIKE {id}       """

        cursor.execute(query)
        connection.commit()   


    



if __name__=='__main__':
    books_data = update_books(7, 'title','author', 'year', 'genre', 'summary')

    # Connect the function to the button
    # Get the info from the form
    # title, author, year, genre, summary = 'WIP', 'WIP', 'WIP', 'WIP', 'WIP'
    # print(title, author, year, genre, summary )


