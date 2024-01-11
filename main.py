from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def root():
    return render_template("base.html")

@app.route('/books')
def books():
    return 'List of all the books from the db'
    

# @app.route('books/<search>')


# @app.route('/books',  methods=["GET", "POST"])


if __name__ == "__main__":
    app.run(debug=True)