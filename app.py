from flask import Flask, render_template, request
from db_func import run_query

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/register", methods=['GET'])
def all_person_page():
    query = "SELECT * FROM person"
    data = run_query(query)
    return render_template("all_person.html", data=data, searched=False)

@app.route("/register/<id>", methods=['GET'])
def pers_info(id):
    query = f"SELECT * FROM person WHERE personID like {id}"
    data = run_query(query)
    return render_template("pers_info.html", data=data[0])




@app.route("/register", methods=['GET', 'POST'])
def search_register():
    key = list(request.form.keys())[0]
    search_term = request.form.get(key)

    # TODO searching with ' breaks the query and the website
    query = f"SELECT * FROM person WHERE name LIKE '%{search_term}%'"
    data = run_query(query)

    if data != []:
        print(data)

        return render_template("all_person.html", searched_data=data, searched=True)
    else:
        return render_template("all_person.html", searched_data=data, searched=True)





if __name__ == "__main__":
    app.run(debug=True)



