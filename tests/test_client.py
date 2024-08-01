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


def test_get_tag_should_find(tag='dark-web:topic="hacking"'):
    try:
        c = client.Client(api_key=config.API_KEY)
        result = c.get_tag(tag)

        assert "total" in str(result), True
        assert "hits" in str(result), True
        assert result.total > 0
        assert len(result.hits) > 0

    except Exception as exc:
        print("TEST EXCEPTION", exc)
        assert False, f"'test_get_tag_should_find' raised an exception {exc}"


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


def test_phone_should_find(country_code="1", phone="200080426"):
    try:
        c = client.Client(api_key=config.API_KEY)
        result = c.find_phone(country_code, phone)

        assert "total" in str(result), True
        assert "hits" in str(result), True
        assert result.total > 0
        assert len(result.hits) > 0
    
    except Exception as exc:
        print("TEST EXCEPTION", exc)
        assert False, f"'test_phone_should_find' raised an exception {exc}"



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


def test_search_ransomware_victim_should_find(key="alvac"):
    try:
        c = client.Client(api_key=config.API_KEY)
        result = c.search_ransomware_victim(key)

        assert "total" in str(result), True
        assert "hits" in str(result), True
        assert result.total == 1
        assert len(result.hits) > 0
    except Exception as exc:
        print("TEST EXCEPTION", exc)
        assert (
            False
        ), f"'test_search_ransomware_victim_should_find' raised an exception {exc}"


def test_search_ransomware_victim_should_not_find(key="UAH1"):
    try:
        c = client.Client(api_key=config.API_KEY)
        result = c.search_ransomware_victim(key)

        assert "total" in str(result), True
        assert "hits" in str(result), True
        assert result.total == 0
        assert len(result.hits) == 0
    except Exception as exc:
        print("TEST EXCEPTION", exc)
        assert (
            False
        ), f"'test_search_ransomware_victim_should_not_find' raised an exception {exc}"


def test_get_ransomware_victim(key="64abc305e7f72075c8b582c2"):
    try:
        c = client.Client(api_key=config.API_KEY)
        result = c.get_ransomware_victim(key)

        assert "total" in str(result), True
        assert "hits" in str(result), True
        assert result.total == 1
        assert len(result.hits) > 0
    except Exception as exc:
        print("TEST EXCEPTION", exc)
        assert False, f"'test_get_ransomware_victim' raised an exception {exc}"


def test_ransomware_countries_stats():
    try:
        c = client.Client(api_key=config.API_KEY)
        result = c.ransomware_countries_stats()

        assert "total" in str(result), True
        assert "hits" in str(result), True
        assert result.total == 10000
        assert len(result.hits) > 0
    except Exception as exc:
        print("TEST EXCEPTION", exc)
        assert False, f"'test_ransomware_countries_stats' raised an exception {exc}"


def test_ransomware_groups_stats():
    try:
        c = client.Client(api_key=config.API_KEY)
        result = c.ransomware_groups_stats()

        assert "total" in str(result), True
        assert "hits" in str(result), True
        assert result.total == 10000
        assert len(result.hits) > 0
    except Exception as exc:
        print("TEST EXCEPTION", exc)
        assert False, f"'test_ransomware_groups_stats' raised an exception {exc}"


def test_ransmoware_attacks_stats():
    try:
        c = client.Client(api_key=config.API_KEY)
        result = c.ransomware_attacks_stats()

        assert "total" in str(result), True
        assert "hits" in str(result), True
        assert result.total == 10000
        assert len(result.hits) > 0
    except Exception as exc:
        print("TEST EXCEPTION", exc)
        assert False, f"'test_ransmoware_attacks_stats' raised an exception {exc}"


def test_im_telegram_search(platform="telegram", key="madrid"):
    try:
        c = client.Client(api_key=config.API_KEY)
        result = c.search_im(platform, key)

        assert "total" in str(result), True
        assert "hits" in str(result), True
        assert result.total >= 18
        assert len(result.hits) > 0
    except Exception as exc:
        print("TEST EXCEPTION", exc)
        assert False, f"'test_im_telegram_search' raised an exception {exc}"


def test_get_im_chat(platform="telegram", key="-1002018336281"):
    try:
        c = client.Client(api_key=config.API_KEY)
        result = c.get_im_chat(platform, key)

        assert "total" in str(result), True
        assert "hits" in str(result), True
        assert len(result.hits) > 0
    except Exception as exc:
        print("TEST EXCEPTION", exc)
        assert False, f"'test_get_im_chat' raised an exception {exc}"


def test_get_im_profile(platform="telegram", key="609517172"):
    try:
        c = client.Client(api_key=config.API_KEY)
        result = c.get_im_profile(platform, key)

        assert "total" in str(result), True
        assert "hits" in str(result), True
        assert result.total == 1
        assert len(result.hits) > 0
    except Exception as exc:
        print("TEST EXCEPTION", exc)
        assert False, f"'test_get_im_profile' raised an exception {exc}"


def test_get_im_message(platform="telegram", key="-1002018336281_46918"):
    try:
        c = client.Client(api_key=config.API_KEY)
        result = c.get_im_message(platform, key)

        assert "total" in str(result), True
        assert "hits" in str(result), True
        assert result.total == 1
        assert len(result.hits) > 0
    except Exception as exc:
        print("TEST EXCEPTION", exc)
        assert False, f"'test_get_im_message' raised an exception {exc}"


def test_get_im_channel(platform="telegram", key="-1001806390689"):
    try:
        c = client.Client(api_key=config.API_KEY)
        result = c.get_im_channel(platform, key)

        assert "total" in str(result), True
        assert "hits" in str(result), True
        assert result.total == 1
        assert len(result.hits) > 0
    except Exception as exc:
        print("TEST EXCEPTION", exc)
        assert False, f"'test_get_im_channel' raised an exception {exc}"


def test_invalid_apikey():
    try:
        client.Client(api_key="invalid api key")
    except Exception as e:
        assert type(e) is Error  # TODO Validate 403
