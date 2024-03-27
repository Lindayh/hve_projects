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

@app.route("/register", methods=['GET', 'POST'])
def search_register():
    key = list(request.form.keys())[0]
    search_term = request.form.get(key)

    if "'" in search_term: search_term=search_term.replace("'", "''")
    
    try:
        query = f"SELECT * FROM person WHERE name LIKE '%{search_term}%'"
        data = run_query(query)
    except Exception as e:
        print(e)
        data = []

    if data != []:
        return render_template("all_person.html", searched_data=data, searched=True)
    else:
        return render_template("all_person.html", searched_data=data, searched=True)

@app.route("/register/<int:id>", methods=['GET'])
def pers_info(id):
    query = f"SELECT * FROM person WHERE personID like {id}"
    data = run_query(query)
    return render_template("pers_info.html", data=data[0])




@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_validation():
    form_pw, form_user = request.form["login_pw"], request.form["login_user"]    

    query = f"SELECT * FROM user WHERE username LIKE '{form_user}'"
    data = run_query(query)

    if data:
        data_pw, data_user = data[0]['password'], data[0]['username']

        if form_pw == data_pw:
            logged= True
            return render_template('home.html', logged = True)
        else: 
            return render_template("login.html", error="Wrong username or password!")
    else:
        return render_template("login.html", error="Wrong username or password!")
    


        




if __name__ == "__main__":
    app.run(debug=True)



