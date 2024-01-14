from flask import Flask, render_template, request, redirect, url_for
import db_functions as db_f


app = Flask(__name__)

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


if __name__ == "__main__":
    app.run(debug=True)
