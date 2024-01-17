import pytest
from pytest import mark
from unittest.mock import patch
from unittest import mock
import requests
from db_functions import get_books, run_show_query



endpoint = 'http://127.0.0.1:5000'

dictionary={"title":'Pytest_title'}

def test_POST_books(dictionary):        # xfail
    data_01 = get_books()               

    response = requests.post(endpoint + '/books', json=dictionary)
    assert response.status_code == 200
    
    data_02 = get_books()               
    assert len(data_02) > len(data_01)

    # query = f"""DELETE FROM book
    # WHERE title like "Pytest_title"
    # """
    # run_show_query(query)   
    
test_POST_books(dictionary)



