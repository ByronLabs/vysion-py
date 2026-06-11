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
                "id": "9e8e403c995a75cbf83a4f3603641727808a6d8d4ae7d2ae3b25c4a6f647314a",
                "companyName": "http://ramet-trom.co.il/",
                "companyLink": "http://ramet-trom.co.il/",
                "url": "http://incblog6qu4y4mm4zvw5nrmue6qbwtgjsxpw6b7ixzssu36tsajldoad.onion/blog/disclosures/69a4a7828f1d14b7438463a2",
                "ransomwareGroup": "Inc Ransom",
                "detectionDate": "2026-03-01T21:54:00",
                "text": "1 terabyte of data, blueprints, contracts and much more, not recognized by the israeli ministry of defense as a terrorist organization.",
                "country": "IL",
                "naics": "332999",
                "industry": "All Other Miscellaneous Fabricated Metal Product Manufacturing"
            },
            {
                "id": "22b72346742a9d93fc2249a5b0ffc9b0bc5af69f2636ff87df15ea4b5955ebd2",
                "companyName": "lke-group.com",
                "companyLink": "https://lke-group.com",
                "url": "http://incblog6qu4y4mm4zvw5nrmue6qbwtgjsxpw6b7ixzssu36tsajldoad.onion/blog/disclosures/69a499e68f1d14b743834763",
                "ransomwareGroup": "Inc Ransom",
                "detectionDate": "2026-03-01T20:56:00",
                "text": "LKE Group creates custom transport equipment for businesses across different industries. They design and build specialized gear that helps companies move materials, products, and goods more efficiently. From warehouse systems to industrial transport devices, LKE makes machines that solve real moving and handling challenges for factories, logistics centers, and manufacturing plants.Employees: 500Revenue: $30.4 MillionIndustry: Architecture, Engineering & DesignPhone Number: +49 23650000000Size: 800 GB +",
                "country": "DE",
                "naics": "212390",
                "industry": "Other Nonmetallic Mineral Mining and Quarrying"
            },
            {
                "id": "ac768e41360e0452784d9a731da4e6e818e9289c6e014cd9f9d7df67851c7ca5",
                "companyName": "DAINTY CLOUD INC",
                "companyLink": "",
                "url": "http://longcc4fqrfcqt5lzceutylaxir6h66fp6df3oin6mvwvz6pfdbxc6qd.onion/blog/0f09749244704dd7eda6e563ddd286eb4bd7ab0138dfefbc93a237c6179c0b21/",
                "ransomwareGroup": "Tengu",
                "detectionDate": "2026-03-01T09:06:46",
                "text": "DaintyCloud offers a variety of affordable virtual private server (VPS) solutions including Windows, Linux, and GPU servers across more than 34 data centers worldwide. Their services cater to clients who require high performance for applications such as gaming, video processing, and cloud computing. With competitive pricing and features like one-click deployment and easy management, DaintyCloud is geared towards both individual users and businesses seeking reliable cloud services. Additionally, they provide proxy services, ensuring clients have access to high-speed, dedicated IP options",
                "country": "",
                "naics": "",
                "industry": ""
            },
            {
                "id": "d2baaefeebd82682cd3da75dd4053200d22f79f016ca8f74cf05a912125f1b45",
                "companyName": "piglerautomation.com",
                "companyLink": "https://piglerautomation.com",
                "url": "http://incblog6qu4y4mm4zvw5nrmue6qbwtgjsxpw6b7ixzssu36tsajldoad.onion/blog/disclosures/69a38f9b8f1d14b7436e50f9",
                "ransomwareGroup": "Inc Ransom",
                "detectionDate": "2026-03-01T02:00:00",
                "text": "Pigler Automation specializes in Industrial Automation System Integration, helping clients streamline and modernize their operations to enhance efficiency and productivity. Their services include control system consultation, project planning, and support for various industries such as biopharma, oil and gas, and energy. With over 20 years of experience, their team of certified engineers offers expertise in SCADA design, PLC programming, and system integration. Pigler Automation aims to bridge the gap between legacy systems and cutting-edge automation, ensuring clients can optimize performance and stay ahead of industry challenges.Employees: 50Revenue: $5 MillionIndustry: Industrial Machinery & EquipmentPhone Number: (866) 871-1456",
                "country": "",
                "naics": "",
                "industry": ""
            },
            {
                "id": "c9f717d35ef8ed1a0a55dad889a4608ab3f89ebc7cd3c3d2122e80d501993a7d",
                "companyName": "Ricopia",
                "companyLink": "https://ricopia.com",
                "url": "http://tezwsse5czllksjb7cwp65rvnk4oobmzti2znn42i43bjdfd2prqqkad.onion/",
                "ransomwareGroup": "The Gentleman",
                "detectionDate": "2026-03-01T00:00:00",
                "text": "ricopia.com zoominfo.com/c/ricopia/405953806 Ricopia helps businesses upgrade their technology and work smarter. With over 100 tech experts, they've been helping companies of all sizes get better at digital tools for more than 30 years. They do this by checking how a company works, finding ways to improve technology, and helping teams learn new skills. Big names like ING Direct and BNP Paribas trust Ricopia to make their businesses run more smoothly and efficiently",
                "country": "US",
                "naics": "423420",
                "industry": "Office Equipment Merchant Wholesalers"
            },
            {
                "id": "b55df3c23a3283fa0a0e539232c156ab001740fdd2a2173a08720be9b54164db",
                "companyName": "Trinity Catholic High School",
                "companyLink": "https://www.trinitycatholichs.org",
                "url": "http://beast6azu4f7fxjakiayhnssybibsgjnmy77a6duufqw5afjzfjhzuqd.onion/card/trinity_catholic_high_school",
                "ransomwareGroup": "Beast",
                "detectionDate": "2026-03-01T00:00:00",
                "text": "Trinity Catholic High School offers a full array of co-curricular activities and sports programs. Our athletic programs include football, cheerleading, cross country, golf, swimming, tennis, weight lifting, basketball, volleyball, baseball, bowling, girls flag football, softball, lacrosse and track and field. Our State Championships include: football, women's soccer, baseball, wrestling and track.date: 01.03.2026\nrevenue: $6.5M\nwebsite: www.trinitycatholichs.org\ndata size: 500GB",
                "country": "",
                "naics": "",
                "industry": ""
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
    page = dto.Page(
        id="test-id",
        url=dto.URL.parse("https://vysion.ai"),
        language=None,
        detectionDate="2024-01-01T00:00:00",
        ingestionDate="2024-01-02T00:00:00",
        chunk=False,
    )
    assert page.detectionDate is not None
    assert page.ingestionDate is not None


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
