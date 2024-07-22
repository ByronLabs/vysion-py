from curses.has_key import has_key

import pytest

import vysion.client as client
from vysion.client.error import Error

from . import config

##### API INTEGRATION TEST ######


def test_initialization():
    c = client.Client(api_key=config.API_KEY)
    assert True


def test_url_should_not_find(url="dkalg"):
    try:
        c = client.Client(api_key=config.API_KEY)
        result = c.find_url(url)

        assert "total" in str(result), True
        assert "hits" in str(result), True
        assert result.total == 0
        assert len(result.hits) == 0

    except Exception as exc:
        print("TEST EXCEPTION", exc)
        assert False, f"'test_url_should_not_find' raised an exception {exc}"


def test_url_should_find(
    url="continewsnv5otx5kaoje7krkto2qbu3gtqef22mnr7eaxw3y6ncz3ad.onion",
):
    try:
        c = client.Client(api_key=config.API_KEY)
        result = c.find_url(url)

        assert "total" in str(result), True
        assert "hits" in str(result), True
        assert result.total > 0
        assert len(result.hits) > 0

    except Exception as exc:
        print("TEST EXCEPTION", exc)
        assert False, f"'test_url_should_find' raised an exception {exc}"


def test_email_should_not_find(email="purplefdw@hdu.com.es.org"):
    try:
        c = client.Client(api_key=config.API_KEY)
        result = c.find_email(email)

        assert "total" in str(result), True
        assert "hits" in str(result), True
        assert result.total == 0
        assert len(result.hits) == 0

    except Exception as exc:
        print("TEST EXCEPTION", exc)
        assert False, f"'test_email_should_not_find' raised an exception {exc}"


def test_email_should_find(email="som3on3@xmpp.jp"):
    try:
        c = client.Client(api_key=config.API_KEY)
        result = c.find_email(email)

        assert "total" in str(result), True
        assert "hits" in str(result), True
        assert result.total > 0
        assert len(result.hits) > 0

    except Exception as exc:
        print("TEST EXCEPTION", exc)
        assert False, f"'test_email_should_find' raised an exception {exc}"


def test_search_should_find(key="tijuana"):
    try:
        c = client.Client(api_key=config.API_KEY)
        result = c.search(key)

        assert "total" in str(result), True
        assert "hits" in str(result), True
        assert result.total > 0
        assert len(result.hits) > 0

    except Exception as exc:
        print("TEST EXCEPTION", exc)
        assert False, f"'test_search_should_find' raised an exception {exc}"


def test_search_should_not_find(key="lorolo"):
    try:
        c = client.Client(api_key=config.API_KEY)
        result = c.search(key)

        assert "total" in str(result), True
        assert "hits" in str(result), True
        assert result.total == 0
        assert len(result.hits) == 0

    except Exception as exc:
        print("TEST EXCEPTION", exc)
        assert False, f"'test_search_should__not_find' raised an exception {exc}"


def test_get_html(key="6437b93761fcc7e355878e90"):
    try:
        c = client.Client(api_key=config.API_KEY)
        result = c.get_document_html(key)

        # compute sha1sum over result
        import hashlib
        sha1sum = hashlib.sha1(result.encode()).hexdigest()

        assert "a092ced214da10c9c63293ff9489332f655f2dd7" in sha1sum

    except Exception as exc:
        print("TEST EXCEPTION", exc)
        assert False, f"'test_get_html' raised an exception {exc}"


def test_find_btc_should_find(wallet="114qvtyucvKtiNXy9UL3eYx6HPYmadxeM4"):
    try:
        c = client.Client(api_key=config.API_KEY)
        result = c.find_wallet("BTC", wallet)

        assert "total" in str(result), True
        assert "hits" in str(result), True
        assert result.total > 0
        assert len(result.hits) > 0

    except Exception as exc:
        print("TEST EXCEPTION", exc)
        assert False, f"'test_find_btc_should_find' raised an exception {exc}"


def test_find_btc_should_not_find(address="notvalidaddress"):
    try:
        c = client.Client(api_key=config.API_KEY)
        result = c.find_wallet("BTC", address)

        assert "total" in str(result), True
        assert "hits" in str(result), True
        assert result.total == 0
        assert len(result.hits) == 0

    except Exception as exc:
        print("TEST EXCEPTION", exc)
        assert False, f"'test_find_btc_should_not_find' raised an exception {exc}"


def test_invalid_apikey():
    try:
        client.Client(api_key="invalid api key")
    except Exception as e:
        assert type(e) is Error  # TODO Validate 403
