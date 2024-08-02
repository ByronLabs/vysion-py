import json
from types import SimpleNamespace

import pytest

import vysion.dto as dto
from vysion.dto import URL, BaseModel, DocumentHit, RansomFeedHit
from vysion.dto.util import MISPProcessor


@pytest.fixture
def get_ransom_feed_fixture():
    ransom_feed = {
        "data": {
            "total": 6,
            "hits": [
                {
                    "id": "8c9f21ef102d118808f130ea3e2207bf36ae7217bae6ef88064d9bd53edadab7",
                    "companyName": "kansashighwaypatrol.org",
                    "companyLink": "http://kansashighwaypatrol.org",
                    "url": "http://lockbitapt6vx57t3eeqjofwgcglmutr3a35nygvokja5uuccip4ykyd.onion/post/ZXIuZfPw887fteYK629cfb250d22e",
                    "ransomwareGroup": "LockBit",
                    "detectionDate": "2022-06-20T23:48:00",
                    "text": "Contact Us General Headquarters 122 SW 7th Street Topeka, KS 66603 Report a road hazard or erratic driver: Call *47, or *KTA (Turnpike) Emergency: 911 Questions: 78...",
                    "country": "US",
                },
                {
                    "id": "8848f137bbfb375fe0d96f3d6c8766a328f3aa1f9bce5f94230ec33ccdb1ae1f",
                    "companyName": "medcoenergi.com",
                    "companyLink": "http://medcoenergi.com",
                    "url": "http://lockbitapt6vx57t3eeqjofwgcglmutr3a35nygvokja5uuccip4ykyd.onion/post/0I9Fe47C78Ms7Edp62a911ee5cb4e",
                    "ransomwareGroup": "LockBit",
                    "detectionDate": "2022-06-20T22:54:00",
                    "text": "PT Medco Energi Internasional Tbk or MedcoEnergi is a public stock listed Indonesian oil and gas company. The company operates in Trading and Holding & Related Operations, Exploration for and Producti...",
                    "country": None,
                },
                {
                    "id": "f4d6fb7a1c2d0f10674db63a282387a837a1a2ffd568d73101dbdf354a738695",
                    "companyName": "hyatts.com",
                    "companyLink": "http://hyatts.com",
                    "url": "http://lockbitapt6vx57t3eeqjofwgcglmutr3a35nygvokja5uuccip4ykyd.onion/post/LCYf0rDLKshIpIyd629dbbecf3e39",
                    "ransomwareGroup": "LockBit",
                    "detectionDate": "2022-06-20T08:31:00",
                    "text": "Hyatts - All Things Creative · ART - Artist Supplies and Picture Framing · PANTONE - Color Matching Products · SIGN - Computer Signmaking Equipment and Supplies.",
                    "country": None,
                },
                {
                    "id": "6c09a9ae88e5f1d98121f98634e585b4639880ba29a0d2113a221bdb6c74fd95",
                    "companyName": "ptg.com.au",
                    "companyLink": "http://ptg.com.au",
                    "url": "http://lockbitapt6vx57t3eeqjofwgcglmutr3a35nygvokja5uuccip4ykyd.onion/post/PHj2POP43RLNkKiR62a6d75655d74",
                    "ransomwareGroup": "LockBit",
                    "detectionDate": "2022-06-20T06:18:00",
                    "text": "ptg.com.au",
                    "country": "AU",
                },
                {
                    "id": "c99c65628f4f8579a8ebce2c2ca8aa5008b827f749f38093c8d67c581050c492",
                    "companyName": "LebensWohnArt",
                    "companyLink": "https://www.lebenswohnart.de/",
                    "url": "http://basemmnnqwxevlymli5bs36o5ynti55xojzvn246spahniugwkff2pad.onion/company/789095",
                    "ransomwareGroup": "8base",
                    "detectionDate": "2022-06-20T00:00:00",
                    "text": "We at the Lebens Wohn Art team have been working towards this goal since the opening of our first branch in Hamburg in 2003 for our clients.\nWith each of our products, we want to decorate your home so that you can not only live in it, but also enjoy it.\nIf you are looking for something special or individual that is not available on every corner, then you have come to the right place.\n\nhttps://www.lebenswohnart.de/\n\nWohnmeile Halstenbek\n(bei Hamburg)\nGärtnerstr.150\n25469 Halstenbek\nhttps://mega.nz/folder/cQIHEK7T#wLWTZ_CgJSkl6nCtxkf_BQ",
                    "country": "DE",
                },
                {
                    "id": "256a0f4b6336f847a2dc557ed9daf9fb8b9dfd7b23137102c8918ea651fb4d57",
                    "companyName": "Van Ausdall & Farrar, inc",
                    "companyLink": "http://https://vanausdall.com/",
                    "url": "http://lorenzmlwpzgxq736jzseuterytjueszsvznuibanxomlpkyxk6ksoyd.onion/",
                    "ransomwareGroup": "Lorenz",
                    "detectionDate": "2022-06-20T00:00:00",
                    "text": "Loading ...\nUploading ...\n\nContact us",
                    "country": None,
                },
            ],
        },
        "error": None,
    }

    return ransom_feed


