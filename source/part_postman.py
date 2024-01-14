from flask import Flask, render_template, request, redirect, url_for
import db_functions as db_f

app = Flask(__name__)

# region done

# @app.route('/books', methods=['GET'])
# def books_get():
#     booksData = db_f.get_books()
#     return booksData

# @app.route('/books', methods=["POST"])
# def books_add_to_db():
#     data = request.args   ;print((dict(data)))
#     try:
#         title, author, year, genre, summary = (dict(data)).values()
#         db_f.add_books(title, author, year, genre, summary)
#         return f"Record added to database successfully, with following:\n {dict(data)}"
#     except:
#         return 'Empty values. All params are needed: title, author, year, genre, summary'
#     # ? try to return a list with string for postman and render_template

# @app.route('/books/<book_id>', methods=['PUT'])
# def book_id_update(book_id):
#     data = request.args   #;print((dict(data)))
#     print(list(data.values()))
#     if list(data.values()).count('')==0:
#         title, author, year, genre, summary = (dict(data)).values()
#         db_f.update_books(book_id, title, author, year, genre, summary)
#         return f"Record added to database successfully, with following:\n {dict(data)}"
#     else:
#         return 'Empty values. All params are needed: title, author, year, genre, summary'
    
# # POST /reviews - Lägger till en ny recension till en bok.
# @app.route('/reviews', methods=["POST"])
# def add_reviews():
#     data = request.args   #;print((dict(data)))  ;print((dict(data)).values())

#     if list(data.values()).count('')==0:
#         user, book_ID, rating, description = (dict(data)).values()
#         print(user, book_ID, rating, description)
#         return db_f.add_review(user, book_ID, rating, description)
#     else:
#         return f'Empty values. All params are needed: user, book_ID, rating, description'

# GET /reviews - Hämtar alla recensioner som finns i databasen
# @app.route('/reviews', methods=["GET"])
# def show_reviews():
#     reviews = db_f.show_reviews()
#     return reviews

# GET /reviews/{book_id} -Hämtar alla recensioner för en enskild bok.
# @app.route('/reviews/<int:book_id>', methods=["GET"])
# def review_by_ID(book_id):
#     reviews = db_f.show_review_by_id(book_id)
#     print(len(reviews))
#     if len(reviews) == 0:
#         return f'No reviews for this book.'
#     return reviews

# endregion





# * Notes: Error handling if bs keys are written from postman.

if __name__ == "__main__":
    app.run(debug=True)
