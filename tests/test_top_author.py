import pytest
from pytest import mark
import requests
from app import run_query
from flask import request
from tests import endpoint

# GET /books/top - Hämtar de fem böckerna med högst genomsnittliga recensioner.
def test_GET_books_top(endpoint):
    response = requests.get(f'{endpoint}/books/top')
    
    assert response.json()

# GET /author - Hämtar en kort sammanfattning om författaren och författarens mest kända verk. Använd externa API:er för detta.
def test_GET_author(endpoint, dictionary={'author':'Lovecraft'}):
    response = requests.get(f'{endpoint}/author',json=dictionary)

    assert list(response.json().keys()) == ['bio', 'name', 'top_works']


@mark.parametrize('dictionary',[{'wrong_key':'wrong_value'}, {'':''}, {'author':''}])
def test_GET_author_wrong(endpoint, dictionary):

    response = requests.get(f'{endpoint}/author',json=dictionary)

    assert "invalid key" in response.text.lower()






