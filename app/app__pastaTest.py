import pytest
from pytest import mark
from unittest.mock import patch
from unittest import mock
import requests
from random import randint

def test_GET_author_wrong(endpoint, dictionary):

    response = requests.get(f'{endpoint}/author',json=dictionary)

    print("invalid key" in response.text.lower())



if __name__ == '__main__':              # -----------------------------------------------------------
    endpoint = 'http://127.0.0.1:5000'

    # dictionary = {}

    test_GET_author_wrong(endpoint, dictionary={'wrongkey':'meow'})


    












