#!/usr/bin/env python3
"""
Copyright 2022 ByronLabs S.L.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from vysion.taxonomy.flavours import (
    MISP,
    DBSafe,
    EmptyFlavour,
    Flavours,
    Vysion,
)

"""
    
    # Vysion taxonomy 1.0

    Siguiendo metodología de MISP:

    - https://github.com/MISP/misp-taxonomies/blob/main/tools/docs/images/taxonomy-explanation.png?raw=true

    Tratar de ajustarse a los nombres ("value") que utilicen ellos.

    Predicados propios

    
    ## ENTITY TEMPLATE
    
    class Template(Entity):

        _flavours = Flavours(
            vysion=Vysion(namespace="vysion", predicate="api", value="template"),
            dbsafe=EmptyFlavour(),
            misp=EmptyFlavour,
            stix=EmptyFlavour(),
            case=EmptyFlavour()
        )

"""


class Field:
    pass


# class Username(TimedItem):
#     name = scrapy.Field()
#     # TODO Comentado en previsión de mejorar la regex
#     # found_at = scrapy.Field()

# class Keyword(TimedItem):
#     value = scrapy.Field()
#     found_at = scrapy.Field()


# class TwitterUsername(TimedItem):
#     name = scrapy.Field()
#     found_at = scrapy.Field()

# class Discord_URL(TimedItem):
#     address = scrapy.Field()
#     found_at = scrapy.Field()

# class Metadata(TimedItem):
#     file_name = scrapy.Field()
#     file_type = scrapy.Field()
#     signature_without_metadata = scrapy.Field()
#     signature = scrapy.Field()
#     raw_metadata = scrapy.Field()
#     found_at = scrapy.Field()

# class Keyword(Item):
#     pass


# class Bitname_URL(Item):
#     pass


# class IPFS_URL(Item):
#     pass


# class Username(Item):
#     pass


# class Base64(Item):
#     pass


# class OwnName(Item):
#     pass

# class MD5(Item):
#     pass

# class SHA1(Item):
#     pass

# class SHA256(Item):
#     pass


class Entity:

    _flavours: Flavours = None

    def __init_subclass__(cls) -> None:

        super().__init_subclass__()

        assert cls._flavours is not None

        for flavour in cls._flavours.get_flavours():
            assert flavour is not None


# class XMR


class Bitcoin_Address(Entity):

    _flavours = Flavours(
        vysion=Vysion("digital-asset", "cryptocurrency", "bitcoin_address"),
        dbsafe=DBSafe("vysion", "automatic-detection", "bitcoin-address"),
        misp=MISP("infoleak", "automatic-detection", "bitcoin-address"),
        stix=EmptyFlavour(),
        case=EmptyFlavour(),
    )


class Binance_Address(Entity):

    _flavours = Flavours(
        vysion=Vysion("digital-asset", "cryptocurrency", "binance_address"),
        dbsafe=DBSafe("vysion", "automatic-detection", "binance-address"),
        misp=EmptyFlavour(),
        stix=EmptyFlavour(),
        case=EmptyFlavour(),
    )


class Polkadot_Address(Entity):

    _flavours = Flavours(
        vysion=Vysion("digital-asset", "cryptocurrency", "polkadot_address"),
        dbsafe=DBSafe("vysion", "automatic-detection", "polkadot-address"),
        misp=EmptyFlavour(),
        stix=EmptyFlavour(),
        case=EmptyFlavour(),
    )

    address = Field()
    found_at = Field()


class Ethereum_Address(Entity):

    _flavours = Flavours(
        vysion=Vysion("digital-asset", "cryptocurrency", "ethereum_address"),
        dbsafe=DBSafe("vysion", "automatic-detection", "ethereum-address"),
        misp=EmptyFlavour(),
        stix=EmptyFlavour(),
        case=EmptyFlavour(),
    )

    address = Field()
    found_at = Field()


class Monero_Address(Entity):

    _flavours = Flavours(
        vysion=Vysion("digital-asset", "cryptocurrency", "monero_address"),
        dbsafe=DBSafe("vysion", "automatic-detection", "monero-address"),
        misp=EmptyFlavour(),
        stix=EmptyFlavour(),
        case=EmptyFlavour(),
    )

    address = Field()
    found_at = Field()


class Ripple_Address(Entity):

    _flavours = Flavours(
        vysion=Vysion("digital-asset", "cryptocurrency", "ripple_address"),
        dbsafe=DBSafe("vysion", "automatic-detection", "ripple-address"),
        misp=EmptyFlavour(),
        stix=EmptyFlavour(),
        case=EmptyFlavour(),
    )

    address = Field()
    found_at = Field()


class Zcash_Address(Entity):

    _flavours = Flavours(
        vysion=Vysion("digital-asset", "cryptocurrency", "zcash_address"),
        dbsafe=DBSafe("vysion", "automatic-detection", "zcash-address"),
        misp=EmptyFlavour(),
        stix=EmptyFlavour(),
        case=EmptyFlavour(),
    )

    address = Field()
    found_at = Field()


class Tor_Domain_v3(Entity):

    _flavours = Flavours(
        vysion=Vysion("darknet", "tor", "onion_v3"),
        dbsafe=DBSafe("vysion", "automatic-detection", "url"),
        misp=MISP("infoleak", "automatic-detection", "onion"),
        stix=EmptyFlavour(),
        case=EmptyFlavour(),
    )


class Tor_Domain_v2(Entity):

    _flavours = Flavours(
        vysion=Vysion("darknet", "tor", "onion_v2"),
        dbsafe=DBSafe("vysion", "automatic-detection", "url"),
        misp=MISP("infoleak", "automatic-detection", "onion"),
        stix=EmptyFlavour(),
        case=EmptyFlavour(),
    )


class I2P_Domain(Entity):

    _flavours = Flavours(
        vysion=Vysion("darknet", "i2p", "i2p"),
        dbsafe=EmptyFlavour(),
        misp=EmptyFlavour(),
        stix=EmptyFlavour(),
        case=EmptyFlavour(),
    )


class I2P_B32_Domain(Entity):

    _flavours = Flavours(
        vysion=Vysion("darknet", "i2p", "i2p-b32"),
        dbsafe=EmptyFlavour(),
        misp=EmptyFlavour(),
        stix=EmptyFlavour(),
        case=EmptyFlavour(),
    )


class ZeroNet(Entity):

    _flavours = Flavours(
        vysion=Vysion("network", "darknet", "zeronet"),
        dbsafe=EmptyFlavour(),
        misp=EmptyFlavour(),
        stix=EmptyFlavour(),
        case=EmptyFlavour(),
    )


class ZeroNet_Bit_Domain(Entity):

    _flavours = Flavours(
        vysion=Vysion("darknet", "zeronet", "zeronet-bit"),
        dbsafe=EmptyFlavour(),
        misp=EmptyFlavour(),
        stix=EmptyFlavour(),
        case=EmptyFlavour(),
    )


class ZeroNet_PK_Domain(Entity):

    _flavours = Flavours(
        vysion=Vysion("darknet", "zeronet", "zeronet-pk"),
        dbsafe=EmptyFlavour(),
        misp=EmptyFlavour(),
        stix=EmptyFlavour(),
        case=EmptyFlavour(),
    )


class Freenet_SSK_Domain(Entity):

    _flavours = Flavours(
        vysion=Vysion("darknet", "freenet", "freenet-ssk"),
        dbsafe=EmptyFlavour(),
        misp=EmptyFlavour(),
        stix=EmptyFlavour(),
        case=EmptyFlavour(),
    )


class Freenet_CHK_Domain(Entity):

    _flavours = Flavours(
        vysion=Vysion("darknet", "freenet", "freenet-chk"),
        dbsafe=EmptyFlavour(),
        misp=EmptyFlavour(),
        stix=EmptyFlavour(),
        case=EmptyFlavour(),
    )


class URL(Entity):

    _flavours = Flavours(
        vysion=EmptyFlavour(),
        dbsafe=DBSafe("parche", "automatic-detection", "url"),
        misp=EmptyFlavour(),
        stix=EmptyFlavour(),
        case=EmptyFlavour(),
    )


class HTML(Entity):

    _flavours = Flavours(
        vysion=EmptyFlavour(),
        dbsafe=DBSafe("vysion", "automatic-detection", "html"),
        misp=MISP("file-type", "type", "html"),
        stix=EmptyFlavour(),
        case=EmptyFlavour(),
    )


class Location(Entity):

    _flavours = Flavours(
        vysion=EmptyFlavour(),
        dbsafe=DBSafe("vysion", "automatic-detection", "location-addresss"),
        misp=MISP("gea-nz-entities", "places-address-type", "location-addresss"),
        stix=EmptyFlavour(),
        case=EmptyFlavour(),
    )


class Business(Entity):

    _flavours = Flavours(
        vysion=EmptyFlavour(),
        dbsafe=DBSafe("vysion", "automatic-detection", "business"),
        misp=MISP("stix-ttp", "victim-targeting", "business-professional-sector"),
        stix=EmptyFlavour(),
        case=EmptyFlavour(),
    )


class PhoneNumber(Entity):

    _flavours = Flavours(
        vysion=Vysion("finding", "id", "phone-number"),
        dbsafe=DBSafe("vysion", "automatic-detection", "phone-number"),
        misp=MISP("infoleak", "automatic-detection", "phone-number"),
        stix=EmptyFlavour(),
        case=EmptyFlavour(),
    )


class Password(Entity):

    _flavours = Flavours(
        vysion=EmptyFlavour(),
        dbsafe=DBSafe("vysion", "automatic-detection", "password"),
        misp=EmptyFlavour(),
        stix=EmptyFlavour(),
        case=EmptyFlavour(),
    )


class SeedPhrase(Entity):

    _flavours = Flavours(
        vysion=EmptyFlavour(),
        dbsafe=DBSafe("vysion", "automatic-detection", "seed-phrase"),
        misp=EmptyFlavour(),
        stix=EmptyFlavour(),
        case=EmptyFlavour(),
    )


class Email(Entity):

    _flavours = Flavours(
        vysion=Vysion("finding", "id", "email"),
        dbsafe=DBSafe("vysion", "automatic-detection", "email"),
        misp=EmptyFlavour(),
        stix=EmptyFlavour(),
        case=EmptyFlavour(),
    )


class Pastebin(Entity):

    _flavours = Flavours(
        vysion=Vysion("network", "paste", "pastebin"),
        dbsafe=EmptyFlavour(),
        misp=EmptyFlavour(),
        stix=EmptyFlavour(),
        case=EmptyFlavour(),
    )


class JustPaste(Entity):

    _flavours = Flavours(
        vysion=Vysion("network", "paste", "justpaste"),
        dbsafe=EmptyFlavour(),
        misp=EmptyFlavour(),
        stix=EmptyFlavour(),
        case=EmptyFlavour(),
    )


class IRC(Entity):

    _flavours = Flavours(
        vysion=Vysion("network", "im", "irc"),
        dbsafe=DBSafe("vysion", "automatic-detection", "internet-relay-chat"),
        misp=EmptyFlavour(),
        stix=EmptyFlavour(),
        case=EmptyFlavour(),
    )


class Skype(Entity):

    _flavours = Flavours(
        vysion=Vysion("network", "im", "skype"),
        dbsafe=DBSafe("vysion", "automatic-detection", "skype"),
        misp=EmptyFlavour(),
        stix=EmptyFlavour(),
        case=EmptyFlavour(),
    )


class PGPPublic(Entity):

    _flavours = Flavours(
        vysion=EmptyFlavour(),
        dbsafe=DBSafe("vysion", "automatic-detection", "pgp-public-key-block"),
        misp=MISP("infoleak", "automatic-detection", "pgp-public-key-block"),
        stix=EmptyFlavour(),
        case=EmptyFlavour(),
    )


class PGPPrivate(Entity):

    _flavours = Flavours(
        vysion=EmptyFlavour(),
        dbsafe=DBSafe("vysion", "automatic-detection", "pgp-private-key"),
        misp=MISP("infoleak", "automatic-detection", "pgp-private-key"),
        stix=EmptyFlavour(),
        case=EmptyFlavour(),
    )


class Tor(Entity):

    _flavours = Flavours(
        vysion=Vysion("network", "darknet", "tor"),
        dbsafe=EmptyFlavour(),
        misp=EmptyFlavour(),
        stix=EmptyFlavour(),
        case=EmptyFlavour(),
    )


class Telegram(Entity):

    _flavours = Flavours(
        vysion=Vysion("network", "im", "telegram"),
        dbsafe=DBSafe("vysion", "automatic-detection", "telegram"),
        misp=MISP(
            "DFRLab-dichotomies-of-disinformation", "platforms-messaging", "telegram"
        ),
        stix=EmptyFlavour(),
        case=EmptyFlavour(),
    )


class WhatsApp(Entity):

    _flavours = Flavours(
        vysion=Vysion("network", "im", "whatsapp"),
        dbsafe=DBSafe("vysion", "automatic-detection", "whatsapp"),
        misp=MISP(
            "DFRLab-dichotomies-of-disinformation", "platforms-messaging", "whatsapp"
        ),
        stix=EmptyFlavour(),
        case=EmptyFlavour(),
    )


class Discord(Entity):

    _flavours = Flavours(
        vysion=Vysion("network", "im", "discord"),
        dbsafe=DBSafe("vysion", "automatic-detection", "discord"),
        misp=EmptyFlavour(),
        stix=EmptyFlavour(),
        case=EmptyFlavour(),
    )
