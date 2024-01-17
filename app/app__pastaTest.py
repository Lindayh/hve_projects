import pytest
from pytest import mark
from unittest.mock import patch
from unittest import mock
import requests
from db_functions import get_books, run_query
from random import randint


# POST /reviews - Lägger till en ny recension till en bok.
def test_POST_reviews(endpoint, dictionary):

    response = requests.post(f'{endpoint}/reviews', json=dictionary)


def test_POST_reviews_wrong_keys(endpoint, dictionary):
   
    response = requests.post(f'{endpoint}/reviews', json=dictionary)

    
# NOTE check properly tests with run_query 

if __name__ == '__main__':
    endpoint = 'http://127.0.0.1:5000'

    dictionary = [{},
                  {}
                  ]

    test_POST_reviews(endpoint,dictionary)









