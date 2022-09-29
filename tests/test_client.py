from curses.has_key import has_key
import pytest

import vysion.client as client
from vysion.client.error import VysionError

from . import config

##### API INTEGRATION TEST ######


def test_initialization():
    c = client.Client(api_key=config.API_KEY)
    assert True


def test_url_should_not_find(url="dkalg"):
    try:
        c = client.Client(api_key=config.API_KEY)
        result = c.find_url(url)

        assert 'total' in str(result), True
        assert 'hits' in str(result), True
        assert result.total == 0
        assert len(result.hits) == 0

    except Exception as exc:
        print("TEST EXCEPTION", exc)
        assert False, f"'test_url_should_not_find' raised an exception {exc}"


def test_url_should_find(url="continewsnv5otx5kaoje7krkto2qbu3gtqef22mnr7eaxw3y6ncz3ad.onion"):
    try:
        c = client.Client(api_key=config.API_KEY)
        result = c.find_url(url)

        assert 'total' in str(result), True
        assert 'hits' in str(result), True
        assert result.total > 0
        assert len(result.hits) > 0

    except Exception as exc:
        print("TEST EXCEPTION", exc)
        assert False, f"'test_url_should_find' raised an exception {exc}"


def test_email_should_not_find(email="purplefdw@hdu.com.es.org"):
    try:
        c = client.Client(api_key=config.API_KEY)
        result = c.find_email(email)

        assert 'total' in str(result), True
        assert 'hits' in str(result), True
        assert result.total == 0
        assert len(result.hits) == 0

    except Exception as exc:
        print("TEST EXCEPTION", exc)
        assert False, f"'test_email_should_not_find' raised an exception {exc}"


def test_email_should_find(email="som3on3@xmpp.jp"):
    try:
        c = client.Client(api_key=config.API_KEY)
        result = c.find_email(email)

        assert 'total' in str(result), True
        assert 'hits' in str(result), True
        assert result.total > 0
        assert len(result.hits) > 0

    except Exception as exc:
        print("TEST EXCEPTION", exc)
        assert False, f"'test_email_should_find' raised an exception {exc}"


def test_search_should_find(key="tijuana"):
    try:
        c = client.Client(api_key=config.API_KEY)
        result = c.search(key)

        assert 'total' in str(result), True
        assert 'hits' in str(result), True
        assert result.total > 0
        assert len(result.hits) > 0

    except Exception as exc:
        print("TEST EXCEPTION", exc)
        assert False, f"'test_search_should_find' raised an exception {exc}"


def test_search_should_not_find(key="lorolo"):
    try:
        c = client.Client(api_key=config.API_KEY)
        result = c.search(key)

        assert 'total' in str(result), True
        assert 'hits' in str(result), True
        assert result.total == 0
        assert len(result.hits) == 0

    except Exception as exc:
        print("TEST EXCEPTION", exc)
        assert False, f"'test_search_should__not_find' raised an exception {exc}"


def test_find_btc_should_find(address="114qvtyucvKtiNXy9UL3eYx6HPYmadxeM4"):
    try:
        c = client.Client(api_key=config.API_KEY)
        result = c.find_btc(address)

        assert 'total' in str(result), True
        assert 'hits' in str(result), True
        assert result.total > 0
        assert len(result.hits) > 0

    except Exception as exc:
        print("TEST EXCEPTION", exc)
        assert False, f"'test_find_btc_should_find' raised an exception {exc}"


def test_find_btc_should_not_find(address="notvalidaddress"):
    try:
        c = client.Client(api_key=config.API_KEY)
        result = c.find_btc(address)

        assert 'total' in str(result), True
        assert 'hits' in str(result), True
        assert result.total == 0
        assert len(result.hits) == 0

    except Exception as exc:
        print("TEST EXCEPTION", exc)
        assert False, f"'test_find_btc_should_not_find' raised an exception {exc}"        


def test_invalid_apikey():
    try:
        client.Client(api_key="invalid api key")
    except Exception as e:
        assert type(e) is VysionError  # TODO Validate 403
