from flask import Flask, render_template, request, redirect, url_for
import db_functions as db_f
import asyncio
import requests

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

    # POST /reviews - Lägger till en ny recension till en bok.
    @app.route('/reviews', methods=["POST"])
    def add_reviews():
        data = request.args   #;print((dict(data)))  ;print((dict(data)).values())

        if list(data.values()).count('')==0:
            user, book_ID, rating, description = (dict(data)).values()
            print(user, book_ID, rating, description)
            return db_f.add_review(user, book_ID, rating, description)
        else:
            return f'Empty values. All params are needed: user, book_ID, rating, description'

    # GET /reviews - Hämtar alla recensioner som finns i databasen
    @app.route('/reviews', methods=["GET"])
    def show_reviews():
        reviews = db_f.show_reviews()
        return reviews

    # GET /reviews/{book_id} -Hämtar alla recensioner för en enskild bok.
    @app.route('/reviews/<int:book_id>', methods=["GET"])
    def review_by_ID(book_id):
        reviews = db_f.show_review_by_id(book_id)
        print(len(reviews))
        if len(reviews) == 0:
            return f'No reviews for this book.'
        return reviews

    # GET /books/top -Hämtar de fem böckerna med högst genomsnittliga recensioner.
    @app.route('/books/top', methods=["GET"])
    def top_reviews():
        query = f""" SELECT review.book_ID, book.title, book.author, round(avg(review.rating),2) as 'Average review'
        FROM review
        INNER JOIN book ON book.book_ID like review.book_ID
        GROUP BY review.book_ID
        ORDER BY avg(review.rating) DESC
        LIMIT 5     """
        data = db_f.run_query(query)
        return data

    # GET /author -Hämtar en kort sammanfattning om författaren och författarens mest kända verk. Använd externa API:er för detta.
    @app.route('/author', methods=["GET"])
    def get_authors_API():

        if request.json:

            if list(request.json.values()) == [''] or list(request.json.keys()) == ['']:
                return 'Empty value or key.'
            else:
                search_value = list(request.json.values())
                search_key = list(request.json.keys())

                if list(request.json.keys()) == ['author']:
                    try:
                        author = (list(request.json.values()) )  ;print(author)
                    
                        # Author bio
                        url = f'https://openlibrary.org/search/authors.json?q={author}'
                        response = requests.get(url)            
                        data = response.json()
                        key = data['docs'][0]['key']                ;print(key)
                        name = (data['docs'][0]['name'])            ; print(name)

                        url = f'https://openlibrary.org/authors/{key}.json'
                        response = requests.get(url)            
                        data = response.json()

                        if isinstance(data['bio'], str):        # Struktur är olika beroende på författaren
                            bio = data['bio']  
                        else:
                            bio = data['bio']['value']               

                        result = {'name':name, 'bio':bio}#f'Author: {name}\nBiography: {bio}'
                        return result
                    except IndexError:
                        return 'Empty value'
                    except KeyError:
                        return "Couldn't find any result with the search term provided."
                else:
                    return 'Wrong key. Expected: "author"'  
        else:
            return 'No key was given. Expected: "author"'

# * Notes: What to test =
    # * Invalid keys from postman.
    # * At the start of a func that needs args from postman -> check if args are present -> if request.args: ...
    # * Try before unpacking dictionary -> try:  var01, var02 = (dict(data)).values()
        # * ^ Should also solve any empty field -> not acceptable
    # ! * Error if ' are in the text from postman  -> \" instead of ' in queries


if __name__ == "__main__":
    app.run(debug=True)

    

 




    



    

    




