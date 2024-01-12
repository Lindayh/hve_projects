from flask import Flask, render_template, request
import db_functions as db_f


app = Flask(__name__)

@app.route('/')
def root():
    return render_template("base.html", title='Book Reviews', h1_text='Welcome !') 

# region /books
# GET /books - Hämtar alla böcker i databasen. 
# Du ska kunna filtrera på titel, författare och/eller genre via en parameteri search-query. 
# Exempelvis: /books?genre=biography
@app.route('/books', methods=['GET'])
def books():
    booksData = db_f.get_books()
    

    filtered_books = []

    if request.args:
        filter = dict(request.args)           
        filter = str(list(filter.values())[0])
        for index, value in enumerate(booksData):
            if filter in value.values():
                filtered_books.append(value)

        return render_template("base.html", title='Book List', h1_text='Books list', data=filtered_books)
    
    return render_template("base.html", title='Book List', h1_text='Books list', data=booksData)    



# if request.method == 'POST':

# POST /books -Lägger till en eller flera böcker i databasen.                 
# @app.route('/books', methods=["POST"])
# def books_add_to_db():
#     # db_f.add_books()


# GET /books/{book_id} -Hämtar en enskild bok.              
@app.route('/books/<book_id>', methods=["GET"])
def book_id_get(book_id):
    data = db_f.get_books()
    for index,value in enumerate(data):
        if book_id == str(value['book_ID']):
            temp = []
            temp.append(value)
            print(type(value['book_ID']))           ;print(type(temp))
            return render_template("base.html", title='Book List', h1_text='Books list', data=temp)

    # return render_template("base.html", title='Book List', h1_text='Books list')
    return render_template("base.html", title='Book List', h1_text='Books list', extend='Invalid book ID')


# PUT /books/{book_id} -Uppdaterar information om en enskild bok.
# @app.route('/books/<book_id>', methods=["PUT"])


# DELETE /books/{book_id} -Tar bort en enskild bok
# @app.route('/books/<book_id>', methods=["DELETE"])
# endregion


# region /reviews
# POST /reviews -Lägger till en ny recension till en bok.
# @app.route('/books/reviews', methods=["POST"])


# GET /reviews -Hämtar alla recensioner som finns i databasen
# @app.route('/books/reviews', methods=["GET"])


# GET /reviews/{book_id} -Hämtar alla recensioner för en enskild bok.
# @app.route('/books/reviews/<book_I>', methods=["GET"])
# endregion


# GET /books/top -Hämtar de fem böckerna med högst genomsnittliga recensioner.
# @app.route('/books/reviews/top', methods=["GET"])


# GET /author -Hämtar en kort sammanfattning om författaren och författarens mest kända verk. Använd externa API:er för detta.
# @app.route('/books/author', methods=["GET"])



if __name__ == "__main__":
    app.run(debug=True)

    # booksData = db_f.get_books()
    # filter = {'genre': 'Horror'}             # ;print(filter, type(filter))
    
    # filter = str(list(filter.values())[0])

    # filtered_books = []

    
    # for index, value in enumerate(booksData):
    #     # print(value)
    #     if filter in value.values():
    #         filtered_books.append(value)








        