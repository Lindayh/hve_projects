from flask import Flask, request, redirect, url_for
from .db_functions import *
import requests

app = Flask(__name__)

def print_body(func):
    def wrapper():
        func_output = func()
        if isinstance(func_output, dict):
            print(f"Json data received: \n{func_output}") 
            return f'Record added successfully, with following: \nTitle: {func_output['title']}\nAuthor: {func_output['author']}\nYear: {func_output['year']}\nGenre: {func_output['genre']} \nSummary: {func_output['summary']}'
        else:
            return func_output
        
    return wrapper


@app.route('/')
def root():
    return 'Welcome!'

# region /books

# 1. GET /books - Hämtar alla böcker i databasen + filter med URL                 
# + returnerar också det genomsnittliga betyget för böckerna/boken
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

            if filtered_books == []:
                return 'Search returned no results.'
            else:
                return filtered_books
        else:
            return 'Invalid filter terms. Terms accepted: "title", "author", "year", "genre"'

    return books_with_avg


# 2. POST /books - Lägger till en eller flera böcker i databasen.  
# @app.route('/books', methods=["POST"])
@app.route('/books', methods=["POST"])
@print_body
def books_add_to_db():

    if request.json:
        data = request.json   #;print(list(data.keys()))
        if list(data.keys()) == ['title', 'author', 'year', 'genre', 'summary']:
            if list(data.values()).count('')==0:
                title, author, year, genre, summary = (dict(data)).values()
                add_books(title, author, year, genre, summary)

                
                return request.json
            else:
                return f'Empty values.'
        else:
            return 'Empty or wrong params. Expected keys: "title", "author", "year", "genre", "summary"'
    else:
        return 'Empty values. Expected keys: "title", "author", "year", "genre", "summary"'
    

# 3. GET /books/{book_id} -Hämtar en enskild bok.
# + avg rating
@app.route('/books/<book_id>', methods=['GET'])
def book_id_show(book_id):
    print (type (book_id))
    try:
        book_id = int(book_id)
        book_with_avg = run_query(f""" SELECT b.book_ID, b.title, b.author, b.year, b.genre, b.summary, round(avg(r.rating),2) as "avg_rating"
                                    FROM book b
                                    LEFT JOIN review r USING (book_ID)
                                    WHERE b.book_ID LIKE {book_id}
                                    GROUP BY b.title
                                    ORDER BY b.book_ID    """) 
        if book_with_avg == []:
            return "No book with such ID."
        else:
            return book_with_avg
    except ValueError:
        return 'Invalid ID.'


# 4. PUT /books/{book_id} - Uppdaterar boken på databasen
@app.route('/books/<int:book_id>', methods=['PUT'])
def book_id_update(book_id):
    if request.json:

        data = request.json      
        data_keys= data.keys()          ;print(list(data_keys))
        book_keys = ['title', 'author','year', 'genre', 'summary']           ;print(list(data_keys) == book_keys)

        # Kolla om book_ID existerar i db:n
        query = f""" SELECT * FROM book WHERE book_ID LIKE {book_id}
        """
        print(len(run_query(query)))
        if len(run_query(query)) == 0:
            return "No book with such id."

        if list(data_keys) == book_keys and list(data.values()).count('') == 0:
            try:
                title, author, year, genre, summary = (dict(data)).values()
                update_books(book_id, title, author, year, genre, summary)
                return f"Record updated successfully, with following:\n {dict(data)}"
            except:
                return 'Empty values. All params are needed: "title", "author", "year", "genre", "summary"'
        else:
            return f'Invalid keys or values. Expected keys: "title", "author", "year", "genre", "summary".'
    return 'Empty values. Expected keys: "title", "author", "year", "genre", "summary".'   


# 5. DELETE /books/{book_id} -Tar bort en enskild bok
@app.route('/books/<book_id>', methods=['DELETE'])
def book_delete_by_id(book_id):
    delete_books(book_id)

    data = run_query(f"""SELECT * FROM book WHERE book_ID LIKE {book_id}""")
    if data == []:
        return f'No book with such ID.'
    else:
        return f"Book with ID {book_id} was removed from the database."
 
# endregion

# region /reviews

    
# 6. POST /reviews - Lägger till en ny recension till en bok.
@app.route('/reviews', methods=["POST"])
def add_reviews():

    if request.json:
        data = request.json  #;print(list(data.keys()))

        if list(data.keys()) == ["user", "book_ID", "rating", "description"]:
            user, book_ID, rating, description = (dict(data)).values()
            print(data)
            if data['user'] == '':
                return f'Username missing.'
            elif data['description'] == '':
                return f'Description missing.'
            return add_review(user, book_ID, rating, description)
        else:
            return f'Invalid or missing keys. Expected keys: "user", "book_ID", "rating", "description"'
    else:
        return 'Missing keys. Expected keys: "user", "book_ID", "rating", "description"'
    

# 7. GET /reviews - Hämtar alla recensioner som finns i databasen
@app.route('/reviews', methods=["GET"])
def show_reviews():
    reviews = show_all_reviews()
    return reviews


# 8. GET /reviews/{book_id} -Hämtar alla recensioner för en enskild bok.
@app.route('/reviews/<int:book_id>', methods=["GET"])
def review_by_ID(book_id):
    reviews = show_review_by_id(book_id)
    print(len(reviews))
    if len(reviews) == 0:
        return f'No reviews for this book.'
    return reviews
# endregion

# region top + author


# 9. GET /books/top -Hämtar de fem böckerna med högst genomsnittliga recensioner.
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

# 10. GET /author -Hämtar en kort sammanfattning om författaren och författarens mest kända verk. Använd externa API:er för detta.
@app.route('/author', methods=["GET"])
def get_authors_API():

    if request.json:
        body = request.json

        if list(request.json.values()) == [''] or list(request.json.keys()) == ['']:
            return 'Empty value or key.'
        else:
            search_value = list(request.json.values())
            search_key = list(request.json.keys())

            if list(request.json.keys()) == ['author']:
                try:
                    search_value = (list(request.json.values()) )  #;print(search_value)
                
                    # Author bio
                    url = f'https://openlibrary.org/search/authors.json?q={search_value}'
                    response = requests.get(url)            
                    data = response.json()
                    key = data['docs'][0]['key']                #;print(key)
                    name = (data['docs'][0]['name'])            #;print(name)

                    url = f'https://openlibrary.org/authors/{key}.json'
                    response = requests.get(url)            
                    data = response.json()

                    if isinstance(data['bio'], str):        # Struktur är olika beroende på författaren
                        bio = data['bio']  
                    else:
                        bio = data['bio']['value']               

                    result = {'name':name, 'bio':bio}

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

# endregion 

if __name__ == "__main__":
    app.run(debug=True)








