from tkinter import Entry
from .flavours import Flavours, EmptyFlavour, DBSafe, MISP, Vysion

'''
Vysion taxonomy 1.0
'''

class Field():
    pass

# class Phone(TimedItem):
#     number = scrapy.Field()
#     found_at = scrapy.Field()


# class Username(TimedItem):
#     name = scrapy.Field()
#     # TODO Comentado en previsión de mejorar la regex
#     # found_at = scrapy.Field()

# class Keyword(TimedItem):
#     value = scrapy.Field()
#     found_at = scrapy.Field()


# class BTCWallet(TimedItem):
#     address = scrapy.Field()
#     found_at = scrapy.Field()


# class TwitterUsername(TimedItem):
#     name = scrapy.Field()
#     found_at = scrapy.Field()


# class I2P_URL(TimedItem):
#     address = scrapy.Field()
#     found_at = scrapy.Field(default=None)


# class Tor_URL(TimedItem):
#     address = scrapy.Field()
#     found_at = scrapy.Field(default=None)


# class Freenet_URL(TimedItem):
#     address = scrapy.Field()
#     found_at = scrapy.Field(default=None)


# class Zeronet_URL(TimedItem):
#     address = scrapy.Field()
#     found_at = scrapy.Field(default=None)


# class Whatsapp_URL(TimedItem):
#     address = scrapy.Field()
#     found_at = scrapy.Field()


# class Telegram_URL(TimedItem):
#     address = scrapy.Field()
#     found_at = scrapy.Field()


# class Skype_URL(TimedItem):
#     address = scrapy.Field()
#     found_at = scrapy.Field()


# class Discord_URL(TimedItem):
#     address = scrapy.Field()
#     found_at = scrapy.Field()


# class Paste(TimedItem):
#     address = scrapy.Field()
#     found_at = scrapy.Field()


# class Metadata(TimedItem):
#     file_name = scrapy.Field()
#     file_type = scrapy.Field()
#     signature_without_metadata = scrapy.Field()
#     signature = scrapy.Field()
#     raw_metadata = scrapy.Field()
#     found_at = scrapy.Field()


# class Page(TimedItem):
#     title = scrapy.Field()
#     lang = scrapy.Field()
#     value = scrapy.Field()
#     sha1sum = scrapy.Field()
#     ssdeep = scrapy.Field()
#     found_at = scrapy.Field()

# class Phone(Item):
#     pass


# class Keyword(Item):
#     pass


# class TW_Account(Item):
#     pass


# class Bitname_URL(Item):
#     pass


# class IPFS_URL(Item):
#     pass


# class Username(Item):
#     pass


# class Password(Item):
#     pass


# class Base64(Item):
#     pass


# class OwnName(Item):
#     pass


# class Paste(Item):
#     pass

# class MD5(Item):
#     pass

# class SHA1(Item):
#     pass

# class SHA256(Item):
#     pass


class Entity:

    _flavours = None

    def __init_subclass__(cls) -> None:

        super().__init_subclass__()

        assert cls._flavours is not None

        for flavour in cls._flavours.get_flavours():
            assert flavour is not None


# class XMR

'''
    Siguiendo metodología de MISP:

    - https://github.com/MISP/misp-taxonomies/blob/main/tools/docs/images/taxonomy-explanation.png?raw=true

    Tratar de ajustarse a los nombres ("value") que utilicen ellos.

    Predicados propios
'''

'''
TEMPLATE ENTITY
'''
class Template(Entity):

    _flavours = Flavours(
        vysion=Vysion(namespace="vysion", predicate="api", value="template"),
        dbsafe=EmptyFlavour(),
        misp=EmptyFlavour,
        stix=EmptyFlavour(),
        case=EmptyFlavour()
    )


class Bitcoin_Address(Entity):

    _flavours = Flavours(
        vysion=Vysion("digital-asset", "cryptocoin", "bitcoin-address"),
        dbsafe=DBSafe("vysion", "automatic-detection", "bitcoin-address"),
        misp=MISP("infoleak", "automatic-detection", "bitcoin-address"),
        stix=EmptyFlavour(),
        case=EmptyFlavour()
    )

    address = Field()
    found_at = Field()


class Binance_Address(Entity):

    _flavours = Flavours(
        vysion=Vysion("digital-asset", "cryptocoin", "binance-address"),
        dbsafe=DBSafe("vysion", "automatic-detection", "binance-address"),
        misp=EmptyFlavour(),
        stix=EmptyFlavour(),
        case=EmptyFlavour()
    )

    address = Field()
    found_at = Field()


class Polkadot_Address(Entity):

    _flavours = Flavours(
        vysion=Vysion("digital-asset", "cryptocoin", "polkadot-address"),
        dbsafe=DBSafe("vysion", "automatic-detection", "polkadot-address"),
        misp=EmptyFlavour(),
        stix=EmptyFlavour(),
        case=EmptyFlavour()
    )

    address = Field()
    found_at = Field()


