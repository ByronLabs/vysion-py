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

from typing import List
from .model import URL, Email, Hit, Network, Page, Paste, Result, Skype, Telegram, WhatsApp

def process_response(raw_elk_hits: List[dict]) -> Result:

    hits = []

    for raw_hit in raw_elk_hits:

        # TODO Create builder
        source = raw_hit['_source']

        url = URL(
            protocol=source.get('protocol'),
            domain=source.get('domain'),
            port=source.get('port'),
            path=source.get('path'),
            signature=source.get('signature'),
            network=Network(value=source.get('network')),
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

        hit = Hit(page=page, email=email, paste=paste, skype=skype, telegram=telegram, whatsapp=whatsapp)
        
        hits.append(hit)
    
    return Result(hits=hits)
