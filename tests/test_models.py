import pytest

import vysion.dto as dto


def test_invalid():
    try:
        dto.wrong()
        assert False
    except:
        assert True

def test_email():
    pass

def test_paste():
    pass

def test_skype():
    pass

def test_telegram():
    pass

def test_bitcoin_address():
    pass

def test_whatsapp():
    pass

def test_url():
    url = dto.URL.parse("https://vysyion.ai")

def test_page():
    pass

def test_hit():
    pass


def test_ransom_feed_hit():
    pass


def test_result():
    pass


def test_vysion_error():
    # class StatusCode(int, Enum):
    pass
