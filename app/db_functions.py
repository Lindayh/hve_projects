import sqlite3
from sqlite3 import IntegrityError

def add_books(title, author, year, genre, summary):
    with sqlite3.connect('app/bookReviews.db') as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        query = f""" INSERT INTO book (\"title\",\"author\",\"year\",\"genre\",\"summary\")
        VALUES
        (\"{title}\",\"{author}\",\"{year}\",\"{genre}\",\"{summary}\")
        """

        cursor.execute(query)
        connection.commit()

def update_books(id, new_title, new_author, new_year, new_genre, new_summary):
    with sqlite3.connect('app/bookReviews.db') as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        query = f"""UPDATE book 
            SET title=\"{new_title}\",author=\"{new_author}\", year=\"{new_year}\", genre=\"{new_genre}\", summary=\"{new_summary}\"
            WHERE book_ID LIKE {id}       """

        cursor.execute(query)
        connection.commit() 
        
def add_review(user, book_ID, rating, description):
    with sqlite3.connect('app/bookReviews.db') as connection:
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
                if rating > 5 or rating <= 0:
                    return "Invalid rating. Must be between 0 and 5."
            except ValueError:
                return "Invalid rating. Must be a number between 0 and 5."
            return f'Invalid book_ID. No book with such ID.'

def run_query(query):            
    with sqlite3.connect('app/bookReviews.db') as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute(query)
        connection.commit()

        data = [dict(row) for row in cursor.fetchall()]
    return data