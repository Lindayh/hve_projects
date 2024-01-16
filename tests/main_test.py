import pytest
from unittest.mock import patch
from unittest import mock
import app.app as app

# TODO
# NOTE Parametrize för alla endpoints som behöver externt data.
# endpoint = 'https:/127.0.0.1:5000/books'    # GET
# def test_GET_books():
    
# WIP Current test
endpoint = 'https:/127.0.0.1:5000/books'    # POST
@pytest.Parametrize('data', [{'title':'Test_title', 'author':'Test_author', 'year': 'Test_year', 'genre': 'Test_genre', 'summary':'Test_summary'}, {'wrong_key_title':'Randomtext_title','wrong_key_author': 'Randomtext02'},
{''},               # Too few keys
{''}                # Too many keys
])
def test_POST_books(data):
    app.books_add_to_db

# LINK test POST /books
@patch('request.args')
def test_testing(mock_get):
    mock_args = mock.Mock()
    mock_args.return_value = {'title':'Test_title', 
                              'author': 'Test_author',
                              'year':'Test_year',
                              'genre': 'Test_genre',
                              'summary': 'Test_summary'}



# @patch('requests.get')
# def test_get_users(mock_get):
#     mock_response = mock.Mock()
#     mock_response.status_code = 200
#     mock_response.json.return_value = {'id': 1, 'name': 'John Doe'}
#     mock_get.return_value = mock_response
#     data = service.get_users()
#     assert data == {'id': 1, 'name': 'John Doe'}


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
