import pytest
from pytest import mark
from unittest.mock import patch
from unittest import mock
import requests

# TODO
# NOTE Parametrize för alla endpoints som behöver externt data.
    
endpoint = 'http://127.0.0.1:5000'

def test_home():                   # Skickar en GET
    response = requests.get(endpoint)
    assert response.status_code == 200


# NOTE - Mock response? You know how
# GET /books - Visar en lista över böcker + filter 
@mark.parametrize('category, filter',[('title','Dracula'),('author','Bram Stoker'),('genre','Horror'),('year', '2012')])              
def test_GET_books(category,filter):        
    response = requests.get(endpoint + f'/books?{category}={filter}')
    assert response.status_code == 200  # Check connection

    print(response.json()[0][category])
    data = response.json()[0]

    assert data[category] == filter



# @mark.xfail
@mark.parametrize('category, filter',[('wrong_key','Dracula'),('wrong_key', 'wrong_filter')])              
def test_GET_books_wrong(category,filter):          
    response = requests.get(endpoint + f'/books?{category}={filter}')
    assert response.status_code == 200  # Check connection

    # print(response.json()[0][category])
    # data = response.json()[0]
    return response.json()


# WIP Current test
print ( test_GET_books_wrong('wrong_key', 'Dracula')  ) # (response.json() still getting Dracula row. 

# print ( test_GET_books_wrong('wrong_key', 'wrong_filter')  )   # Empty list 



    




# @pytest.Parametrize('data', [{'title':'Test_title', 'author':'Test_author', 'year': 'Test_year', 'genre': 'Test_genre', 'summary':'Test_summary'}, {'wrong_key_title':'Randomtext_title','wrong_key_author': 'Randomtext02'},
# {''},               # Too few keys
# {''}                # Too many keys
# ])
# def test_POST_books(data):
#     app.books_add_to_db()





# region bye
# def test_PUT_books_id():

# def test_DELETE_books_id():

# def test_POST_reviews():

# def test_GET_reviews():

# def test_GET_reviews_id():

# def test_GET_books_top():

# def test_GET_author():
    
# endregion
# NOTE VG: Skriv gärna en kommentar om hur du resonerat när du deginat testet. 