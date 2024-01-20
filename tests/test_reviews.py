import pytest
from pytest import mark
from unittest.mock import patch
from unittest import mock
import requests
from app import run_query
from flask import request
from tests import endpoint

# POST /reviews - Lägger till en ny recension till en bok.
def test_POST_reviews_succeed(endpoint):
    len_01 = len(run_query(f"SELECT * FROM review")) 

    dictionary = {"user":"Test_user","book_ID":1, "rating":4, "description":"Awsomm"}     

    requests.post(f'{endpoint}/reviews', json=dictionary)

    len_02 = len(run_query(f"SELECT * FROM review"))          

    assert len_02 == len_01+1

    run_query(f"""DELETE FROM review
                WHERE reviewID LIKE 
                (SELECT max(reviewID) FROM review)       """)
    
# alla möjliga fel värde/nycklar (POST kvar bara)
@mark.parametrize('dictionary',[{"wrong_key":"POST_reviews","book_ID":1, "rating":4, "description":"Awsomm"},{'user':''},{'':'','':'','':'','':''}, {"user":"Test_user","book_ID":1, "rating":4, "description":"Awsomm", 'extra_key':'extra_value'}])
def test_POST_reviews_wrong_keys(endpoint, dictionary):   
    response = requests.post(f'{endpoint}/reviews', json=dictionary)        ;print(response.text)

    assert 'missing keys' in response.text.lower()


# GET /reviews - Hämtar alla recensioner som finns i databasen
def test_GET_reviews(endpoint):
    response = requests.get(f'{endpoint}/reviews')

    query = "SELECT * FROM review"

    assert (response.headers['Content-Type'] == 'application/json')
    assert ( len(run_query(query)) == len(response.json()))

# GET /reviews/{book_id} - Hämtar alla recensioner för en enskild bok.
def test_GET_reviews_book_id(endpoint):
    book_id = 1
    response = requests.get(f'{endpoint}/reviews/{book_id}')

    assert response.json()[0]['book_ID']  == book_id

def test_GET_reviews_book_id_invalid(endpoint):
    book_id = 9999
    response = requests.get(f'{endpoint}/reviews/{book_id}')

    assert response.text == 'No reviews for this book.'

