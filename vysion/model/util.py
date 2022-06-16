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

    '''# SAMPLE API's RESPONSE (20220613)
        
        $ curl --location --request GET 'https://vysion-api-secured-afkbm06.nw.gateway.dev/api/v1/email/purplefdw@protonmail.ch' --header 'Accept: application/json' --header 'x-api-key: *********************' | jq 

        {
        "total": {
            "value": 3,
            "relation": "eq"
        },
        "max_score": null,
        "hits": [
            {
            "_index": "vysion-062022",
            "_id": "614d869a896a534dd40ac36d",
            "_score": null,
            "_source": {
                "protocol": "http",
                "domain": "trollodrome2.torpress2sarn7xw.onion",
                "port": 80,
                "path": "/topic/service-%f0%9f%92%80-hacking-2/",
                "signature": "27749d192f4a9cdc603b1fd94cf599ad",
                "parent": "421b5f3b1a8c8cd2f51dba70b658d278",
                "date": "2021-10-21T08:53:43.626235",
                "network": "tor",
                "sha1sum": null,
                "ssdeep": null,
                "title": "SERVICE 💀 HACKING – Le Trollodrôme 2.0",
                "url": "trollodrome2.torpress2sarn7xw.onion/topic/service-%f0%9f%92%80-hacking-2/",
                "language": "fr",
                "html": null,
                "email": [
                "purplefdw@protonmail.ch"
                ],
                "pastebin-dumps": [],
                "skype": [],
                "telegram": [],
                "whatsapp": []
            },
            "sort": [
                1634806423626
            ]
            },
            {
            "_index": "vysion-062022",
            "_id": "614d868d896a534dd40ac212",
            "_score": null,
            "_source": {
                "protocol": "http",
                "domain": "trollodrome2.torpress2sarn7xw.onion",
                "port": 80,
                "path": "/topic/service-%f0%9f%92%80-hack/",
                "signature": "28d781c04f157e07224744a589b6de67",
                "parent": "421b5f3b1a8c8cd2f51dba70b658d278",
                "date": "2021-10-21T08:53:43.561108",
                "network": "tor",
                "sha1sum": null,
                "ssdeep": null,
                "title": "SERVICE 💀 HACK – Le Trollodrôme 2.0",
                "url": "trollodrome2.torpress2sarn7xw.onion/topic/service-%f0%9f%92%80-hack/",
                "language": "fr",
                "html": null,
                "email": [
                "purplefdw@protonmail.ch"
                ],
                "pastebin-dumps": [],
                "skype": [],
                "telegram": [],
                "whatsapp": []
            },
            "sort": [
                1634806423561
            ]
            },
            {
            "_index": "vysion-062022",
            "_id": "614d8535896a534dd40aa47b",
            "_score": null,
            "_source": {
                # URL
                "protocol": "http",
                "domain": "tor66sewebgixwhcqfnp5inzp5x5uohhdy3kvtnyfxc2e5mxiuh34iid.onion",
                "port": 80,
                "path": "/about",
                "signature": "62ab8067d6d4fe91074283cd70767414",
                "parent": "7c9de3f17e87b5d42d920ccddeac5a48",
                "network": "tor",

                "date": "2021-10-21T08:53:42.560068",
                
                "title": "Tor66 - About",
                "language": "en",
                "html": null,
                "sha1sum": null,
                "ssdeep": null,
                "email": [
                "torservice77@protonmail.ch"
                ],
                "pastebin-dumps": [],
                "skype": [],
                "telegram": [],
                "whatsapp": []
            },
            "sort": [
                1634806422560
            ]
            }
        ]
        }
    '''

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
        paste = [Paste(value=v) for v in source.get('paste', [])] 
        skype = [Skype(value=v) for v in source.get('skype', [])]
        telegram = [Telegram(value=v) for v in source.get('telegram', [])]
        whatsapp = [WhatsApp(value=v) for v in source.get('whatsapp', [])]

        hit = Hit(page=page, email=email, paste=paste, skype=skype, telegram=telegram, whatsapp=whatsapp)
        
        hits.append(hit)
    
    return Result(hits=hits)
