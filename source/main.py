from flask import Flask, render_template
import db_functions as db_f

app = Flask(__name__)

@app.route('/')
def root():
    return render_template("base.html", title='Book Reviews', h1_text='Welcome !')

@app.route('/books')
def books():
    data = db_f.get_books()
    return render_template("base.html", title='Book Reviews', h1_text='Books list', data=data)
    

# @app.route('books/<search>')


# @app.route('/books',  methods=["GET", "POST"])


if __name__ == "__main__":
    app.run(debug=True)