from flask import Flask, render_template, request, session
from db_func import run_query
import os
from dotenv import load_dotenv
from flask_migrate import Migrate, upgrade

from SQLAlchemy_test import db, Person, seed_data


load_dotenv()
app = Flask(__name__)

app.secret_key = "psst"

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URI_LOCAL")
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db.init_app(app)

migrate = Migrate(app, db)


# TODO log status into decorator?
def loggedin_check():
    if session:
        log_status = session['logged']
        return log_status
    else:
        log_status = False
        return log_status

@app.route("/")
def home():
    log_status = loggedin_check()
    return render_template('home.html', logged= log_status)

@app.route("/register", methods=['GET'])
def all_person_page():
    log_status = loggedin_check()

    query = "SELECT * FROM person"
    data = run_query(query)
    return render_template("all_person.html", 
                           data=data, searched=False, 
                           logged=log_status)


@app.route("/register", methods=['GET', 'POST'])
def search_register():
    log_status = loggedin_check()

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
        return render_template("all_person.html", searched_data=data, searched=True, 
                           logged= log_status)
    else:
        return render_template("all_person.html", searched_data=data, searched=True, 
                           logged= log_status)
    

@app.route("/register/<int:id>", methods=['GET'])
def pers_info(id):
    query = f"SELECT * FROM person WHERE personID like {id}"
    data = run_query(query)

    log_status = loggedin_check()

    return render_template("pers_info.html", data=data[0], logged= log_status)



@app.route("/login")
def login_page():
    log_status = loggedin_check()
    return render_template("login.html", logged= log_status)


@app.route("/login", methods=["POST"])
def login_validation():

    try:

        form_pw, form_user = request.form["login_pw"], request.form["login_user"]    

        query = f"SELECT * FROM user WHERE username LIKE '{form_user}'"
        data = run_query(query)

        if data:
            data_pw, data_user = data[0]['password'], data[0]['username']

            if form_pw == data_pw:
                session['logged'] = True
                return render_template('home.html', logged = session['logged'])
            else: 
                return render_template("login.html", error="Wrong username or password!")
        else:
            return render_template("login.html", error="Wrong username or password!")
        
    except Exception as e:
        print(e)

    return render_template('home.html', logged = session['logged'])

@app.route("/mypage", methods= ["GET", "POST"])
def my_page():
    log_status = loggedin_check()

    if log_status == False:
            return "Not authorized wip"

    if "Logout" in request.form:
        session['logged'] = False

    return render_template('login.html', logged = session['logged'])
    

    


        




if __name__ == "__main__":
    with app.app_context():
        upgrade()
        seed_data()

    app.run(debug=True)




