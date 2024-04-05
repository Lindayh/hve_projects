from flask import Flask, render_template, request, session, redirect, url_for
from dotenv import load_dotenv
from flask_migrate import Migrate, upgrade
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, login_required, roles_required
from flask_wtf.csrf import CSRFProtect
import os
from cls_alchemy import db, Person, User, seed_data, user_datastore

load_dotenv()
app = Flask(__name__)

CSRFProtect(app)

app.secret_key = "psst"

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URI_LOCAL")
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SECURITY_PASSWORD_SALT'] = os.getenv('SECURITY_PASSWORD_SALT')

app.config['SECURITY_LOGOUT_URL']= '/log_out'
app.config['SECURITY_POST_LOGOUT_VIEW']= '/post_logout'

app.config['SECURITY_USERNAME_ENABLE'] = True
app.config['IDENTITY_ATTRIBUTES'] = 'username'

db.init_app(app)
migrate = Migrate(app, db)
security = Security(app, user_datastore)


@app.route("/")
@login_required
def home():
    return render_template('home.html')


@app.route("/register", methods=['POST', 'GET']) 
@login_required 
def all_person_page():
    data =  Person.query
    page = request.args.get('page', 1, type=int)

    if 'search_field' in request.form or 's' in request.args:

        if 'search_field' in request.form:
            search_term = request.form.get('search_field')
            if "'" in search_term: search_term=search_term.replace("'", "''")
        else:
            search_term = request.args.get('s')

        search_data = data.filter(
            Person.name.like("%" + search_term + "%") |
            Person.age.like("%" + search_term + "%") |
            Person.country.like("%" + search_term + "%")
            )

        print(f"Search term: {search_term} | Results found: {search_data.count()} | Args \'page\': {request.args.get('page')}  \n  'search_field' in request.form: {'search_field' in request.form}   ")

        if search_data.count()>30:           
            paged_search_data = search_data.paginate(page=page, per_page=30, error_out=True)

            return render_template("all_person.html", data=paged_search_data, page=page, s=search_term)  # ,logged=log_status
        elif page>1:
            return redirect(url_for("all_person_page", s=search_term, page=1))
        return render_template("all_person.html", data=search_data, page=page, s=search_term)
            
    paged_data = data.paginate(page=page, per_page=30, error_out=True)

    return render_template("all_person.html", data=paged_data, searched=False, page=page)
    

@app.route("/register/<int:id>", methods=['GET'])
@login_required 
def pers_info(id):
    data = Person.query.filter(
            Person.person_id.like(id)).first()
    return render_template("pers_info.html", data=data)


# NOTE /user/<user_id>
# TODO Admin page
@app.route("/mypage", methods= ["GET", "POST"])
def my_page():
    return render_template('mypage.html')

@app.route("/log_out")
def log_out():
    return "Logging out"

@app.route("/post_logout")
def post_logout():
    return render_template("post_logout.html")

@app.route('/admin')
@roles_required("Admin")
def admin_page():
    return render_template('admin_page.html')


if __name__ == "__main__":
    with app.app_context():
        upgrade()
        seed_data()

    app.run(debug=True)