class Ethereum_Address(Entity):

    _flavours = Flavours(
        vysion=Vysion("digital-asset", "cryptocoin", "ethereum-address"),
        dbsafe=DBSafe("vysion", "automatic-detection", "ethereum-address"),
        misp=EmptyFlavour(),
        stix=EmptyFlavour(),
        case=EmptyFlavour()
    )

    address = Field()
    found_at = Field()


class Monero_Address(Entity):

    _flavours = Flavours(
        vysion=Vysion("digital-asset", "cryptocoin", "monero-address"),
        dbsafe=DBSafe("vysion", "automatic-detection", "monero-address"),
        misp=EmptyFlavour(),
        stix=EmptyFlavour(),
        case=EmptyFlavour()
    )

    address = Field()
    found_at = Field()


class Ripple_Address(Entity):

    _flavours = Flavours(
        vysion=Vysion("digital-asset", "cryptocoin", "ripple-address"),
        dbsafe=DBSafe("vysion", "automatic-detection", "ripple-address"),
        misp=EmptyFlavour(),
        stix=EmptyFlavour(),
        case=EmptyFlavour()
    )

    address = Field()
    found_at = Field()


class Zcash_Address(Entity):

    _flavours = Flavours(
        vysion=Vysion("digital-asset", "cryptocoin", "zcash-address"),
        dbsafe=DBSafe("vysion", "automatic-detection", "zcash-address"),
        misp=EmptyFlavour(),
        stix=EmptyFlavour(),
        case=EmptyFlavour()
    )

    address = Field()
    found_at = Field()


class Tor_Domain(Entity):

    _flavours = Flavours(
        vysion=Vysion("darknet", "tor", "onion-v3"),
        dbsafe=DBSafe("vysion", "automatic-detection", "url"),
        misp=MISP("infoleak", "automatic-detection", "onion"),
        stix=EmptyFlavour(),
        case=EmptyFlavour()
    )


class I2P_Domain(Entity):

    _flavours = Flavours(
        vysion=Vysion("darknet", "i2p", "i2p"),
        dbsafe=EmptyFlavour(),
        misp=EmptyFlavour(),
        stix=EmptyFlavour(),
        case=EmptyFlavour()
    )



class I2P_B32_Domain(Entity):

    _flavours = Flavours(
        vysion=Vysion("darknet", "i2p", "i2p-b32"),
        dbsafe=EmptyFlavour(),
        misp=EmptyFlavour(),
        stix=EmptyFlavour(),
        case=EmptyFlavour()
    )


class ZeroNet(Entity):

    _flavours = Flavours(
        vysion=Vysion("network", "darknet", "zeronet"),
        dbsafe=EmptyFlavour(),
        misp=EmptyFlavour(),
        stix=EmptyFlavour(),
        case=EmptyFlavour()
    )


class ZeroNet_Bit_Domain(Entity):

    _flavours = Flavours(
        vysion=Vysion("darknet", "zeronet", "zeronet-bit"),
        dbsafe=EmptyFlavour(),
        misp=EmptyFlavour(),
        stix=EmptyFlavour(),
        case=EmptyFlavour()
    )


class ZeroNet_PK_Domain(Entity):

    _flavours = Flavours(
        vysion=Vysion("darknet", "zeronet", "zeronet-pk"),
        dbsafe=EmptyFlavour(),
        misp=EmptyFlavour(),
        stix=EmptyFlavour(),
        case=EmptyFlavour()
    )


class Freenet_SSK_Domain(Entity):

    _flavours = Flavours(
        vysion=Vysion("darknet", "freenet", "freenet-ssk"),
        dbsafe=EmptyFlavour(),
        misp=EmptyFlavour(),
        stix=EmptyFlavour(),
        case=EmptyFlavour()
    )

class Freenet_CHK_Domain(Entity):

    _flavours = Flavours(
        vysion=Vysion("darknet", "freenet", "freenet-chk"),
        dbsafe=EmptyFlavour(),
        misp=EmptyFlavour(),
        stix=EmptyFlavour(),
        case=EmptyFlavour()
    )


class URL(Entity):

    _flavours = Flavours(
        vysion=EmptyFlavour(),
        dbsafe=DBSafe("parche", "automatic-detection", "url"),
        misp=EmptyFlavour(),
        stix=EmptyFlavour(),
        case=EmptyFlavour()
    )


class HTML(Entity):

    _flavours = Flavours(
        vysion=EmptyFlavour(),
        dbsafe=DBSafe("vysion", "automatic-detection", "html"),
        misp=MISP("file-type", "type", "html"),
        stix=EmptyFlavour(),
        case=EmptyFlavour()
    )


