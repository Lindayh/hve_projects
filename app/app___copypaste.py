import pytest
from pytest import mark
from unittest.mock import patch
from unittest import mock
import requests
from db_functions import get_books, run_show_query



endpoint = 'http://127.0.0.1:5000'

dictionary={"title":'Pytest_title'}

def test_GET_books_id(endpoint, book_id:int):
    response = requests.get(endpoint + f'/books/{book_id}')
    assert response.status_code == 200

    query = f"""SELECT book_ID
    FROM book
    WHERE book_ID like {book_id}
    """
    data = run_show_query(query)           

    print (response.json()[0]['book_ID']  == data[0][0] )

def test_GET_books_id_wrong(endpoint,book_id:int):
    response = requests.get(endpoint + f'/books/{book_id}')
    assert response.status_code == 200

    assert response.text == 'No book with such ID.'


test_GET_books_id_wrong(endpoint, book_id=2568)
