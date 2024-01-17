import pytest
from pytest import mark
from unittest.mock import patch
from unittest import mock
import requests
from app import get_books, run_show_query

# TODO
# NOTE Parametrize för alla endpoints som behöver externt data.
# NOTE - Mock response? You know how
    
endpoint = 'http://127.0.0.1:5000'


# GET /books - Visar en lista över böcker 

def test_GET_books_list():                   # Skickar en GET
    response = requests.get(endpoint + f'/books?')
    assert response.status_code == 200

    assert response.json()      # assert that you get a list?

# /books?key=value test
@mark.parametrize('dictionary',[{'title':'Dracula'},{'author':'Bram Stoker'},{'genre':'Horror'},{'year': '2012'}])              
def test_GET_books_filter_correct(dictionary):
    key = list(dictionary.keys())[0]               
    value = list(dictionary.values())[0]         
    response = requests.get(endpoint + f'/books?{key}={value}')
    assert response.status_code == 200 

    assert value in response.json()[0]

@mark.parametrize('dictionary',[{'title':'non_existing_title'}])              
def test_GET_books_filter_wrong_value(dictionary):
    key = list(dictionary.keys())[0]               
    value = list(dictionary.values())[0]         
    response = requests.get(endpoint + f'/books?{key}={value}')
    assert response.status_code == 200 

    assert response.text == "Search returned no results."

@mark.parametrize('dictionary',[{'wrong_key':'Dracula'},{'wrong_key': 'wrong_filter'}])              
def test_GET_books_filter_wrong_keys(dictionary):
    key = list(dictionary.keys())[0]               
    value = list(dictionary.values())[0]                     
    
    response = requests.get(endpoint + f'/books?{key}={value}')
    assert response.status_code == 200  

    assert response.text == 'Wrong key.'


# POST /books - Lägger till en bok i databasen
@mark.parametrize('dictionary', [{'title':'Pytest_title', 'author':'Pytest_author', 'year': 'Pytest_year', 'genre': 'Pytest_genre', 'summary':'Pytest_summary'}])
# {''},               # Too few keys
# {''}                # Too many keys
# ])
def test_POST_books(dictionary):
    data_01 = get_books()               

    response = requests.post(endpoint + '/books', json=dictionary)
    assert response.status_code == 200
    
    data_02 = get_books()               
    assert  len(data_02) > len(data_01)

    query = f"""DELETE FROM book
    WHERE title like "Pytest_title"
    """
    run_show_query(query)


@mark.wip
@mark.xfail
@mark.parametrize('dictionary', [{'title':'Pytest_title'}, {'wrong_key':'Pytest_fail' }])
def test_POST_books(dictionary):
    data_01 = get_books()               

    response = requests.post(endpoint + '/books', json=dictionary)
    assert response.status_code == 200
    
    data_02 = get_books()               
    assert len(data_02) > len(data_01)







# region bye

# def test_DELETE_books_id():

# def test_POST_reviews():

# def test_GET_reviews():

# def test_GET_reviews_id():

# def test_GET_books_top():

# def test_GET_author():
    
# endregion
# NOTE VG: Skriv gärna en kommentar om hur du resonerat när du deginat testet. 