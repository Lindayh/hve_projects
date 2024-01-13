from flask import Flask, render_template, request, redirect, url_for
import db_functions as db_f


app = Flask(__name__)

@app.route('/')
def root():
    return render_template("base.html", title='Book Reviews', h1_text='Welcome !') 

# region /books
# GET /books - Hämtar alla böcker i databasen. 
# Du ska kunna filtrera på titel, författare och/eller genre via en parameteri search-query. 
# Exempelvis: /books?genre=biography

# POST /books -Lägger till en eller flera böcker i databasen.    ^^               
# @app.route('/books', methods=["POST"])
# def books_add_to_db():
#     # db_f.add_books()
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
    
    return render_template("base.html", title='Book List', h1_text='Books list', data=booksData, extend_upper='You can filter by adding text to the url.<br>E.g. books?genre=Horror will show all Horror books.<br> books/5 will show the book with that specifid ID<br><br>You can add books to the database with the form below.')    



# GET /books/{book_id} -Hämtar en enskild bok.              
@app.route('/books/<book_id>', methods=['GET', 'POST'])
def book_id_show(book_id):
    data = db_f.get_books()
    temp = []   
    
    # To fix later: just do a query WHERE book_ID = book_id
    # + test if book_id is out of range 
    if request.method=='GET':
        for index,value in enumerate(data):
                if book_id == str(value['book_ID']):
                    temp.append(value)    

                    return render_template("base.html", title='Book List', h1_text='Books list', data=temp, book_input=True, extend_upper='You can use the form below to update the current book.', book_id=book_id)

    # PUT funkar inte med Jinja så fixade 'POST' som extra för att uppdatera boken från front-end
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
    


@app.route('/books/<book_id>', methods=['DELETE'])
def book_delete_by_id(book_id):
    print("DELETE method triggered")

    return redirect(url_for('book_id_show', book_id=book_id))

        # Steps: Check if query works
        # Check if method gets triggerred:
            # Connect the button in jinja   


            
    
# PUT method som uppdaterar boken på databasen med Postman
@app.route('/books/<book_id>', methods=['PUT'])
def book_id_update(book_id):
    data = request.args     ;print(data)
    title, author, year, genre, summary = 'WIP', 'WIP', 'WIP', 'WIP', 'WIP' 
    db_f.update_books(book_id,title, author, year, genre, summary)

    # return what?


    

            
    

    





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








        