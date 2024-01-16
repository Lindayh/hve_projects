import pytest
import source.main as main

# TODO
# NOTE Parametrize för alla endpoints som behöver externt data.
# def test_GET_books():
    
# WIP Current
@pytest.Parametrize('data', [{'title':'Test_title', 'author':'Test_author', 'year': 'Test_year', 'genre': 'Test_genre', 'summary':'Test_summary'}, {'wrong_key_title':'Randomtext_title','wrong_key_author': 'Randomtext02'}])
def test_POST_books(data):
    main.books_add_to_db


# def test_PUT_books_id():

# def test_DELETE_books_id():

# def test_POST_reviews():

# def test_GET_reviews():

# def test_GET_reviews_id():

# def test_GET_books_top():

# def test_GET_author():

# NOTE VG: Skriv gärna en kommentar om hur du resonerat när du deginat testet. 





