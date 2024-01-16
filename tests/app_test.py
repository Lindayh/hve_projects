import pytest
from unittest.mock import patch
from unittest import mock
import requests

# TODO
# NOTE Parametrize för alla endpoints som behöver externt data.
# endpoint = 'https:/127.0.0.1:5000/books'    # GET
# def test_GET_books():
    
# WIP Current test

endpoint = 'http://127.0.0.1:5000/'    # POST

response = requests.get(endpoint)       ;print(response)         # SET FLASK_APP='app/app.py' $env:FLASK_APP = "app/app.py"

# data = response.json()
# print(data)

status_code = response.status_code
print(status_code)


def test_call_endpoint():
    response = requests.get(endpoint)
    assert response.status_code == 200


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