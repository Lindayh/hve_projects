import pytest
from pytest import mark
from unittest.mock import patch
from unittest import mock
import requests
from app import get_books, run_query
from flask import request
from random import randint

@pytest.fixture
def endpoint():
    return 'http://127.0.0.1:5000'

# GET /books/{book_id} - Hämtar en enskild bok.
def test_GET_books_id(endpoint, book_id:int=1):
    response = requests.get(endpoint + f'/books/{book_id}')
    assert response.status_code == 200

    query = f"""SELECT book_ID
    FROM book
    WHERE book_ID like {book_id}
    """
    data = run_query(query)           

    assert response.json()[0]['book_ID']  == data[0]['book_ID']

# Book id som finns inte på dbn
def test_GET_books_id_wrong(endpoint):
    book_id = 9999
    response = requests.get(endpoint + f'/books/{book_id}')
    assert response.status_code == 200

    assert response.text == 'No book with such ID.'

# PUT /books/{book_id} - Uppdaterar information om en enskild bok.
def test_PUT_books_id_right(endpoint, book_id=135):
    dictionary = {'title':'Updated_title_', 'author':'Updated_author','year':f'{randint(0,2024)}', 'genre':'updated_genre', 'summary':'Updated_summary'}

    query = f""" SELECT *
    FROM book
    WHERE book_ID LIKE {book_id}
    """ 

    data_01 = run_query(query)
    response = requests.put(f'{endpoint}/books/{book_id}', json=dictionary)
    data_02 = run_query(query)

    assert data_01 != data_02

def test_PUT_books_id_invalid_id(endpoint,book_id:int=9999):
    dictionary = {'title':'Updated_title', 'author':'Updated_author','year':'Updated_year', 'genre':'Updated_genre', 'summary':'Updated_summary'}
    response = requests.put(f'{endpoint}/books/{book_id}', json=dictionary)

    assert response.text == "No book with such id."

@mark.parametrize('dictionary',[{'wrong_key':'Updated_title', 'author':'Updated_author','year':'Updated_year', 'genre':'Updated_genre', 'summary':'Updated_summary'},
                                {'':'','':'','':'','':'','':''},
                                {"title":"Something"},
                                {'wrong_key':'Updated_title', 'author':'Updated_author','year':'Updated_year', 'genre':'Updated_genre', 'summary':'Updated_summary', 'extra_key':'extra_value'}   ])              
def test_PUT_books_id_wrong_keys(endpoint, dictionary, book_id:int=135,):

    response = requests.put(f'{endpoint}/books/{book_id}', json=dictionary)

    assert "Invalid keys" in response.text

    
# DELETE /books/{book_id} - Tar bort en enskild bok
def test_DELETE_books_id(endpoint):
    #  Skapa en ny record
    query = """INSERT INTO book ('title','author','year','genre','summary')
    VALUES ('Random Book','Writer McScribbly','425 BCE','Classics','My nice summary')"""
    data = run_query(query) 

    query = f"""SELECT max(book_ID) as id FROM book  """            # max(book_ID) så får man den nyaste ID
    data = run_query(query)         
    book_id = data[0]['id']

    response = requests.delete(f'{endpoint}/books/{book_id}')

    query = f"""SELECT * FROM book WHERE book_ID LIKE {book_id} """
    data = run_query(query) 

    assert data == []

@mark.wip
@mark.parametrize('invalid_id',[9999,'text',9999.45])
def test_DELETE_books_id_invalid_id(endpoint, invalid_id):
    invalid_id = 9999

    response = requests.delete(f'{endpoint}/books/{invalid_id}')

    assert response.text == "No book with such ID."
