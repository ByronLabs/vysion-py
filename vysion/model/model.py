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
from .enum import Enum
import hashlib
import uuid
from datetime import datetime

from vysion.taxonomy.taxonomy import Monero_Address, Ripple_Address

try:
    from types import NoneType
except:
    NoneType: type = type(None)

from typing import List, Optional, Union

from pydantic import BaseModel, Field # , constr

from .enum import Services, Network

import re

<<<<<<< Updated upstream
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

=======
NULL_UUID = uuid.UUID("00000000-0000-0000-0000-000000000000")
>>>>>>> Stashed changes

class URL(BaseModel):

    protocol: Optional[str] 
    domain: Optional[str]   
    port: Optional[int] = Field(default_factory=lambda: -1)
    path: Optional[str]
    signature: uuid.UUID = Field(default_factory=lambda: NULL_UUID)
    
    raw: str

    @staticmethod
    def _parse_(url):
        
        """
        RFC3986
            scheme    = $2
            authority = $4
            path      = $5
            query     = $7
            fragment  = $9
        """
        regex = r"^(([^:/?#]+):)?(//([^/?#]*))?([^?#]*)(\?([^#]*))?(#(.*))?"
        
        res = re.match(regex, url)
        
        scheme = res[2]
        authority = res[4]
        path = res[5]
        query = res[7]
        fragment = res[9]

        return dict(
            scheme=scheme,
            authority=authority,
            path=path,
            query=query,
            fragment=fragment
        )

    def _generate_signature_(self) -> uuid.UUID:
        return uuid.uuid5(uuid.NAMESPACE_URL, self.build())

    @classmethod
    def parse(cls, url, fix=False):

        # Saving the original url
        raw = url

        parsed = cls._parse_(url)
        
        # Elements
        scheme = parsed["scheme"]
        netloc = parsed["authority"]
        path = parsed["path"]
        query = parsed["query"]
        fragment = parsed["fragment"]

        # Build domain:port
        if netloc is not None:
            domain_port = (netloc.split(":") + [None])[:2]
        else:
            domain_port = [None, None]
        
        domain = domain_port[0]
        port = domain_port[1]

        # Normalize path: /path?query#fragment
        # Parse a URL into 6 components:
        # <protocol>://<domain>:<port>/<path>
        if query is not None:

            # Normalize query
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
        
            path += res_query
        
        if fragment is not None:
            path += f"#{fragment}"

        # TODO Adapt restalker.link_extractors.UUF logic to fix URLs
        # TODO Detect network?
        result = cls(
            protocol=scheme,
            domain=domain,
            port=port,
            path=path,
            raw=raw
        )

<<<<<<< Updated upstream
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
    sha256sum: str = None
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
    polkadot_address: List[PolkadotAddress] = Field(default_factory=lambda: [])
    monero_address: List[MoneroAddress] = Field(default_factory=lambda: [])
    ripple_address: List[RippleAddress] = Field(default_factory=lambda: [])
    zcash_address: List[ZcashAddress] = Field(default_factory=lambda: [])
=======
        if fix:
            result._fix()

        return result
>>>>>>> Stashed changes

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.signature = self._generate_signature_()

    def build(self) -> str:
        
        url = self.path

        if self.domain is not None:
            
            if self.port is not None:
                url = f":{self.port}" + url
            
            url = f"{self.domain}" + url

        if self.protocol is not None:

            url = f"{self.protocol}://" + url
            
        return url

    def _fix(self, default_protocol=Services.http) -> None:

        if self.protocol is None:
            if self.port is None:
                self.protocol = default_protocol.name
            else:
                self.protocol = Services(self.port).name

        if self.port is None:
            self.port = Services[self.protocol].value

        if self.domain is None:
            path = self.path
            if path[0] == "/":
                path = path[1:]
            path_parts = path.split('/')
            self.domain = path_parts[0]
            self.path = "/" + "/".join(path_parts[1:])
        
        self.signature = self._generate_signature_()

    def __str__(self) -> str:
        return self.build()

    def __repr__(self):
        return self.build()