#!/bin/env python3.10

import dataclasses

from pydantic.dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, constr

from vysion import taxonomy as vystaxonomy


# TODO Enum?
@dataclass
class Network():
    value: str


@dataclass
class Email():

    _taxonomy = [
        vystaxonomy.Email
    ]
    
    # RFC 5322 Official Standard (https://www.emailregex.com/)
    value: constr(regex=r'''(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])''')
   
    


@dataclass
class Paste():

    _taxonomy = [
        vystaxonomy.Pastebin,
        vystaxonomy.JustPaste
    ]
    value: str # TODO Regex


@dataclass
class Skype():

    _taxonomy = [
        vystaxonomy.Skype
    ]
    value: str # TODO Regex


@dataclass
class Telegram():

    _taxonomy = [
        vystaxonomy.Telegram
    ]
    value: str # TODO Regex


@dataclass
class WhatsApp():

    _taxonomy = [
        vystaxonomy.WhatsApp
    ]
    value: str # TODO Regex


@dataclass
class URL():

    _taxonomy = [
        vystaxonomy.URL
    ]
    
    protocol: str
    domain: str
    port: int
    path: str
    signature: str
    network: Network


@dataclass
class Page():

    url: URL
    parent: str
    title: str
    language: str
    html: str
    sha1sum: str
    ssdeep: str
    date: datetime


@dataclass
class Hit():

    page: Page
    email: List[Email] = dataclasses.field(default_factory=lambda: [])
    paste: List[Paste] = dataclasses.field(default_factory=lambda: [])
    skype: List[Skype] = dataclasses.field(default_factory=lambda: [])
    telegram: List[Telegram] = dataclasses.field(default_factory=lambda: [])
    whatsapp: List[WhatsApp] = dataclasses.field(default_factory=lambda: [])


@dataclass
class Result():

    total: int
    hits: List[Hit] = dataclasses.field(default_factory=lambda: [])

    def __init__(self, hits):
        self.hits = hits
        self.total = len(self.hits)
