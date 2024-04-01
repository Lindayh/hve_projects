from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from faker import Faker
from random import randint

import os

db = SQLAlchemy()

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

class User(db.Model):
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    password = Column(String)

def seed_data():
    faker = Faker()
    while Person.query.count() < 300:
        new_name = faker.name()
        new_age = randint(20,70)
        new_phone_nr = str(randint(1000000000, 9999999999))
        new_country = faker.country()
        new_email = faker.email()
        new_city = faker.city()
        new_address = faker.address()

        new_person = Person(name=new_name, age=new_age, phone_nr=new_phone_nr, email=new_email,
                            country=new_country, city=new_city, address=new_address)
        db.session.add(new_person)
        db.session.commit()
    
    while User.query.count() < 50:
        new_username = faker.user_name()
        new_pw = faker.password()

        new_user = User(username=new_username, password=new_pw)

        db.session.add(new_user)
        db.session.commit()
    

    