@pytest.fixture
def get_document_fixture():
    raw_docuemnt = {
        "data": {
            "total": 1,
            "hits": [
                {
                    "page": {
                        "id": "629aa2cb91462d18a4b2a9cd",
                        "url": {
                            "url": "deepv2w7p33xa4pwxzwi2ps4j62gfxpyp44ezjbmpttxz3owlsp4ljid.onion/show.php",
                            "networkProtocol": "http",
                            "domainName": "deepv2w7p33xa4pwxzwi2ps4j62gfxpyp44ezjbmpttxz3owlsp4ljid.onion",
                            "port": 80,
                            "path": "/show.php",
                            "signature": "68239670-191c-0af7-2182-75274376ff43",
                            "network": "tor",
                        },
                        "foundAt": "55e14463b7addf8f5cdbb4ea1372f74f",
                        "pageTitle": "DeepPaste V3",
                        "language": "en",
                        "html": "",
                        "text": None,
                        "sha1sum": "a561d3a58d6e66c4248f111c9c285898f69e66cc",
                        "sha256sum": None,
                        "ssdeep": "96:v/oWfI68To5FZbLqhsYMErZ21+MpLUYvoyYIwu/pra:HoWSTo5j+wejd1uhu",
                        "detectionDate": "2022-06-04T00:09:47.461424",
                        "chunk": True,
                    },
                    "tag": [],
                    "email": [
                        {"value": "someonedeep@protonmail.com"},
                        {"value": "som3on3@xmpp.jp"},
                        {"value": "sarah_edelmann@fastmail.fm"},
                    ],
                    "paste": [],
                    "skype": [],
                    "telegram": [],
                    "whatsapp": [],
                    "bitcoin_address": [],
                    "polkadot_address": [],
                    "ethereum_address": [],
                    "monero_address": [],
                    "ripple_address": [],
                    "zcash_address": [],
                }
            ],
        },
        "error": None,
    }

    return raw_docuemnt


########


def test_invalid():
    try:
        dto.wrong()
        assert False
    except Exception as exc:
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
    try:
        url = dto.URL.parse("https://vysion.ai")
    except Exception as exc:
        print("TEST EXCEPTION", exc)
        assert False, f"'test_url' raised an exception {exc}"


def test_page():
    pass


def test_hit(get_document_fixture):
    processor = MISPProcessor()
    raw_hits = get_document_fixture["data"]["hits"]
    hits: DocumentHit = []
    try:
        for raw_hit in raw_hits:
            hit: DocumentHit = json.loads(
                json.dumps(raw_hit), object_hook=lambda d: SimpleNamespace(**d)
            )

            url = URL(
                networkProtocol="http",
                url="http://deepv2w7p33xa4pwxzwi2ps4j62gfxpyp44ezjbmpttxz3owlsp4ljid.onion/show.php",
                domainName="deepv2w7p33xa4pwxzwi2ps4j62gfxpyp44ezjbmpttxz3owlsp4ljid",
                port=80,
                path="/show.php",
                signature="68239670191c0af7218275274376ff43",
                network="tor",
            )

            hit.page.url = url

            hits.append(hit)
        for hit in hits:
            processor.parse_hit(hit)
    except Exception as exc:
        print("TEST EXCEPTION", exc)
        assert False, f"'test_hit' raised an exception {exc}"


def test_ransom_feed_hit(get_ransom_feed_fixture):
    processor = MISPProcessor()
    raw_hits = get_ransom_feed_fixture["data"]["hits"]
    hits = []

    try:
        for raw_hit in raw_hits:
            hit: RansomFeedHit = json.loads(
                json.dumps(raw_hit), object_hook=lambda d: SimpleNamespace(**d)
            )
        hits.append(hit)

        for hit in hits:
            processor.parse_ransom_feed_hit(hit)

    except Exception as exc:
        print("TEST EXCEPTION", exc)
        assert False, f"'parse_ransom_feed_hit' raised an exception {exc}"
    pass


def test_result():
    pass


def test_vysion_error():
    # class StatusCode(int, Enum):
    pass
