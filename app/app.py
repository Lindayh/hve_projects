from flask import Flask, render_template, request, redirect, url_for
import db_functions as db_f
import requests
from sqlite3 import OperationalError

app = Flask(__name__)

# FIXME - HTML stuff
@app.route('/')
def root():
    return 'Hey'

# region /books

# LINK POST /books - Lägger till en eller flera böcker i databasen.  
@app.route('/books', methods=["POST"])
def books_add_to_db():

    if request.json:
        data = request.json   #;print(list(data.keys()))
        if list(data.keys()) == ['title', 'author', 'year', 'genre', 'summary']:
            title, author, year, genre, summary = (dict(data)).values()
            db_f.add_books(title, author, year, genre, summary)
            return f"Record added to database successfully, with following:\n {dict(data)}"
        else:
            return 'Empty or wrong params. Expected keys: "title", "author", "year", "genre", "summary"'
    else:
        return 'Empty values. Expected keys: "title", "author", "year", "genre", "summary"'

# FIXME Remove part for html 
# GET /books - Hämtar alla böcker i databasen + filter med URL (=args)
@app.route('/books', methods=['GET'])
def books():
    booksData = db_f.get_books()

    if request.args:
        args = dict(request.args)
        key = (list(args.keys()))[0]
        value = (list(args.values()))[0]

        try:
            query = f"""  SELECT * FROM book
            WHERE {key} LIKE \'{value}\'
            """
            data = db_f.run_show_query(query)           ;print(len(data))
            if len(data) == 0 :
                return "Search returned no results."

            return data
        except:
            return 'Wrong key.'


    return booksData


# GET /books/{book_id} -Hämtar en enskild bok.
# PUT /books/{book_id} -Uppdaterar information om en enskild bok.
@app.route('/books/<book_id>', methods=['GET', 'POST'])
def book_id_show(book_id):
    data = db_f.get_books()
    temp = []

    # FIXME: To fix later: just do a query WHERE book_ID = book_id
    # + test if book_id is out of range
    if request.method=='GET':
        for index,value in enumerate(data):
                if book_id == str(value['book_ID']):
                    temp.append(value)

                    return render_template("base.html", title='Book List', h1_text='Books list', data=temp, book_input=True, extend_upper='You can use the form below to update the current book.', book_id=book_id)

    # FIXME - Remove later: if request.method=='POST':
    # HTML accepterar inte 'PUT' så fixade 'POST' som extra för att uppdatera boken från front-end
    if request.method=='POST':
        form_values = list((request.form).values())

        if form_values.count('')>0:
            print('Empty values')
        else:
            print(f"Updating book with ID {book_id}: {dict(request.form)}")
            title, author, year, genre, summary = (dict(request.form)).values()
            db_f.update_books(book_id,title, author, year, genre, summary)

        return redirect(url_for('book_id_show', book_id=book_id))

    return render_template("base.html", title='Book List', h1_text='Books list', data=temp, book_input=True, extend_upper='You can use the form below to update the current book.', book_id=book_id)

# DELETE /books/{book_id} -Tar bort en enskild bok
@app.route('/books/<book_id>', methods=['DELETE'])
def book_delete_by_id(book_id):
    db_f.delete_books(book_id)
    return f"Book with ID {book_id} was removed from the database."
    # ! VG: error/message if invalid index


# PUT /books/{book_id} - Uppdaterar boken på databasen
@app.route('/books/<int:book_id>', methods=['PUT'])
def book_id_update(book_id):
    if request.json:

        data = request.json      
        data_keys=request.json.keys()          ;print(list(data_keys))
        book_keys = ['title', 'author','year', 'genre', 'summary']           ;print(list(data_keys) == book_keys)

        # Kolla om book_ID existerar i db:n
        query = f""" SELECT * FROM book WHERE book_ID LIKE {book_id}
        """
        print(len(db_f.run_show_query(query)))
        if len(db_f.run_show_query(query)) == 0:
            return "No book with such id."

        if list(data_keys) == book_keys:
            try:
                title, author, year, genre, summary = (dict(data)).values()
                db_f.update_books(book_id, title, author, year, genre, summary)
                return f"Record updated successfully, with following:\n {dict(data)}"
            except:
                return 'Empty values. All params are needed: "title", "author", "year", "genre", "summary"'
        else:
            return f'Invalid keys. Expected keys: "title", "author", "year", "genre", "summary".'
    return 'Empty values. Expected keys: "title", "author", "year", "genre", "summary".'
    
# endregion


# region /reviews

# GET /reviews - Hämtar alla recensioner som finns i databasen
@app.route('/reviews', methods=["GET"])
def show_reviews():
    reviews = db_f.show_reviews()
    return reviews
    
# POST /reviews - Lägger till en ny recension till en bok.
@app.route('/reviews', methods=["POST"])
def add_reviews():
    data = request.args   

    if list(data.values()).count('')==0:
        user, book_ID, rating, description = (dict(data)).values()
        print(user, book_ID, rating, description)
        return db_f.add_review(user, book_ID, rating, description)
    else:
        return f'Empty values. All params are needed: user, book_ID, rating, description'


# GET /reviews/{book_id} -Hämtar alla recensioner för en enskild bok.
@app.route('/reviews/<int:book_id>', methods=["GET"])
def review_by_ID(book_id):
    reviews = db_f.show_review_by_id(book_id)
    print(len(reviews))
    if len(reviews) == 0:
        return f'No reviews for this book.'
    return reviews
    

# endregion

# GET /books/top -Hämtar de fem böckerna med högst genomsnittliga recensioner.
@app.route('/books/top', methods=["GET"])
def top_reviews():
    query = f""" SELECT review.book_ID, book.title, book.author, round(avg(review.rating),2) as 'Average review'
    FROM review
    INNER JOIN book ON book.book_ID like review.book_ID
    GROUP BY review.book_ID
    ORDER BY avg(review.rating) DESC
    LIMIT 5     """
    data = db_f.run_show_query(query)
    return data

# ! Current WIP
# -TODO- GET /author -Hämtar en kort sammanfattning om författaren och författarens mest kända verk. Använd externa API:er för detta.
@app.route('/author', methods=["GET"])
def get_authors_wikipedia():

    if list(request.args.keys()) == ['author']:
        if True:
            author = (list(request.args.values()) )  ;print(author)
            
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
            

            text = f'Author: {name}\nBiography: {bio}'

            return text
        
    else:
        return 'Invalid search term. Expected: author'
        

# -TODO- VG :
    # ● Samtliga endpoints är testade. Skriv gärna en kommentar om hur du resonerat när du designat testet. Kommentaren behöver bara vara 1 -2 rader.
    # ● Det finns en decorator som skriver ut vilken body varje request har i konsolen för utvalda requests, om det finns en body.
    # ● Varje endpoint ger användarvänliga felmeddelanden ifall input eller ett externt beroende fallerar.
    # ● GET /author hämtar information från API asynkront.
    # ● GET /books och /books/{book_id} returnerar också det genomsnittliga betyget för böckerna/boken.



if __name__ == "__main__":
    app.run(debug=True)

    # booksData = db_f.get_books()








