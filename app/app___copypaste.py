import pytest
from pytest import mark
from unittest.mock import patch
from unittest import mock
import requests
from db_functions import get_books, run_show_query
from random import randint



endpoint = 'http://127.0.0.1:5000'



# PUT /books/{book_id} - Uppdaterar information om en enskild bok.
def test_PUT_books_id_right(endpoint=endpoint, book_id=135):
    dictionary = {'title':'Updated_title_', 'author':'Updated_author','year':f'{randint(0,2024)}', 'genre':'updated_genre', 'summary':'Updated_summary'}

    query = f""" SELECT *
    FROM book
    WHERE book_ID LIKE {book_id}
    """ 

    data_01 = run_show_query(query)
    response = requests.put(f'{endpoint}/books/{book_id}', json=dictionary)
    data_02 = run_show_query(query)

    assert data_01 != data_02

def test_PUT_books_id_invalid_id(endpoint=endpoint,book_id:int=9999):
    dictionary = {'title':'Updated_title', 'author':'Updated_author','year':'Updated_year', 'genre':'Updated_genre', 'summary':'Updated_summary'}
    response = requests.put(f'{endpoint}/books/{book_id}', json=dictionary)

    print(response.text)
    print (response.text == "No book with such id.")

def test_PUT_books_id_wrong_keys(endpoint=endpoint,book_id:int=135):
    dictionary = {'wrong_key':'Updated_title', 'author':'Updated_author','year':'Updated_year', 'genre':'Updated_genre', 'summary':'Updated_summary'}
    dictionary = {'':'','':'','':'','':'','':''}            # Rätt antal, tomma värde
    dictionary = {"title":"Something"}
    dictionary = {'wrong_key':'Updated_title', 'author':'Updated_author','year':'Updated_year', 'genre':'Updated_genre', 'summary':'Updated_summary', 'extra_key':'extra_value'}    

    response = requests.put(f'{endpoint}/books/{book_id}', json=dictionary)

    print("Invalid keys" in response.text)

test_PUT_books_id_wrong_keys()






    

# id som finns inte


