#!/usr/bin/env python3
"""
Copyright 2024 ByronLabs S.L.

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
from enum import Enum

try:
    from types import NoneType
except:
    NoneType: type = type(None)

import uuid
from typing import Generic, List, Optional, TypeVar, Union
from urllib.parse import urlparse

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from vysion import taxonomy as vystaxonomy
from vysion.model.enum import Language, Network

from .tag import Tag


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

    url: str
    networkProtocol: str = Field(default_factory=lambda: "http")
    domainName: str = Field(default_factory=lambda: None)
    port: int = Field(default_factory=lambda: 80)
    path: str = Field(default_factory=lambda: None)
    signature: uuid.UUID = Field(
        default_factory=lambda: uuid.UUID("{00000000-0000-0000-0000-000000000000}")
    )
    network: Network = Field(default_factory=lambda: Network.clearnet)

    def __generate_signature(self) -> uuid.UUID:
        return uuid.uuid5(uuid.NAMESPACE_URL, self.build())

    @classmethod
    def parse(cls, url):
        parsed = urlparse(url)

        # Elements
        scheme = parsed.scheme
        netloc = parsed.netloc
        path = parsed.path
        query = parsed.query
        fragment = parsed.fragment

        # Build domain:port
        try:
            domain_port = (netloc.split(":") + [80])[:2]
        except Exception as e:
            print(e)

        domainName = domain_port[0]

        if ".onion" in domainName:
            network = Network.tor
        elif ".i2p" in domainName:
            network = Network.i2p
        else:
            network = Network.clearnet

        port = domain_port[1]

        # Build /path?query#fragment
        res_path = path

        # Rebuild path's query
        if len(query) > 0:
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

            res_path += res_query

        if len(fragment) > 0:
            res_path += f"#{fragment}"

        return cls(
            url=url,
            networkProtocol=scheme,
            domainName=domainName,
            port=port,
            path=res_path,
            network=network,
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.signature = self.__generate_signature()

    def build(self) -> str:
        url = self.path

        if self.domainName != "":
            if self.port != 80:
                url = f":{self.port}" + url

            url = f"{self.domainName}" + url

        if self.networkProtocol != "":
            url = f"{self.networkProtocol}://" + url

        return url


class Page(BaseModel):
    id: str
    url: URL
    foundAt: Optional[str] = None
    pageTitle: Optional[str] = None
    language: Optional[Language]
    html: Optional[str] = None
    text: Optional[str] = None
    sha1sum: Optional[str] = None
    sha256sum: Optional[str] = None
    ssdeep: Optional[str] = None
    detectionDate: datetime = None
    screenshot: Optional[str] = None
    chunk: bool = False
    htmlOversize: Optional[bool] = False
    docType: Optional[str] = None



class RansomwareHit(BaseModel):
    page: Page
    tag: List[Tag] = Field(default_factory=lambda: [])
    ransomwareGroup: str
    companyName: Optional[str] = None
    companyAddress: Optional[str] = None
    companyLink: Optional[str] = None
    country: Optional[str] = None
    naics: Optional[str] = None
    industry: Optional[str] = None

class DocumentHit(BaseModel):
    page: Page
    tag: List[Tag] = Field(default_factory=lambda: [])
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


class Media(BaseModel):
    bucketName: Optional[str] = Field(default_factory=lambda: None)
    objectPath: Optional[str] = Field(default_factory=lambda: None)
    objectName: Optional[str] = Field(default_factory=lambda: None)
    contentType: str

    @field_validator("bucketName", "objectPath", "objectName")
    def validate_strings(cls, v):
        if v is not None and not isinstance(v, str):
            raise ValueError("value must be a string")
        return v

    @field_validator("contentType")
    def validate_contentType(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("contentType field cannot be empty")
        return v


class LanguagePair(BaseModel):
    language: str
    probability: float

    @model_validator(mode="before")
    @classmethod
    def split_key_value(cls, data: str) -> dict:
        if isinstance(data, str):
            key, value = data.split(":")
            return {"language": key, "probability": float(value)}
        return data

    @field_validator("language")
    def validate_language(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Language field cannot be empty")
        return v

    @field_validator("probability")
    def validate_probability(cls, v: float) -> float:
        if v < 0 or v > 1:
            raise ValueError("Probability must be between 0 and 1")
        return v


class ImMessageHit(BaseModel):
    userId: Optional[Union[int, str]] = Field(default_factory=lambda: None)
    username: Optional[str] = Field(default_factory=lambda: None)
    channelId: Optional[Union[int, str]] = Field(default_factory=lambda: None)
    messageId: Union[int, str]
    message: Optional[str] = Field(default_factory=lambda: None)
    channelTitle: Optional[str] = Field(default_factory=lambda: None)
    languages: Optional[List[LanguagePair]] = Field(default_factory=lambda: None)
    sha1sum: Optional[str] = None
    sha256sum: Optional[str] = None
    media: Optional[str] = Field(default_factory=lambda: None)
    detectionDate: datetime
    serverId: Optional[Union[int, str]] = Field(default_factory=lambda: None) #Discord Exclusive
    serverTitle: Optional[str] = Field(default_factory=lambda: None) #Discord Exclusive
    platform: Optional[str] = Field(default_factory=lambda: None) 

    @model_validator(mode="after")
    def validate_platform_specific_fields(cls, values):
        """
        Conditionally include platform-specific fields:
        - Include Discord-specific fields only for Discord platform
        - Exclude Discord-specific fields for Telegram platform
        """
        platform = getattr(values, "platform", None)
        
        # For Telegram platform, remove Discord-specific fields
        if platform is None or (isinstance(platform, str) and platform.lower() == "telegram"):
            # Delete attributes instead of setting to None
            for attr in ["serverId", "serverTitle"]:
                if hasattr(values, attr):
                    delattr(values, attr)
        
        return values
    
class ImMessageCardHit(BaseModel):
    userId: Optional[Union[int, str]] = Field(default_factory=lambda: None)
    username: Optional[str] = Field(default_factory=lambda: None)
    channelId: Optional[int] = Field(default_factory=lambda: None)
    messageId: Union[int, str]
    message: Optional[str] = Field(default_factory=lambda: None)
    channelTitle: Optional[str] = Field(default_factory=lambda: None)
    languages: Optional[List[LanguagePair]] = Field(default_factory=lambda: None)
    detectionDate: datetime
    serverId: Optional[Union[int, str]] = Field(default_factory=lambda: None) #Discord Exclusive
    serverTitle: Optional[str] = Field(default_factory=lambda: None) #Discord Exclusive
    platform: Optional[str] = Field(default_factory=lambda: None)

    @model_validator(mode="after")
    def validate_platform_specific_fields(cls, values):
        """
        Conditionally include platform-specific fields:
        - Include Discord-specific fields only for Discord platform
        - Exclude Discord-specific fields for Telegram platform
        """
        platform = getattr(values, "platform", None)
        
        # For Telegram platform, remove Discord-specific fields
        if platform is None or (isinstance(platform, str) and platform.lower() == "telegram"):
            # Delete attributes instead of setting to None
            for attr in ["serverId", "serverTitle"]:
                if hasattr(values, attr):
                    delattr(values, attr)
        
        return values

class ImProfileHit(BaseModel):
    userId: Union[int, str]
    usernames: Optional[List[str]] = Field(default_factory=lambda: None)
    firstName: Optional[List[str]] = Field(default_factory=lambda: None)
    lastName: Optional[List[str]] = Field(default_factory=lambda: None)
    detectionDate: datetime
    profilePhoto: Optional[List[str]] = Field(default_factory=lambda: None)
    bot: Optional[bool] = Field(default_factory=lambda: None) #Discord Exclusive
    discordLink: Optional[List[str]] = Field(default_factory=lambda: None) #Discord Exclusive
    discriminator: Optional[List[int]] = Field(default_factory=lambda: None) #Discord Exclusive
    # TODO platform should be mandatory
    platform: Optional[str] = Field(default_factory=lambda: None)
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

    
    model_config = ConfigDict(exclude_defaults=True)

    @model_validator(mode="after")
    def validate_platform_specific_fields(cls, values):
        """
        Conditionally include platform-specific fields:
        - Include Discord-specific fields only for Discord platform
        - Exclude Discord-specific fields for Telegram platform
        """
        platform = getattr(values, "platform", None)
        
        # For Telegram platform, remove Discord-specific fields
        if platform is None or (isinstance(platform, str) and platform.lower() == "telegram"):
            # Delete attributes instead of setting to None
            for attr in ["discordLink", "bot", "discriminator"]:
                if hasattr(values, attr):
                    delattr(values, attr)
        
        return values

    @field_validator("userId")
    def validate_userId(cls, v: int) -> int:
        if not v:
            raise ValueError("UserId field cannot be empty")
        return v

    @field_validator("detectionDate")
    def validate_detectionDate(cls, v: datetime) -> datetime:
        if not v:
            raise ValueError("DetectionDate field cannot be empty")
        return v


class ImChannelHit(BaseModel):
    channelId: Union[int, str]
    channelTitles: Optional[List[str]] = Field(default_factory=lambda: None)
    detectionDate: datetime
    creationDate: datetime
    channelPhoto: Optional[List[str]] = Field(default_factory=lambda: None) #Telegram Exclusive
    serverId: Optional[Union[int, str]] = Field(default_factory=lambda: None) #Discord Exclusive
    serverTitle: Optional[List[str]] = Field(default_factory=lambda: None) #Discord Exclusive
    platform: Optional[str] = Field(default_factory=lambda: None)
    
    @model_validator(mode="after")
    def validate_platform_specific_fields(cls, values):
        """
        Conditionally include platform-specific fields:
        - Include Discord-specific fields only for Discord platform
        - Exclude Discord-specific fields for Telegram platform
        """
        platform = getattr(values, "platform", None)
        
        # For Telegram platform, remove Discord-specific fields
        if platform is None or (isinstance(platform, str) and platform.lower() == "telegram"):
            # Delete attributes instead of setting to None
            for attr in ["serverId", "serverTitle"]:
                if hasattr(values, attr):
                    delattr(values, attr)
        else:
            # For Discord platform, remove Telegram-specific fields
            for attr in ["channelPhoto"]:
                if hasattr(values, attr):
                    delattr(values, attr)
        
        return values
    
    @field_validator("detectionDate")
    def validate_detectionDate(cls, v: datetime) -> datetime:
        if not v:
            raise ValueError("DetectionDate field cannot be empty")
        return v

    @field_validator("creationDate")
    def validate_creationDate(cls, v: datetime) -> datetime:
        if not v:
            raise ValueError("creationDate field cannot be empty")
        return v

class ImServerHit(BaseModel):
    serverId: Union[int, str]
    serverTitles: Optional[List[str]] = Field(default_factory=lambda: None)
    detectionDate: datetime
    creationDate: datetime
    serverPhoto: Optional[List[str]] = Field(default_factory=lambda: None)
    memberCount: Optional[int] = Field(default_factory=lambda: None)
    discordLink: Optional[List[str]] = Field(default_factory=lambda: None)

    @field_validator("detectionDate")
    def validate_detectionDate(cls, v: datetime) -> datetime:
        if not v:
            raise ValueError("DetectionDate field cannot be empty")
        return v

    @field_validator("creationDate")
    def validate_creationDate(cls, v: datetime) -> datetime:
        if not v:
            raise ValueError("creationDate field cannot be empty")
        return v

class ImFeedHit(BaseModel):
    id: str
    telegram: List[str]
    detectionDate: datetime
    url: str
    path: str
    network: str


class CryptoFeedHit(BaseModel):
    id: str
    url: str
    detectionDate: datetime
    url: str
    network: str
    title: str
    tag: List[Tag] = Field(default_factory=lambda: [])
    bitcoin_address: Optional[List[BitcoinAddress]] = Field(default_factory=lambda: [])
    polkadot_address: Optional[List[PolkadotAddress]] = Field(default_factory=lambda: [])
    ethereum_address: Optional[List[EthereumAddress]] = Field(default_factory=lambda: [])
    monero_address: Optional[List[MoneroAddress]] = Field(default_factory=lambda: [])
    ripple_address: Optional[List[RippleAddress]] = Field(default_factory=lambda: [])
    zcash_address: Optional[List[ZcashAddress]] = Field(default_factory=lambda: [])

    model_config = ConfigDict(
        arbitrary_types_allowed=True, 
        exclude_defaults=True, 
        validate_assignment=True
    )

    @model_validator(mode="after")
    def remove_empty_lists(cls, values):
        """Remove empty cryptocurrency lists from output"""
        crypto_fields = [
            "bitcoin_address", 
            "polkadot_address", 
            "ethereum_address", 
            "monero_address", 
            "ripple_address", 
            "zcash_address"
        ]
        
        for field_name in crypto_fields:
            field_value = getattr(values, field_name, None)
            if isinstance(field_value, list) and not field_value:
                setattr(values, field_name, None)
        
        return values


class RansomFeedHit(BaseModel):
    id: str
    companyName: Optional[str]
    companyLink: Optional[str]
    url: str
    ransomwareGroup: str
    detectionDate: datetime
    text: Optional[str]
    country: Optional[str]
    naics: Optional[str]
    industry: Optional[str]

    model_config = ConfigDict(arbitrary_types_allowed=True)


class Stat(BaseModel):
    key: Union[str, int]
    doc_count: int


class Buckets(BaseModel):
    buckets: List[Stat]


class AggStats(Stat):
    key_as_string: str
    agg: Optional[Buckets] = None


class PhoneInfo(BaseModel):
    name: str
    source: str
    href: Optional[str] = None
    carrier: Optional[str] = None


T = TypeVar("T")


class Result(BaseModel, Generic[T]):
    total: int = 0
    hits: List[T] = Field(default_factory=lambda: [])
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.total <= 0:
            self.total = len(self.hits)

    def get_type(self) -> type:
        if len(self.hits) <= 0:
            return NoneType

        return type(self.hits[0])

    @model_validator(mode="before")
    @classmethod
    def check_hits(cls, data):
        hits = data.get("hits")
        if not isinstance(hits, list):
            raise ValueError("hits must be a list")

        return data


class ErrorCode(int, Enum):
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICT = 409
    UNPROCESSABLE_ENTITY = 422
    TOO_MANY_REQUESTS = 429
    INTERNAL_SERVER_ERROR = 500


class ErrorMessage(str, Enum):
    BAD_REQUEST = "Bad Request"
    UNAUTHORIZED = "Unauthorized"
    FORBIDDEN = "Forbidden"
    NOT_FOUND = "Not Found"
    CONFLICT = "Conflict"
    UNPROCESSABLE_ENTITY = "Unprocessable Entity"
    TOO_MANY_REQUESTS = "Too Many Requests"
    INTERNAL_SERVER_ERROR = "Internal Server Error"


class Error(BaseModel):
    code: ErrorCode
    message: str


class VysionResponse(BaseModel, Generic[T]):
    data: Optional[Result[T]] = None
    error: Optional[Error] = None
