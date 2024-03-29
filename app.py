from flask import Flask, render_template, request, session
import os
from dotenv import load_dotenv
from flask_migrate import Migrate, upgrade
from flask_sqlalchemy import SQLAlchemy

from SQLAlchemy_test import db, Person, User, seed_data


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

    data =  Person.query
    
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
        data = Person.query.filter(
            Person.name.like("%" + search_term + "%")).all()

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

    data = Person.query.filter(
            Person.person_id.like(id)).first()
    
    print(Person.person_id)

    log_status = loggedin_check()

    return render_template("pers_info.html", data=data, logged= log_status)


@app.route("/login")
def login_page():
    log_status = loggedin_check()
    return render_template("login.html", logged= log_status)


@app.route("/login", methods=["POST"])
def login_validation():

    log_status = loggedin_check()

    try:
        form_pw, form_user = request.form["login_pw"], request.form["login_user"]    

        data = User.query.filter(
            User.username.like(form_user)).first()

        if data:
            data_user = data.username
            data_pw = data.password

            if form_pw == data_pw:
                session['logged'] = True
                log_status = loggedin_check()    
                return render_template('home.html', logged = log_status)
            else: 
                return render_template("login.html", error="Wrong username or password!")
        else:
            return render_template("login.html", error="Wrong username or password!")
        
    except Exception as e:
        print(e)

    print(log_status)
    return render_template('home.html', logged = log_status)


@app.route("/mypage", methods= ["GET", "POST"])
def my_page():
    log_status = loggedin_check()

    if log_status == False:
            return "Not authorized wip"

    if "Logout" in request.form:
        session['logged'] = False
        log_status = loggedin_check()    
        return render_template('home.html', logged = log_status)

    return render_template('login.html', logged = session['logged'])
    

    
if __name__ == "__main__":
    with app.app_context():
        upgrade()
        seed_data()

    app.run(debug=True)




