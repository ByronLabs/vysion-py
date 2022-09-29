import pytest
import vysion.dto as dto
from vysion.dto.util import MISPProcessor
from vysion.dto import (
    RansomFeedHit,
    Hit,
    URL,
    BaseModel
)
import json
from types import SimpleNamespace

##### FIXTURES #####

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
                    "country": "ES"
                },
                {
                    "id": "8848f137bbfb375fe0d96f3d6c8766a328f3aa1f9bce5f94230ec33ccdb1ae1f",
                    "company": "medcoenergi.com",
                    "company_link": "http://medcoenergi.com",
                    "link": "http://lockbitapt6vx57t3eeqjofwgcglmutr3a35nygvokja5uuccip4ykyd.onion/post/0I9Fe47C78Ms7Edp62a911ee5cb4e",
                    "group": "LockBit",
                    "date": "2022-06-20T22:54:00",
                    "info": "PT Medco Energi Internasional Tbk or MedcoEnergi is a public stock listed Indonesian oil and gas company. The company operates in Trading and Holding & Related Operations, Exploration for and Producti...",
                    "country": "EN"
                },
                {
                    "id": "f4d6fb7a1c2d0f10674db63a282387a837a1a2ffd568d73101dbdf354a738695",
                    "company": "hyatts.com",
                    "company_link": "http://hyatts.com",
                    "link": "http://lockbitapt6vx57t3eeqjofwgcglmutr3a35nygvokja5uuccip4ykyd.onion/post/LCYf0rDLKshIpIyd629dbbecf3e39",
                    "group": "LockBit",
                    "date": "2022-06-20T08:31:00",
                    "info": "Hyatts - All Things Creative · ART - Artist Supplies and Picture Framing · PANTONE - Color Matching Products · SIGN - Computer Signmaking Equipment and Supplies.",
                    "country": "EN"

                },
                {
                    "id": "6c09a9ae88e5f1d98121f98634e585b4639880ba29a0d2113a221bdb6c74fd95",
                    "company": "ptg.com.au",
                    "company_link": "http://ptg.com.au",
                    "link": "http://lockbitapt6vx57t3eeqjofwgcglmutr3a35nygvokja5uuccip4ykyd.onion/post/PHj2POP43RLNkKiR62a6d75655d74",
                    "group": "LockBit",
                    "date": "2022-06-20T06:18:00",
                    "info": "ptg.com.au",
                    "country": "EN"
                },
                {
                    "id": "256a0f4b6336f847a2dc557ed9daf9fb8b9dfd7b23137102c8918ea651fb4d57",
                    "company": "Van Ausdall & Farrar, inc",
                    "company_link": "http://https://vanausdall.com/",
                    "link": "http://lorenzmlwpzgxq736jzseuterytjueszsvznuibanxomlpkyxk6ksoyd.onion/",
                    "group": "Lorenz",
                    "date": "2022-06-20T00:00:00",
                    "info": "Loading ...\nUploading ...\n\nContact us",
                    "country": "EN"
                }
            ]
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
                            "protocol": "http",
                            "domain": "deepv2w7p33xa4pwxzwi2ps4j62gfxpyp44ezjbmpttxz3owlsp4ljid.onion",
                            "port": 80,
                            "path": "/show.php",
                            "signature": "68239670191c0af7218275274376ff43",
                            "network": "tor",
                        },
                        "parent": "55e14463b7addf8f5cdbb4ea1372f74f",
                        "title": "DeepPaste V3",
                        "language": "en",
                        "html": "<!DOCTYPE html>\r\n<html>\r\n    <head>\r\n        <meta http-equiv=\"content-type\" content=\"text/html; charset=UTF-8\">\r\n        <title>DeepPaste V3</title>\r\n        <meta charset=\"utf-8\">\r\n        <link rel=\"icon\" type=\"image/png\" href=\"favicon.ico\"/>\r\n        <meta name=\"description\" content=\"The Dark Unconsored Pastebin\">\r\n        <meta name=\"author\" content=\"DeepPaste\">\r\n        <meta name=\"keywords\" content=\"DeepPaste, pastebin, deepweb, darknet, deeppaste, text, share, publish, simple, comments, community, anonymous\">\r\n        <link href=\"style.css\" type=\"text/css\" rel=\"stylesheet\">\r\n    </head>\r\n    <body>\r\n\r\n<span style=\"float: right; \">Hello Anon - <a href=\"account.php\">Login</a></span><br>        \r\n        <a href=\"index.php\"><h1>DeepPaste V3</h1></a>\r\n        <h3>Your Deep-Shit Hoster for special shit</h3>\r\n\r\n        \r\n        <br>\r\n        Results for 5b345bec94f8b364cfe6adb4060a3165:\r\n        <br><hr>\r\n        <h3>Red room and Snuff for you</h3>\r\n        <p style=\"font-size: 0.7em; margin-top: -30px; margin-bottom: 5px;\">Anon, June 11, 2021 - 12:05</p>\r\n        <textarea class=\"boxes\" rows=\"30\" cols=\"110\" readonly=\"readonly\">VIDEO FILMED ACCORDING TO YOUR SCRIPT with tortue/rape/snuff/etc\r\nWe need from you how many actors will be, race, gender and your script/scenario.\r\nThe youngest actor we have - 4 days after he is born.\r\nThe oldest actor we have - 93 year old woman.\r\nproof:\r\ngffi27vwr36xdxfceft52f46dj25zghtmkzi7afj53gfgh3dykbfsgad.onion/images/8424f148911df4103e5d4eab55d109da.jpg\r\ngffi27vwr36xdxfceft52f46dj25zghtmkzi7afj53gfgh3dykbfsgad.onion/images/55129bcbe63072228379058370d34344.jpg\r\ngffi27vwr36xdxfceft52f46dj25zghtmkzi7afj53gfgh3dykbfsgad.onion/images/3ad8b829fbe358d333f510e1ae32450d.jpg\r\ngffi27vwr36xdxfceft52f46dj25zghtmkzi7afj53gfgh3dykbfsgad.onion/images/44943f9a72ab638dd45fd0c97808eada.jpg\r\ngffi27vwr36xdxfceft52f46dj25zghtmkzi7afj53gfgh3dykbfsgad.onion/images/237dbc5d229887180af129043d37051b.jpg\r\ngffi27vwr36xdxfceft52f46dj25zghtmkzi7afj53gfgh3dykbfsgad.onion/images/f0bfb9c8bd73ed15360b481d6217724d.jpg\r\n\r\nCONTACT: someonedeep@protonmail.com OR better use Pidgin (or other client) using encryption: som3on3@xmpp.jp\r\nONLY SERIOUS CUSTOMERS!</textarea>\r\n        <p>\r\n            Views: 48945 &nbsp; | &nbsp;Voting: 0 &nbsp;\r\n                            <span style=\"color: #060;\" href=\"\">↑ Up &nbsp; ↓ Down<br>\r\n                    <span style=\"font-size: 0.5em; padding-left: 110px;\">Login to vote</span>\r\n                </span>\r\n                        </p>\r\n        Comments:<br><br>\r\n                                <span>Anon, August 19, 2021 - 20:54</span><br>\r\n                        <textarea class=\"boxes\" rows=\"8\" cols=\"80\" readonly=\"readonly\"> \r\nHi we want to hire a Red Room done as entertainment at our wedding can you please tell me how we can arrange this?  There will be about 150 guests watching.  It's ok to livestream or video for profit. </textarea><br><br>\r\n                                                <span>Anon, August 19, 2021 - 21:23</span><br>\r\n                        <textarea class=\"boxes\" rows=\"8\" cols=\"80\" readonly=\"readonly\"> My husband says I'm ready for the red room?  Can you help me? sarah_edelmann@fastmail.fm\r\n\r\nhttp://oju4yn237c6hjh42qothvpreqecnqjhtvh4sgn3fqmsdvhu5d5tyspid.onion/i/1fdg4jc65.jpg </textarea><br><br>\r\n                                                <span>Anon, September 27, 2021 - 14:26</span><br>\r\n                        <textarea class=\"boxes\" rows=\"8\" cols=\"80\" readonly=\"readonly\"> bad things here >> Quote 'RED' >> telegram @sheinabox </textarea><br><br>\r\n                                                <span>Anon, October 06, 2021 - 18:52</span><br>\r\n                        <textarea class=\"boxes\" rows=\"8\" cols=\"80\" readonly=\"readonly\"> Nu nahuj v pizdu ce vse! </textarea><br><br>\r\n                                                <span>Anon, April 21, 2022 - 13:01</span><br>\r\n                        <textarea class=\"boxes\" rows=\"8\" cols=\"80\" readonly=\"readonly\"> 1 </textarea><br><br>\r\n                                                <span>Anon, May 25, 2022 - 14:06</span><br>\r\n                        <textarea class=\"boxes\" rows=\"8\" cols=\"80\" readonly=\"readonly\"> jwrjhbd\r\n </textarea><br><br>\r\n                                __________________________________<br>\r\n        <div>\r\n            <form action=\"show.php?md5=5b345bec94f8b364cfe6adb4060a3165\" method=\"post\">\r\n                <br>\r\n                Add a comment:\r\n                <br>\r\n                <span style=\"font-size: 0.9em;\">Name: Anon<br>\r\n                    <textarea class=\"boxes\" rows=\"8\" cols=\"80\" name=\"msg\" maxlength=\"580\"></textarea>\r\n                    <br><br><img src=\"deep/captcha.php?rand=680341357\">  <br>\r\n                    <span style=\"font-size: large;\">Captcha:</span>\r\n                    <input class=\"boxes\" type=\"text\" style=\"text-align: center;\" maxlength=\"8\" name=\"captcha_code\" required>\r\n                    <input class=\"hidden\" type=\"hidden\" name=\"md5\" value=\"5b345bec94f8b364cfe6adb4060a3165\">\r\n                    <input class=\"hidden\" type=\"hidden\" name=\"user\" value=\"Anon\">\r\n                    <br>\r\n                    <input class=\"boxes\" type=\"submit\" value=\" Add comment... \">\r\n                </span>\r\n            </form>\r\n        </div>\r\n        <br>\r\n        <br>\r\n\r\n                <a href=\"last.php\">Last Public Pastes</a><br>\r\n        <a href=\"top.php\">Top Last Public Pastes</a><br>\r\n        <a href=\"show.php\">Search Pastes...</a> <br>\r\n        <a href=\"info.html\">Infos about DeepPaste</a><br>\r\n        <br>\r\n        <span style=\"font-size: 0.5em;\">For new tea:<br>BTC: 3Eb3hBRKQNJfoa3TTALxx46coWKnfieUeF</span><br>\r\n        <span style=\"font-size: 0.5em;\">Views Today: 330.138 - Views Yesterday: 226.887</span>\r\n        <br>\r\n        <br>\r\n    </body>\r\n</html>\r\n",
                        "sha1sum": "a561d3a58d6e66c4248f111c9c285898f69e66cc",
                        "sha256sum": "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
                        "ssdeep": "96:v/oWfI68To5FZbLqhsYMErZ21+MpLUYvoyYIwu/pra:HoWSTo5j+wejd1uhu",
                        "date": "2022-06-04T00:09:47.461424",
                        "chunk": False
                    },
                    "email": [
                        {
                            "value": "someonedeep@protonmail.com"
                        },
                        {
                            "value": "som3on3@xmpp.jp"
                        },
                        {
                            "value": "sarah_edelmann@fastmail.fm"
                        }
                    ],
                    "paste": [],
                    "skype": [],
                    "telegram": [],
                    "whatsapp": [],
                    "bitcoin_address": [],
                    "polkadot_address": [],
                    "ethereum_address":[],
                    "monero_address": [],
                    "ripple_address": [],
                    "zcash_address": [],
                    "tag": "",
                }
            ]
        }
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
    url = dto.URL.parse("https://vysyion.ai")


def test_page():
    pass


def test_hit(get_document_fixture):
    processor = MISPProcessor()
    raw_hits = get_document_fixture["data"]["hits"]
    hits: Hit = []
    try:
        for raw_hit in raw_hits:
            hit: Hit = json.loads(json.dumps(raw_hit), object_hook=lambda d: SimpleNamespace(**d))

            url = URL(
                protocol="http",
                domain="deepv2w7p33xa4pwxzwi2ps4j62gfxpyp44ezjbmpttxz3owlsp4ljid",
                port=80,
                path="/show.php",
                signature="68239670191c0af7218275274376ff43",
                network="tor"
            )
            
            hit.page.url = url
            
            hits.append(hit)
        for hit in hits:
            processor.parse_hit(hit)
    except Exception as exc:
        print("TEST EXCEPTION", exc)
        assert False, f"'test_hit' raised an exception {exc}"
    pass


def test_ransom_feed_hit(get_ransom_feed_fixture):

    processor = MISPProcessor()
    raw_hits = get_ransom_feed_fixture["data"]["hits"]
    hits = []

    try:
        for raw_hit in raw_hits:
            hit: RansomFeedHit = json.loads(json.dumps(raw_hit), object_hook=lambda d: SimpleNamespace(**d))
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
