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
            "total": 5,
            "hits": [
                {
                    "id": "8c9f21ef102d118808f130ea3e2207bf36ae7217bae6ef88064d9bd53edadab7",
                    "company": "kansashighwaypatrol.org",
                    "company_link": "http://kansashighwaypatrol.org",
                    "link": "http://lockbitapt6vx57t3eeqjofwgcglmutr3a35nygvokja5uuccip4ykyd.onion/post/ZXIuZfPw887fteYK629cfb250d22e",
                    "group": "LockBit",
                    "date": "2022-06-20T23:48:00",
                    "info": "Contact Us General Headquarters 122 SW 7th Street Topeka, KS 66603 Report a road hazard or erratic driver: Call *47, or *KTA (Turnpike) Emergency: 911 Questions: 78...",
                    "country": "ES",
                },
                {
                    "id": "8848f137bbfb375fe0d96f3d6c8766a328f3aa1f9bce5f94230ec33ccdb1ae1f",
                    "company": "medcoenergi.com",
                    "company_link": "http://medcoenergi.com",
                    "link": "http://lockbitapt6vx57t3eeqjofwgcglmutr3a35nygvokja5uuccip4ykyd.onion/post/0I9Fe47C78Ms7Edp62a911ee5cb4e",
                    "group": "LockBit",
                    "date": "2022-06-20T22:54:00",
                    "info": "PT Medco Energi Internasional Tbk or MedcoEnergi is a public stock listed Indonesian oil and gas company. The company operates in Trading and Holding & Related Operations, Exploration for and Producti...",
                    "country": "EN",
                },
                {
                    "id": "f4d6fb7a1c2d0f10674db63a282387a837a1a2ffd568d73101dbdf354a738695",
                    "company": "hyatts.com",
                    "company_link": "http://hyatts.com",
                    "link": "http://lockbitapt6vx57t3eeqjofwgcglmutr3a35nygvokja5uuccip4ykyd.onion/post/LCYf0rDLKshIpIyd629dbbecf3e39",
                    "group": "LockBit",
                    "date": "2022-06-20T08:31:00",
                    "info": "Hyatts - All Things Creative · ART - Artist Supplies and Picture Framing · PANTONE - Color Matching Products · SIGN - Computer Signmaking Equipment and Supplies.",
                    "country": "EN",
                },
                {
                    "id": "6c09a9ae88e5f1d98121f98634e585b4639880ba29a0d2113a221bdb6c74fd95",
                    "company": "ptg.com.au",
                    "company_link": "http://ptg.com.au",
                    "link": "http://lockbitapt6vx57t3eeqjofwgcglmutr3a35nygvokja5uuccip4ykyd.onion/post/PHj2POP43RLNkKiR62a6d75655d74",
                    "group": "LockBit",
                    "date": "2022-06-20T06:18:00",
                    "info": "ptg.com.au",
                    "country": "EN",
                },
                {
                    "id": "256a0f4b6336f847a2dc557ed9daf9fb8b9dfd7b23137102c8918ea651fb4d57",
                    "company": "Van Ausdall & Farrar, inc",
                    "company_link": "http://https://vanausdall.com/",
                    "link": "http://lorenzmlwpzgxq736jzseuterytjueszsvznuibanxomlpkyxk6ksoyd.onion/",
                    "group": "Lorenz",
                    "date": "2022-06-20T00:00:00",
                    "info": "Loading ...\nUploading ...\n\nContact us",
                    "country": "EN",
                },
            ],
        }
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
                    "topic": [],
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
