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

try:
    from types import NoneType
except:
    NoneType: type = type(None)

from typing import List, Optional, Union

from pydantic import BaseModel, Field # , constr

from .enum import Services, Network

import re

NULL_UUID = uuid.UUID("00000000-0000-0000-0000-000000000000")

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

        if fix:
            result._fix()

        return result

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
