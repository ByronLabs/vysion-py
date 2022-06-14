#!/bin/env python3.10

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, constr

from vysion import taxonomy as vystaxonomy


# TODO Enums?

class Network(BaseModel):

    value: str


class Language(BaseModel):

    value: str

#-- END ENUMS ---


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


class Page(BaseModel):

    url: URL
    parent: str
    title: str
    language: str
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


class Result(BaseModel):

    total: int = 0
    hits: List[Hit] = Field(default_factory=lambda: [])

    @classmethod
    def process_response(cls, raw_hits: List[dict]) -> List[Hit]:
    
        hits = []
        
        for raw_hit in raw_hits:

            # TODO Create builder
            source = raw_hit['_source']

            url = URL(
                protocol=source.get('protocol'),
                domain=source.get('domain'),
                port=source.get('port'),
                path=source.get('path'),
                signature=source.get('signature'),
                network=Network(value = source.get('network')),
            )

            page = Page(
                url=url, 
                parent=source.get('parent'),
                title=source.get('title'),
                language=source.get('language'),
                html=source.get('html'),
                sha1sum=source.get('sha1sum'),
                ssdeep=source.get('ssdeep'),
                date=source.get('date'),
            )

            email = [Email(value=e) for e in source.get('email', [])]
            paste = [Paste(value=v) for v in source.get('pastebin-dumps', [])] # TODO pastebin-dumps -> paste
            skype = [Skype(value=v) for v in source.get('skype', [])]
            telegram = [Telegram(value=v) for v in source.get('telegram', [])]
            whatsapp = [WhatsApp(value=v) for v in source.get('whatsapp', [])]

            hit = Hit(page  = page, email=email, paste=paste, skype=skype, telegram=telegram, whatsapp=whatsapp)
            
            hits.append(hit)
        
        return cls(hits=hits)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.total = len(self.hits)
