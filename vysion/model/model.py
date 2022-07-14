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

try:
    from types import NoneType
except:
    NoneType: type = type(None)

from typing import List, Optional, Union
from urllib.parse import urlparse

from pydantic import BaseModel, Field # , constr

from vysion import taxonomy as vystaxonomy
from .enum import Services, Network, Language, RansomGroup


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


class WhatsApp(BaseModel):

    _taxonomy = [vystaxonomy.WhatsApp]

    value: str  # TODO Regex


class URL(BaseModel):

    _taxonomy = [vystaxonomy.URL]

    protocol: str
    domain: str
    port: int
    path: str
    signature: str
    network: Network

    @classmethod
    def parse(cls, url):

        parsed = urlparse(url)

        scheme = parsed.scheme
        netloc = parsed.netloc
        path = parsed.path
        query = parsed.query
        fragment = parsed.fragment
        params = parsed.params
        username = parsed.username
        password = parsed.password

        # Build domain:port
        domain_port = netloc.split(":")
        domain = domain_port[0]
        if len(domain_port) <= 1:
            try:
                port = Services[scheme]
            except KeyError:
                port = 80
        else:
            port = domain_port[1]

        # Rebuild path's query
        query_parts = [param.split("=") for param in query.split("&")]
        query_dict = {}
        for part in query_parts:
            if len(part) <= 1:
                query_dict[part[0]] = str()
            else:
                query_dict[part[0]] = part[1]

        query_keys = list(query_dict.keys())
        query_keys.sort()
        res_query_parts = [f"{k}={query_dict[k]}" for k in query_keys]
        res_query = "?" + "&".join(res_query_parts)

        # Build /path?query#fragment
        res_path = path + res_query + f"#{fragment}"

        # TODO Adapt restalker.link_extractors.UUF logic to fix URLs
        # TODO Detect network
        tmp_result = cls(
            protocol=scheme,
            domain=domain,
            port=port,
            path=res_path,
            signature=str(),
            network=Network.clearnet,
        )

        signature = hashlib.sha1(tmp_result.build().encode()).hexdigest()
        tmp_result.signature = signature

        return tmp_result

    def build(self) -> str:
        return f"{self.protocol}://{self.domain}:{self.port}{self.path}"


class Page(BaseModel):

    id: str
    url: URL
    parent: str = None
    title: str = None  # TODO Revisar si None o str()
    language: Language
    html: str = None
    sha1sum: str = None
    ssdeep: str = None
    date: datetime = None
    chunk: bool = False


class Hit(BaseModel):

    page: Page
    email: List[Email] = Field(default_factory=lambda: [])
    paste: List[Paste] = Field(default_factory=lambda: [])
    skype: List[Skype] = Field(default_factory=lambda: [])
    telegram: List[Telegram] = Field(default_factory=lambda: [])
    whatsapp: List[WhatsApp] = Field(default_factory=lambda: [])
    bitcoin_address: List[BitcoinAddress] = Field(default_factory=lambda: [])


class RansomFeedHit(BaseModel):

    id: str
    company: Optional[str]
    company_link: Optional[str]
    link: str
    group: RansomGroup
    date: datetime
    info: Optional[str]


class Result(BaseModel):

    # TODO Añadir paginación, query, etc?
    total: int = 0
    hits: Union[List[Hit], List[RansomFeedHit]] = Field(default_factory=lambda: [])

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
