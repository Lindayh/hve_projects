import sqlite3
from sqlite3 import IntegrityError

# *todo - Fix decorator?
def connect_db(func):
    connection = sqlite3.connect('source/bookReviews.db')
    cursor = connection.cursor()
    func()
    connection.close()

# region books functions
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

        query = f""" INSERT INTO book (\"title\",\"author\",\"year\",\"genre\",\"summary\")
        VALUES
        (\"{title}\",\"{author}\",\"{year}\",\"{genre}\",\"{summary}\")
        """
        print(query)

        cursor.execute(query)
        connection.commit()

def update_books(id, new_title, new_author, new_year, new_genre, new_summary):
    with sqlite3.connect('source/bookReviews.db') as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        query = f"""UPDATE book 
            SET title=\"{new_title}\",author=\"{new_author}\", year=\"{new_year}\", genre=\"{new_genre}\", summary=\"{new_summary}\"
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
# endregion
        
def add_review(user, book_ID, rating, description):
    with sqlite3.connect('source/bookReviews.db') as connection:
        # connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = 1")   # Tvinga foreign key integrity
        cursor = connection.cursor()
        try:
            query = f""" INSERT INTO review (\"user\", \"book_ID\", \"rating\", \"description\")
            VALUES
            (\"{user}\",\"{book_ID}\",\"{rating}\",\"{description}\")
            """
            cursor.execute(query)
            connection.commit()
            return f"Review added successfully with data: \n User: {user}\nBook_ID: {book_ID}\nRating: {rating}\nReview: {description}"   
        except IntegrityError:
            try:
                rating = int(rating)
                if rating > 5 or rating < 0:
                    return "Invalid rating. Must be between 0 and 5."
            except ValueError:
                return "Invalid rating. Must be a number between 0 and 5."
            return f'Invalid book_ID. No book with such ID.'
        
def show_reviews():
    with sqlite3.connect('source/bookReviews.db') as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        query = f"""SELECT review.reviewID, review.user, book.title, review.book_ID, review.rating, review.description
        FROM review
        INNER JOIN book ON book.book_ID like review.book_ID"""

        cursor.execute(query)
        connection.commit()

        reviews = [dict(row) for row in cursor.fetchall()]
    return reviews

def show_review_by_id(id):
    with sqlite3.connect('source/bookReviews.db') as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        query = f"""SELECT review.reviewID, review.user, book.title, review.book_ID, review.rating, review.description
        FROM review
        INNER JOIN book ON book.book_ID like review.book_ID
        WHERE review.book_ID LIKE {id}"""

        cursor.execute(query)
        connection.commit()

        reviews = [dict(row) for row in cursor.fetchall()]
    return reviews

def run_show_query(query):            
    with sqlite3.connect('source/bookReviews.db') as connection:
        cursor = connection.cursor()

        cursor.execute(query)
        connection.commit()

        data = cursor.fetchall()
    return data


    



if __name__=='__main__':
    placeholder = 'WIP'
    # books_data = update_books(7, 'title','author', 'year', 'genre', 'summary')

    # Connect the function to the button
    # Get the info from the form
    # title, author, year, genre, summary = 'WIP', 'WIP', 'WIP', 'WIP', 'WIP'
    # print(title, author, year, genre, summary )

    # print(add_review('Sakir The Cat', '55', '5', 'Meow Meow 5/5'))

    
    # print(run_show_query(query))


