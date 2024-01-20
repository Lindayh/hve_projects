from flask import Flask, render_template, request, redirect, url_for
from db_functions import run_query
import asyncio
import requests
import time

import asyncio


app = Flask(__name__)

def dont_run():
    @app.route('/books', methods=['GET'])
    def books_get():
        booksData = run_query(""" SELECT * FROM book """)   
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
        data = run_query(query)
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

    @app.route('/books', methods=['GET'])
    def books():
        books_with_avg = run_query(f""" SELECT b.book_ID, b.title, b.author, b.year, b.genre, b.summary, round(avg(r.rating),2) as "avg_rating"
                                        FROM book b
                                        LEFT JOIN review r USING (book_ID)
                                        GROUP BY b.title
                                        ORDER BY b.book_ID
                                        """)

        if request.args:                    # filter
            filtered_books = []
            args = request.args                  
            args_keys = set(args.keys())        
            args_values = set(args.values())
            valid_keys = set({'title','author', 'year', 'genre'})     

            if args_keys.issubset(valid_keys):      
                for index, value in enumerate(books_with_avg):
                    if args_values.issubset(set(value.values())):
                        filtered_books.append(value)
                return filtered_books
            else:
                return 'Invalid filter terms. Terms accepted: "title", "author", "year", "genre"'

        return books_with_avg


@app.route('/author', methods=["GET"])
async def get_author_info_API():
    try:
        author = request.json['author']
        print(f"Getting author's info")
        
        loop = asyncio.get_event_loop()
        works_task = loop.create_task(get_works_API(author))
        bio_task = loop.create_task(get_bio_API())
        

        # Wait for both tasks to complete
        await asyncio.gather(bio_task, works_task)

        # Combine the results and return
        result = {'author': bio_task.result()['name'],'bio': bio_task.result()['bio'], 'top_works': works_task.result()}
        return result

    except KeyError:
        return 'No author provided in the request.'
    except Exception as e:
        return f'Error: {str(e)}'


async def get_works_API(author):
    print('Getting works info')
    author = request.json['author']         ;print(author)

    response = requests.get(f'https://openlibrary.org/search.json?author={author}&sort=rating')                   
    works = response.json()['docs']
    
    top_3_works = [ works[0]['title'], works[1]['title'], works[2]['title'] ]       ;print(top_3_works) 

    return top_3_works  

async def get_bio_API():
    if request.json:
        body = request.json

        if list(request.json.values()) == [''] or list(request.json.keys()) == ['']:
            return 'Empty value or key.'
        else:
            search_value = list(request.json.values())

            if list(request.json.keys()) == ['author']:
                try:
                    search_value = list(request.json.values())  # ;print(search_value)

                    # Author bio
                    url = f'https://openlibrary.org/search/authors.json?q={search_value}'
                    response = requests.get(url)
                    data = response.json()
                    key = data['docs'][0]['key']  # ;print(key)
                    name = data['docs'][0]['name']  # ;print(name)

                    url = f'https://openlibrary.org/authors/{key}.json'
                    response = requests.get(url)
                    data = response.json()

                    if isinstance(data['bio'], str):  # Struktur är olika beroende på författaren
                        bio = data['bio']
                    else:
                        bio = data['bio']['value']

                    result = {'name': name, 'bio': bio}

                    print(f'Data received: {body}')
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
    
# async that waits for input
    # > connect to final url
    # > await input ?

if __name__ == "__main__":
    app.run(debug=True)





    

 




    



    

    




