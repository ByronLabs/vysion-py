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
from enum import Enum
import hashlib

from datetime import datetime
from vysion.model import enum

from vysion.taxonomy import Monero_Address, Ripple_Address

try:
    from types import NoneType
except:
    NoneType: type = type(None)

from typing import List, Optional, Union
from urllib.parse import urlparse

from pydantic import BaseModel, Field # , constr
from .tag import *

from urllib.parse import urlparse
from vysion import taxonomy as vystaxonomy
from vysion.model import URL as URL_model
from vysion.model.enum import Services, Network, Language, RansomGroup


class Email(BaseModel):

    _taxonomy = [vystaxonomy.Email]

    # RFC 5322 Official Standard (https://www.emailregex.com/)
    # value: constr(regex=r'''(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])''') # TODO Añadir que es str
    value: str  # TODO Fix regex to allow caps


class Paste(BaseModel):

    _taxonomy = [vystaxonomy.Pastebin, vystaxonomy.JustPaste]

    value: str  # TODO Regex


class Skype(BaseModel):

    _taxonomy = [vystaxonomy.Skype]

    value: str  # TODO Regex


class Telegram(BaseModel):

    _taxonomy = [vystaxonomy.Telegram]  # TODO Create Telegram URL

    value: str  # TODO Regex


class BitcoinAddress(BaseModel):

    _taxonomy = [vystaxonomy.Bitcoin_Address]  # TODO Create Telegram URL

    value: str  # TODO Regex


class PolkadotAddress(BaseModel):

    _taxonomy = [vystaxonomy.Polkadot_Address]  # TODO Create Telegram URL

    value: str  # TODO Regex


class EthereumAddress(BaseModel):

    _taxonomy = [vystaxonomy.Ethereum_Address]  # TODO Create Telegram URL

    value: str  # TODO Regex


class MoneroAddress(BaseModel):

    _taxonomy = [vystaxonomy.Monero_Address]  # TODO Create Telegram URL

    value: str  # TODO Regex


class RippleAddress(BaseModel):

    _taxonomy = [vystaxonomy.Ripple_Address]  # TODO Create Telegram URL

    value: str  # TODO Regex


class ZcashAddress(BaseModel):

    _taxonomy = [vystaxonomy.Zcash_Address]  # TODO Create Telegram URL

    value: str  # TODO Regex


class WhatsApp(BaseModel):

    _taxonomy = [vystaxonomy.WhatsApp]

    value: str  # TODO Regex


class URL(BaseModel):

    _taxonomy = [vystaxonomy.URL]

    protocol: Optional[str]
    domain: Optional[str]
    port: Optional[int]
    path: Optional[str]
    signature: str
    network: Network = Field(default_factory=lambda: Network.clearnet)

    @classmethod
    def parse(cls, url):

        # TODO Save this parsed in a private variable? (e.g., _pared_)
        parsed = URL_model.parse(url)
        print(parsed)
        tmp_result = cls(
            protocol=parsed.protocol,
            domain=parsed.domain,
            port=parsed.port,
            path=parsed.path,
            signature=str(parsed.signature) # TODO Replace signature: str --> UUID
        )

        return tmp_result

    def build(self) -> str:
        return f"{self.protocol}://{self.domain}:{self.port}{self.path}"


class Page(BaseModel):

    id: str
    url: URL
    parent: str = None
    title: str = None  # TODO Revisar si None o str()
    language: Optional[Language]
    html: str = None
    sha1sum: str = None
    sha256sum: str = None
    ssdeep: str = None
    date: datetime = None
    chunk: bool = False

class RansomwarePage(BaseModel):

    id: str
    url: URL
    # title: str = None  
    group: RansomGroup
    company: Optional[str]
    company_address : Optional[str]
    company_link : Optional[str]
    info: Optional[str]
    country: Optional[str]
    sha256sum: str = None
    ssdeep: str = None
    date: datetime 
    chunk: bool = False

class RansomwareHit(BaseModel):
    page: RansomwarePage

class Hit(BaseModel):

    page: Page
    tag: List[Tag]
    email: List[Email] = Field(default_factory=lambda: [])
    paste: List[Paste] = Field(default_factory=lambda: [])
    skype: List[Skype] = Field(default_factory=lambda: [])
    telegram: List[Telegram] = Field(default_factory=lambda: [])
    whatsapp: List[WhatsApp] = Field(default_factory=lambda: [])
    bitcoin_address: List[BitcoinAddress] = Field(default_factory=lambda: [])
    polkadot_address: List[PolkadotAddress] = Field(default_factory=lambda: [])
    ethereum_address: List[EthereumAddress] = Field(default_factory=lambda: [])
    monero_address: List[MoneroAddress] = Field(default_factory=lambda: [])
    ripple_address: List[RippleAddress] = Field(default_factory=lambda: [])
    zcash_address: List[ZcashAddress] = Field(default_factory=lambda: [])


class RansomFeedHit(BaseModel):

    id: str
    company: Optional[str]
    company_link: Optional[str]
    link: str
    group: RansomGroup
    date: datetime
    info: Optional[str]
    country: Optional[str]


class TelegramFeedHit(BaseModel):

    id: str
    telegram: List[str]
    date: datetime
    url: str
    path: str
    network: str


class Result(BaseModel):

    # TODO Añadir paginación, query, etc?
    total: int = 0
    hits: Union[List[Hit], List[RansomFeedHit], List[TelegramFeedHit], List[RansomwareHit]] = Field(
        default_factory=lambda: [])
        
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.total <= 0:
            self.total = len(self.hits)

    def get_type(self) -> type:

        if len(self.hits) <= 0:
            return NoneType

        return type(self.hits[0])


# TODO Move API responses to other class
class VysionResponse(BaseModel):
    """
    VysionResponse is a json:api flavoured response from the API
    """

    data: Result  # TODO Add type to all JSON:API responses


class VysionError(BaseModel):

    class StatusCode(int, Enum):

        UNK = 000
        OK = 200
        REQ_ERROR = 400
        UNAUTHORIZED = 403
        NOT_FOUND = 404
        INTERNAL_ERROR = 500

    code: StatusCode = StatusCode.UNK
    message: str = "UNK_ERR"
