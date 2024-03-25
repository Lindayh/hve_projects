from flask import Flask, render_template
from db_func import run_query

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/register")
def all_person_page():

    query = "SELECT * FROM person"
    data = run_query(query)

    return render_template("all_person.html", data=data)

@app.route("/register/<id>", methods=['GET'])
def pers_info(id):
    query = f"SELECT * FROM person WHERE personID like {id}"
    data = run_query(query)

    print(data[0])

    return render_template("pers_info.html", data=data[0])


if __name__ == "__main__":
    app.run(debug=True)



