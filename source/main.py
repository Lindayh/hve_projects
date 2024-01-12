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
    
    return render_template("base.html", title='Book List', h1_text='Books list', data=booksData, extend_upper='You can filter by adding text to the url.<br>E.g. books?genre=Horror will show all Horror books.<br> books/5 will show the book with that specifid ID.')    


# POST /books -Lägger till en eller flera böcker i databasen.    ^^               
# @app.route('/books', methods=["POST"])
# def books_add_to_db():
#     # db_f.add_books()


# GET /books/{book_id} -Hämtar en enskild bok.              
@app.route('/books/<book_id>', methods=['GET','PUT'])
def book_id_show(book_id):
    data = db_f.get_books()
    if request.method=='GET':
        for index,value in enumerate(data):
            if book_id == str(value['book_ID']):
                temp = []
                temp.append(value)        
                return render_template("base.html", title='Book List', h1_text='Books list', data=temp, extend_input=True, extend_upper='You can use the form below to update the current book.')
            

    if request.method=='PUT':
        db_f.update_books(book_id)
        return render_template("base.html", title='Book List', h1_text='Books list', extend_input=' ')

    # return render_template("base.html", title='Book List', h1_text='Books list')
    return render_template("base.html", title='Book List', h1_text='Books list', extend_upper='Invalid book ID')





# DELETE /books/{book_id} -Tar bort en enskild bok
# @app.route('/books/<book_id>', methods=["DELETE"])
# endregion


# region /reviews

# POST /reviews -Lägger till en ny recension till en bok.
# GET /reviews - Hämtar alla recensioner som finns i databasen
# @app.route('/books/reviews', methods=["POST", "GET"])
# def books_reviews():
#     if request.method=='POST':
#     if request.method=='GET':

# GET /reviews/{book_id} -Hämtar alla recensioner för en enskild bok.
# @app.route('/books/reviews/<book_ID>', methods=["GET"])
# endregion


# GET /books/top -Hämtar de fem böckerna med högst genomsnittliga recensioner.
# @app.route('/books/reviews/top', methods=["GET"])


# GET /author -Hämtar en kort sammanfattning om författaren och författarens mest kända verk. Använd externa API:er för detta.
# @app.route('/books/author', methods=["GET"])



if __name__ == "__main__":
    app.run(debug=True)

    # booksData = db_f.get_books()








        