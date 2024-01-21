from flask import Flask, request
from .db_functions import *
import requests
import threading
import time
from queue import Queue

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

    try:
        book_id = int(book_id)
    except:
        return "Invalid ID. Must be a integer number."
        
    data = run_query(f"""SELECT * FROM book WHERE book_ID LIKE {book_id}""")
    if data == []:
        return f'No book with such ID.'
    else:
        # delete_books(book_id)
        run_query(f"DELETE FROM book WHERE book_ID LIKE {book_id}")
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
    reviews = run_query(""" SELECT review.reviewID, review.user, book.title, review.book_ID, review.rating, review.description
                            FROM review
                            INNER JOIN book ON book.book_ID like review.book_ID""")
    return reviews


# 8. GET /reviews/{book_id} - Hämtar alla recensioner för en enskild bok.
@app.route('/reviews/<book_id>', methods=["GET"])
def review_by_ID(book_id):

    try:
        book_id = int(book_id)
    except:
        return "Invalid ID. Must be a integer number."
    
    reviews = run_query(f"""SELECT review.reviewID, review.user, book.title, review.book_ID, review.rating, review.description
                        FROM review
                        INNER JOIN book ON book.book_ID like review.book_ID
                        WHERE review.book_ID LIKE {book_id}""")
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
@app.route('/author', methods=["GET"])
def multithreading():
    start = time.perf_counter()

    if request.json and list(request.json.keys())==['author'] and request.json['author']!='': 
        author = request.json['author']        

        q = Queue(maxsize=2)
        
        task_bio = threading.Thread(target=get_bio_API, args=(author, q,))
        task_works = threading.Thread(target=get_works_API, args=(author, q,))
        task_bio.start()
        task_works.start()
        task_bio.join()
        task_works.join()

        result = {}
        while q.empty() == False:
            result.update(q.get_nowait())    

        end = time.perf_counter()
        print(f'Time elapsed: {end-start}') 

        if list(result.values()).count('')>0:
            return f'Search term \'{author}\' returned no results.'
        else:
            return result
    else:
        return 'Invalid key or missing value. Exptected key: "author"'

def get_works_API(author, q):
    print('Getting works info.')

    try:
        response = requests.get(f'https://openlibrary.org/search.json?author={author}&sort=rating')                   
        works = response.json()['docs']
        
        top_3_works = {'top_works' : [work['title'] for work in works[:3]]}     

        print('Works search completed.')
        q.put(top_3_works) 
    except:
        q.put({'top_works': ''})


def get_bio_API(author, q):
    print(f"Getting author's info")

    try:
        url = f'https://openlibrary.org/search/authors.json?q={author}'
        response = requests.get(url)
        data = response.json()
        key = data['docs'][0]['key'] 
        name = data['docs'][0]['name'] 

        url = f'https://openlibrary.org/authors/{key}.json'
        response = requests.get(url)
        data = response.json()

        if isinstance(data['bio'], str):  # Struktur är olika beroende på författaren
            bio = data['bio']
        else:
            bio = data['bio']['value']

        print('Author\'s info search completed.')
        q.put({'name': name, 'bio': bio})
    except:
        q.put({'bio': ''})

# endregion 

if __name__ == "__main__":
    app.run(debug=True)








