import pytest
from pytest import mark
from unittest.mock import patch
from unittest import mock
import requests

# TODO
# NOTE Parametrize för alla endpoints som behöver externt data.
# NOTE - Mock response? You know how
    
endpoint = 'http://127.0.0.1:5000'


# GET /books - Visar en lista över böcker 

def test_GET_books_list():                   # Skickar en GET
    response = requests.get(endpoint + f'/books?')
    assert response.status_code == 200
    # assert that you get a list

    assert response.json()

# /books?key=value test
@mark.parametrize('dictionary',[{'title':'Dracula'},{'author':'Bram Stoker'},{'genre':'Horror'},{'year': '2012'}])              
def test_GET_books_filter_correct(dictionary):
    key = list(dictionary.keys())[0]               
    value = list(dictionary.values())[0]         
    response = requests.get(endpoint + f'/books?{key}={value}')
    assert response.status_code == 200  # Check connection

    # print(response.json())
    assert value in response.json()[0]


@mark.parametrize('dictionary',[{'title':'non_existing_title'}])              
def test_GET_books_filter_wrong_value(dictionary):
    key = list(dictionary.keys())[0]               
    value = list(dictionary.values())[0]         
    response = requests.get(endpoint + f'/books?{key}={value}')
    assert response.status_code == 200  # Check connection

    assert response.text == "Search returned no results."

@mark.parametrize('dictionary',[{'wrong_key':'Dracula'},{'wrong_key': 'wrong_filter'}])              
def test_GET_books_filter_wrong_keys(dictionary):
    key = list(dictionary.keys())[0]               
    value = list(dictionary.values())[0]                # ;print(f'Key: {key}, value: {value}')       
    
    response = requests.get(endpoint + f'/books?{key}={value}')
    assert response.status_code == 200  

    assert response.text == 'Wrong key.'

# TODO - Onsdag
# POST /books - Lägger till en bok i databasen
# @pytest.Parametrize('data', [{'title':'Test_title', 'author':'Test_author', 'year': 'Test_year', 'genre': 'Test_genre', 'summary':'Test_summary'}, {'wrong_key_title':'Randomtext_title','wrong_key_author': 'Randomtext02'},
# {''},               # Too few keys
# {''}                # Too many keys
# ])
# def test_POST_books(data):
#     app.books_add_to_db()

# region bye


# def test_DELETE_books_id():

# def test_POST_reviews():

# def test_GET_reviews():

# def test_GET_reviews_id():

# def test_GET_books_top():

# def test_GET_author():
    
# endregion
# NOTE VG: Skriv gärna en kommentar om hur du resonerat när du deginat testet. 