from flask import Flask, render_template, request, redirect, url_for
import db_functions as db_f

app = Flask(__name__)





def dont_run():
    @app.route('/books', methods=['GET'])
    def books_get():
        booksData = db_f.get_books()
        return booksData

    @app.route('/books', methods=["POST"])
    def books_add_to_db():
        data = request.args   ;print((dict(data)))
        try:
            title, author, year, genre, summary = (dict(data)).values()
            db_f.add_books(title, author, year, genre, summary)
            return f"Record added to database successfully, with following:\n {dict(data)}"
        except:
            return 'Empty values. All params are needed: title, author, year, genre, summary'
        # ? try to return a list with string for postman and render_template

    @app.route('/books/<book_id>', methods=['PUT'])
    def book_id_update(book_id):
        data = request.args   #;print((dict(data)))
        print(list(data.values()))
        if list(data.values()).count('')==0:
            title, author, year, genre, summary = (dict(data)).values()
            db_f.update_books(book_id, title, author, year, genre, summary)
            return f"Record added to database successfully, with following:\n {dict(data)}"
        else:
            return 'Empty values. All params are needed: title, author, year, genre, summary'

if __name__ == "__main__":
    app.run(debug=True)
