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
    country = Column(String)
    img = Column(String)


def seed_data():
    faker = Faker()
    while Person.query.count() < 100:
        new_name = faker.name()
        new_age = randint(20,70)
        new_phone_nr = str(randint(1000000000, 9999999999))

        new_person = Person(name=new_name, age=new_age, phone_nr=new_phone_nr)
        db.session.add(new_person)
        db.session.commit()
    

    