import pytest

import vysion.client as client
from vysion.client.error import VysionError

from . import config

def test_initialization():
    c = client.Client(api_key=config.API_KEY)
    assert True

'''
def test_email(email="purplefdw@protonmail.ch"):
    result = c.find_email(email)
    # result = c.search("tijuana")

    for hit in result.hits:
        print(hit.page.title)
'''

def test_invalid_apikey():
    try:
        client.Client(api_key="invalid api key")
    except Exception as e:
        assert type(e) is VysionError # TODO Validate 403

