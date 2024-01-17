import pytest
from pytest import mark
from unittest.mock import patch
from unittest import mock
import requests
from app import get_books, run_query
from flask import request