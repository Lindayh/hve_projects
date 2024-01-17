import pytest
from pytest import mark
from unittest.mock import patch
from unittest import mock
import requests
from app import get_books, run_show_query
from flask import request

@pytest.fixture
def endpoint():
    return 'http://127.0.0.1:5000'

# GET
@mark.wip
def test_GET_books_id(endpoint, book_id:int=1):
    response = requests.get(endpoint + f'/books/{book_id}')
    assert response.status_code == 200

    query = f"""SELECT book_ID
    FROM book
    WHERE book_ID like {book_id}
    """
    data = run_show_query(query)           

    assert response.json()[0]['book_ID']  == data[0][0]

# Book id som finns inte på dbn
def test_GET_books_id_wrong(endpoint):
    book_id = 9999
    response = requests.get(endpoint + f'/books/{book_id}')
    assert response.status_code == 200

    assert response.text == 'No book with such ID.'

# PUT

    
# DELETE

