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

from datetime import datetime
from typing import List, Optional
from enum import Enum, IntEnum

from pydantic import BaseModel, Field, constr

from vysion import taxonomy as vystaxonomy


class Network(str, Enum):

    tor = "tor"
    i2p = "i2p"
    zeronet = "zeronet"
    freenet = "freenet"
    paste = "paste"


class Language(str, Enum):

    '''
    Using names from ISO 639-1
    '''

    avaric = "av"
    swati = "ss"
    russian = "ru"
    lingala = "ln"
    afar = "aa"
    mongolian = "mn"
    tahitian = "ty"
    somali = "so"
    gaelic = "gd"
    uighur = "ug"
    pushto = "ps"
    akan = "ak"
    abkhazian = "ab"
    tamil = "ta"
    micmac = "Mi"
    kannada = "kn"
    cree = "cr"
    ndonga = "ng"
    aymara = "ay"
    italian = "it"
    latvian = "lv"
    ukrainian = "uk"
    malay = "ms"
    ganda = "lg"
    finnish = "fi"
    tswana = "tn"
    telugu = "te"
    chuvash = "cv"
    ewe = "ee"
    azerbaijani = "az"
    lao = "lo"
    sindhi = "sd"
    sardinian = "sc"
    thai = "th"
    haitian = "ht"
    bihariLanguages = "bh"
    romansh = "rm"
    bashkir = "ba"
    volapük = "vo"
    yiddish = "yi"
    guarani = "gn"
    croatian = "hr"
    bambara = "bm"
    belarusian = "be"
    sundanese = "su"
    kongo = "kg"
    kirghiz = "ky"
    nepali = "ne"
    icelandic = "is"
    herero = "hz"
    lithuanian = "lt"
    fulah = "ff"
    swahili = "sw"
    manx = "gv"
    marathi = "mr"
    sinhala = "si"
    tajik = "tg"
    marshallese = "mh"
    aragonese = "an"
    dutch = "nl"
    hindi = "hi"
    ido = "io"
    tagalog = "tl"
    japanese = "ja"
    centralKhmer = "km"
    greek = "el"
    maori = "mi"
    luxembourgish = "lb"
    slovenian = "sl"
    maltese = "mt"
    kikuyu = "ki"
    tatar = "tt"
    lubaKatanga = "lu"
    swedish = "sv"
    panjabi = "pa"
    kashmiri = "ks"
    divehi = "dv"
    indonesian = "id"
    malagasy = "mg"
    oriya = "or"
    kuanyama = "kj"
    sango = "sg"
    westernFrisian = "fy"
    zhuang = "za"
    arabic = "ar"
    afrikaans = "af"
    cornish = "kw"
    xhosa = "xh"
    armenian = "hy"
    malayalam = "ml"
    sotho = "st"
    esperanto = "eo"
    latin = "la"
    korean = "ko"
    interlingua = "ia"
    albanian = "sq"
    catalan = "ca"
    norwegianNynorsk = "nn"
    galician = "gl"
    kurdish = "ku"
    igbo = "ig"
    twi = "tw"
    inuktitut = "iu"
    hungarian = "hu"
    yoruba = "yo"
    tsonga = "ts"
    slovak = "sk"
    dzongkha = "dz"
    churchSlavicc = "cu"
    quechua = "qu"
    romanian = "ro"
    fijian = "fj"
    chechen = "ce"
    amharic = "am"
    burmese = "my"
    gujarati = "gu"
    samoan = "sm"
    chamorro = "ch"
    irish = "ga"
    french = "fr"
    ndebele = "nd"
    pali = "pi"
    vietnamese = "vi"
    kazakh = "kk"
    navajo = "nv"
    inupiaq = "ik"
    avestan = "ae"
    nauru = "na"
    danish = "da"
    breton = "br"
    persian = "fa"
    serbian = "sr"
    georgian = "ka"
    english = "en"
    sichuanYi = "ii"
    oromo = "om"
    northernSami = "se"
    venda = "ve"
    chinese = "zh"
    norwegian = "no"
    interlingue = "ie"
    rundi = "rn"
    bislama = "bi"
    hiriMotu = "ho"
    faroese = "fo"
    shona = "sn"
    bengali = "bn"
    kalaallisut = "kl"
    bokmål = "nb"
    occitan = "oc",
    polish = "pl"
    bulgarian = "bg"
    assamese = "as"
    limburgan = "li"
    turkish = "tr"
    zulu = "zu"
    corsican = "co"
    kanuri = "kr"
    ojibwa = "oj"
    tonga = "to",
    sanskrit = "sa"
    hebrew = "he"
    wolof = "wo"
    kinyarwanda = "rw"
    turkmen = "tk"
    uzbek = "uz"
    ossetian = "os"
    tibetan = "bo"
    komi = "kv"
    portuguese = "pt"
    macedonian = "mk"
    javanese = "jv"
    basque = "eu"
    urdu = "ur"
    tigrinya = "ti"
    bosnian = "bs"
    estonian = "et"
    hausa = "ha"
    walloon = "wa"
    welsh = "cy"
    czech = "cs"
    german = "de"
    spanish = "es"


class Email(BaseModel):

    _taxonomy = [
        vystaxonomy.Email
    ]
    
    # RFC 5322 Official Standard (https://www.emailregex.com/)
    value: constr(regex=r'''(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])''') # TODO Añadir que es str


class Paste(BaseModel):

    _taxonomy = [
        vystaxonomy.Pastebin,
        vystaxonomy.JustPaste
    ]
    
    value: str # TODO Regex


class Skype(BaseModel):

    _taxonomy = [
        vystaxonomy.Skype
    ]

    value: str # TODO Regex


class Telegram(BaseModel):

    _taxonomy = [
        vystaxonomy.Telegram # TODO Create Telegram URL
    ]

    value: str # TODO Regex


class BitcoinAddress(BaseModel):

    _taxonomy = [
        vystaxonomy.Bitcoin_Address # TODO Create Telegram URL
    ]

    value: str # TODO Regex


class WhatsApp(BaseModel):

    _taxonomy = [
        vystaxonomy.WhatsApp
    ]

    value: str # TODO Regex


class URL(BaseModel):

    _taxonomy = [
        vystaxonomy.URL
    ]
   
    protocol: str
    domain: str
    port: int
    path: str
    signature: str
    network: Network

    def build(self):
        return f"{self.protocol}://{self.domain}:{self.port}{self.path}"



class Page(BaseModel):

    id: str
    url: URL
    parent: str
    title: str
    language: Language
    html: str
    sha1sum: str
    ssdeep: str
    date: datetime


class Hit(BaseModel):

    page: Page
    email: List[Email] = Field(default_factory=lambda: [])
    paste: List[Paste] = Field(default_factory=lambda: [])
    skype: List[Skype] = Field(default_factory=lambda: [])
    telegram: List[Telegram] = Field(default_factory=lambda: [])
    whatsapp: List[WhatsApp] = Field(default_factory=lambda: [])
    bitcoin_address: List[BitcoinAddress] = Field(default_factory=lambda: [])

class Result(BaseModel):

    total: int = 0
    hits: List[Hit] = Field(default_factory=lambda: [])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.total = len(self.hits)
