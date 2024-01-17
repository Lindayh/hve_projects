import pytest
from pytest import mark
from unittest.mock import patch
from unittest import mock
import requests
from app import get_books, run_query
from flask import request

@pytest.fixture
def endpoint():
    return 'http://127.0.0.1:5000'

# POST /reviews - Lägger till en ny recension till en bok.
@mark.parametrize('dictionary')
def test_POST_reviews(endpoint, dictionary):
    response = requests.post(f'{endpoint}/reviews', json=dictionary)


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

    assert response.json()[0]['book_ID']  == str(book_id)

def test_GET_reviews_book_id_invalid(endpoint):
    book_id = 9999
    response = requests.get(f'{endpoint}/reviews/{book_id}')

    assert response.text == 'No reviews for this book.'

