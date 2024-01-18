import pytest
from pytest import mark
from unittest.mock import patch
from unittest import mock
import requests
from app import get_books, run_query
from flask import request
from tests import endpoint

# GET /books/top - Hämtar de fem böckerna med högst genomsnittliga recensioner.
def test_GET_books_top(endpoint):
    response = requests.get(f'{endpoint}/books/top')
    
    assert response.json()

# GET /author - Hämtar en kort sammanfattning om författaren och författarens mest kända verk. Använd externa API:er för detta.
def test_GET_author(endpoint, dictionary={'author':'Lovecraft'}):
    response = requests.get(f'{endpoint}/author',json=dictionary)

    assert list(response.json().keys()) == ['bio', 'name']

@mark.wip
@mark.parametrize('dictionary',[{'wrong_key':'wrong_value'}, {'':''}, {'author':''}])
def test_GET_author_wrong(endpoint, dictionary):
    response = requests.get(f'{endpoint}/author',json=dictionary)

    assert "Invalid search term" in response.text
