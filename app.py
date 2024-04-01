from flask import Flask, render_template, request, session, redirect, url_for
import os
from dotenv import load_dotenv
from flask_migrate import Migrate, upgrade
from flask_sqlalchemy import SQLAlchemy
from cls_alchemy import db, Person, User, seed_data

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


@app.route("/register", methods=['POST', 'GET'])    
def all_person_page():
    log_status = loggedin_check()
    
    data =  Person.query
    page = request.args.get('page', 1, type=int)

    if 'search_field' in request.form or 's' in request.args:

        if request.form:
            search_term = request.form.get('search_field')
            if "'" in search_term: search_term=search_term.replace("'", "''")
        else:
            search_term = request.args.get('s')

        search_data = data.filter(
            Person.name.like("%" + search_term + "%") |
            Person.age.like("%" + search_term + "%") |
            Person.country.like("%" + search_term + "%")
            )

        print(f'Search term: {search_term} | Results found: {search_data.count()} | Args \'page\': {request.args.get('page')}')

        if search_data.count()>30:
            paged_search_data = search_data.paginate(page=page, per_page=30, error_out=True)

            return render_template("all_person.html", data=paged_search_data, logged=log_status, page=page, s=search_term)
        else:
            if page>1:
                return redirect(url_for("all_person_page", s=search_term, page=1))
            return render_template("all_person.html", data=search_data, logged=log_status, page=page, s=search_term)
            
    paged_data = data.paginate(page=page, per_page=30, error_out=True)

    return render_template("all_person.html", data=paged_data, searched=False, logged=log_status, page=page)
    

@app.route("/register/<int:id>", methods=['GET'])
def pers_info(id):

    data = Person.query.filter(
            Person.person_id.like(id)).first()

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

# TODO Authorization
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




