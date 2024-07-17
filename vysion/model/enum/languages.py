#!/usr/bin/env python3
"""
Copyright 2022 Byron Labs S.L.

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

from enum import Enum


class Language(str, Enum):
    """
    Using names from ISO 639-1
    """

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
    occitan = ("oc",)
    polish = "pl"
    bulgarian = "bg"
    assamese = "as"
    limburgan = "li"
    turkish = "tr"
    zulu = "zu"
    corsican = "co"
    kanuri = "kr"
    ojibwa = "oj"
    tonga = ("to",)
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
    cotedivoire = "ci"
