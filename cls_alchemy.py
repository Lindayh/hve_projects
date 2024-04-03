from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from faker import Faker
from random import randint
import os
import numpy as np
from flask_security import RoleMixin, UserMixin, SQLAlchemyUserDatastore, hash_password

db = SQLAlchemy()

roles_users = db.Table('roles_users', 
                       Column('user_id', Integer(), db.ForeignKey('user.id')),
                       Column('role_id', Integer(), db.ForeignKey('role.id')),               
                       )

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    password = Column(String)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('user', lazy='dynamic'))
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    active = Column(db.Boolean())

user_datastore = SQLAlchemyUserDatastore(db, User, Role) 

class Person(db.Model):
    person_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    age = Column(Integer)
    phone_nr = Column(String)
    email = Column(String)
    country = Column(String)
    city = Column(String)
    address = Column(String)

    img = Column(String)

def seed_data():
    faker = Faker()

    if not Role.query.first():
        user_datastore.create_role(name="Admin")
        user_datastore.create_role(name="User")
        db.session.commit()

    while Person.query.count() < 300:   

        gender = np.random.choice(["M", "F"], p=[0.5, 0.5])
        rand_nr = np.random.randint(0,150)
        if gender == "M":
            new_name = faker.name_male()
            new_img= f'static/images/face_man/man_{rand_nr}.jpg'

        if gender == "F":
            new_name = faker.name_female()
            new_img= f'static/images/face_woman/woman_{rand_nr}.jpg'


        new_age = randint(20,70)
        new_phone_nr = str(randint(1000000000, 9999999999))
        new_country = faker.country()
        new_email = faker.email()
        new_city = faker.city()
        new_address = faker.address()

        new_person = Person(name=new_name, age=new_age, phone_nr=new_phone_nr, email=new_email,
                            country=new_country, city=new_city, address=new_address, img=new_img)
        db.session.add(new_person)
        db.session.commit()
    
    while User.query.count() < 20:
        new_username = faker.user_name()
        new_pw = hash_password('password')
        new_roles = str(np.random.choice(["Admin", "User"], p=[0.5, 0.5]))

        user_datastore.create_user(username=new_username, password= new_pw, roles=[new_roles])

        db.session.commit()

