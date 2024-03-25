from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/register")
def all_person_page():
    return render_template("all_person.html")

# @app.route("/register/<name>")
    # return ??

if __name__ == "__main__":
    app.run(debug=True)



