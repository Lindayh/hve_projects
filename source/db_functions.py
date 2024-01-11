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

        # book_data=cursor.fetchall()
        book_data = [dict(row) for row in cursor.fetchall()]
    return book_data



if __name__=='__main__':
    books_data = get_books()

    print(books_data[0])