class Location(Entity):

    _flavours = Flavours(
        vysion=EmptyFlavour(),
        dbsafe=DBSafe("vysion", "automatic-detection", "location-addresss"),
        misp=MISP("gea-nz-entities", "places-address-type", "location-addresss"),
        stix=EmptyFlavour(),
        case=EmptyFlavour()
    )


class Business(Entity):

    _flavours = Flavours(
        vysion=EmptyFlavour(),
        dbsafe=DBSafe("vysion", "automatic-detection", "business"),
        misp=MISP("stix-ttp", "victim-targeting", "business-professional-sector"),
        stix=EmptyFlavour(),
        case=EmptyFlavour()
    )


class PhoneNumber(Entity):

    _flavours = Flavours(
        vysion=Vysion("finding", "id", "phone-number"),
        dbsafe=DBSafe("vysion", "automatic-detection", "phone-number"),
        misp=MISP("infoleak", "automatic-detection", "phone-number"),
        stix=EmptyFlavour(),
        case=EmptyFlavour()
    )


class Password(Entity):

    _flavours = Flavours(
        vysion=EmptyFlavour(),
        dbsafe=DBSafe("vysion", "automatic-detection", "password"),
        misp=EmptyFlavour(),
        stix=EmptyFlavour(),
        case=EmptyFlavour()
    )


class SeedPhrase(Entity):

    _flavours = Flavours(
        vysion=EmptyFlavour(),
        dbsafe=DBSafe("vysion", "automatic-detection", "seed-phrase"),
        misp=EmptyFlavour(),
        stix=EmptyFlavour(),
        case=EmptyFlavour()
    )


class Email(Entity):

    _flavours = Flavours(
        vysion=Vysion("finding", "id", "email"),
        dbsafe=DBSafe("vysion", "automatic-detection", "email"),
        misp=EmptyFlavour(),
        stix=EmptyFlavour(),
        case=EmptyFlavour()
    )


class Pastebin(Entity):

    _flavours = Flavours(
        vysion=Vysion("network", "paste", "pastebin"),
        dbsafe=EmptyFlavour(),
        misp=EmptyFlavour(),
        stix=EmptyFlavour(),
        case=EmptyFlavour()
    )



class JustPaste(Entity):

    _flavours = Flavours(
        vysion=Vysion("network", "paste", "justpaste"),
        dbsafe=EmptyFlavour(),
        misp=EmptyFlavour(),
        stix=EmptyFlavour(),
        case=EmptyFlavour()
    )


class IRC(Entity):

    _flavours = Flavours(
        vysion=Vysion("network", "im", "irc"),
        dbsafe=DBSafe("vysion", "automatic-detection", "internet-relay-chat"),
        misp=EmptyFlavour(),
        stix=EmptyFlavour(),
        case=EmptyFlavour()
    )


class Skype(Entity):

    _flavours = Flavours(
        vysion=Vysion("network", "im", "skype"),
        dbsafe=DBSafe("vysion", "automatic-detection", "skype"),
        misp=EmptyFlavour(),
        stix=EmptyFlavour(),
        case=EmptyFlavour()
    )


class PGPPublic(Entity):

    _flavours = Flavours(
        vysion=EmptyFlavour(),
        dbsafe=DBSafe("vysion", "automatic-detection", "pgp-public-key-block"),
        misp=MISP("infoleak", "automatic-detection", "pgp-public-key-block"),
        stix=EmptyFlavour(),
        case=EmptyFlavour()
    )



class PGPPrivate(Entity):

    _flavours = Flavours(
        vysion=EmptyFlavour(),
        dbsafe=DBSafe("vysion", "automatic-detection", "pgp-private-key"),
        misp=MISP("infoleak", "automatic-detection", "pgp-private-key"),
        stix=EmptyFlavour(),
        case=EmptyFlavour()
    )


class Telegram(Entity):

    _flavours = Flavours(
        vysion=Vysion("network", "im", "telegram"),
        dbsafe=DBSafe("vysion", "automatic-detection", "telegram"),
        misp=MISP("DFRLab-dichotomies-of-disinformation", "platforms-messaging", "telegram"),
        stix=EmptyFlavour(),
        case=EmptyFlavour()
    )


class WhatsApp(Entity):

    _flavours = Flavours(
        vysion=Vysion("network", "im", "whatsapp"),
        dbsafe=DBSafe("vysion", "automatic-detection", "whatsapp"),
        misp=MISP("DFRLab-dichotomies-of-disinformation", "platforms-messaging", "whatsapp"),
        stix=EmptyFlavour(),
        case=EmptyFlavour()
    )


class Discord(Entity):

    _flavours = Flavours(
        vysion=Vysion("network", "im", "discord"),
        dbsafe=DBSafe("vysion", "automatic-detection", "discord"),
        misp=EmptyFlavour(),
        stix=EmptyFlavour(),
        case=EmptyFlavour()
    )

