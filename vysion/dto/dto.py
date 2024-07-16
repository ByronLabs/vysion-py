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

import hashlib
import re
from datetime import datetime
from enum import Enum

from vysion.model import enum
from vysion.taxonomy import Monero_Address, Ripple_Address

try:
    from types import NoneType
except:
    NoneType: type = type(None)

from typing import List, Optional, Union
from urllib.parse import urlparse

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    root_validator,
    validator,
)
from pydantic_core.core_schema import FieldValidationInfo

from vysion import taxonomy as vystaxonomy
from vysion.model import URL as URL_model
from vysion.model.enum import Language, Network, RansomGroup, Services

from .topic import Namespace, Predicate, Topic


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

    networkProtocol: Optional[str]
    domainName: Optional[str]
    port: Optional[int]
    path: Optional[str]
    signature: str
    network: Network = Field(default_factory=lambda: Network.clearnet)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @classmethod
    def parse(cls, url):
        # TODO Save this parsed in a private variable? (e.g., _pared_)
        parsed = URL_model.parse(url)
        print(parsed)
        tmp_result = cls(
            networkProtocol=parsed.protocol,
            domainName=parsed.domain,
            port=parsed.port,
            path=parsed.path,
            signature=str(parsed.signature),  # TODO Replace signature: str --> UUID
        )

        return tmp_result

    def build(self) -> str:
        return f"{self.protocol}://{self.domain}:{self.port}{self.path}"


class Page(BaseModel):
    id: str
    url: URL
    foundAt: Optional[str] = None
    pageTitle: Optional[str] = None
    language: Optional[Language]
    html: str = None
    sha1sum: Optional[str] = None
    sha256sum: Optional[str] = None
    ssdeep: Optional[str] = None
    detectionDate: datetime = None
    chunk: bool = False


class RansomwareHit(BaseModel):
    id: str
    url: URL
    pageTitle: Optional[str] = None
    ransomwareGroup: str
    companyName: Optional[str]
    companyAddress: Optional[str]
    companyLink: Optional[str]
    text: Optional[str]
    html: Optional[str]
    country: Optional[str]
    sha256sum: Optional[str] = None
    ssdeep: Optional[str] = None
    detectionDate: datetime
    chunk: bool = False
    topic: List[Topic] = Field(default_factory=lambda: [])

    model_config = ConfigDict(arbitrary_types_allowed=True)


class Media(BaseModel):
    bucketName: Optional[str] = Field(default_factory=lambda: None)
    objectPath: Optional[str] = Field(default_factory=lambda: None)
    objectName: Optional[str] = Field(default_factory=lambda: None)
    contentType: str

    @validator("bucketName", "objectPath", "objectName")
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

    @root_validator(pre=True)
    def split_key_value(cls, value: str) -> dict:
        if isinstance(value, str):
            key, value = value.split(":")
            return {"key": key, "value": float(value)}
        return value

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


class TelegramHit(BaseModel):
    userId: Optional[int] = Field(default_factory=lambda: None)
    username: Optional[str] = Field(default_factory=lambda: None)
    channelId: Optional[int] = Field(default_factory=lambda: None)
    messageId: int
    message: Optional[str] = Field(default_factory=lambda: None)
    channelTitle: Optional[str] = Field(default_factory=lambda: None)
    languages: Optional[List[LanguagePair]] = Field(default_factory=lambda: None)
    sha1sum: Optional[str] = None
    sha256sum: Optional[str] = None
    media: Optional[str] = Field(default_factory=lambda: None)
    detectionDate: datetime

    @field_validator("messageId")
    def validate_messageId(cls, v: int) -> int:
        if not v:
            raise ValueError("MessageId field cannot be empty")
        return v


class TelegramProfileHit(BaseModel):
    userId: int
    usernames: Optional[List[str]] = Field(default_factory=lambda: None)
    firstName: Optional[List[str]] = Field(default_factory=lambda: None)
    lastName: Optional[List[str]] = Field(default_factory=lambda: None)
    detectionDate: datetime
    profilePhoto: Optional[List[str]] = Field(default_factory=lambda: None)

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


class TelegramChannelHit(BaseModel):
    channelId: int
    channelTitles: Optional[List[str]] = Field(default_factory=lambda: None)
    detectionDate: datetime
    creationDate: datetime
    channelPhoto: Optional[List[str]] = Field(default_factory=lambda: None)

    @field_validator("channelId")
    def validate_channelId(cls, v: int) -> int:
        if not v:
            raise ValueError("channelId field cannot be empty")
        return v

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


class Hit(BaseModel):
    page: Page
    topic: List[Topic] = Field(default_factory=lambda: [])
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
    companyName: Optional[str]
    companyLink: Optional[str]
    url: str
    ransomwareGroup: str
    detectionDate: datetime
    text: Optional[str]
    country: Optional[str]

    model_config = ConfigDict(arbitrary_types_allowed=True)


class TelegramFeedHit(BaseModel):
    id: str
    telegram: List[str]
    detectionDate: datetime
    url: str
    path: str
    network: str


class Result(BaseModel):
    # TODO Add pagination, query, etc?
    total: int = 0
    hits: Union[
        List[Hit],
        List[TelegramHit],
        List[RansomFeedHit],
        List[TelegramFeedHit],
        List[RansomwareHit],
        List[TelegramProfileHit],
        List[TelegramChannelHit],
    ] = Field(default_factory=lambda: [])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.total <= 0:
            self.total = len(self.hits)

    def get_type(self) -> type:
        if len(self.hits) <= 0:
            return NoneType

        return type(self.hits[0])


class Pagination(BaseModel):
    page: int = 1
    limit: int = 10


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
    code: ErrorCode = ErrorCode.INTERNAL_SERVER_ERROR
    message: str = ErrorMessage.INTERNAL_SERVER_ERROR


class VysionResponse(BaseModel):
    data: Optional[Result] = None
    error: Optional[Error] = None
