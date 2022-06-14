#!/usr/bin/env python3.10
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

# TODO Referenciar vt-py

from datetime import datetime
from enum import Enum
import json
from urllib.parse import urljoin, urlencode
from pydantic import validate_arguments
import requests

import vysion.model as model
from vysion.model.util import process_response

_API_HOST = 'https://api.vysion.ai'
_API_HOST = 'https://vysion-api-secured-afkbm06.nw.gateway.dev'

# All API endpoints start with this prefix, you don't need to include the
# prefix in the paths you request as it's prepended automatically.
_ENDPOINT_PREFIX = '/api/v1/'

_BASE_API = urljoin(_API_HOST, _ENDPOINT_PREFIX)

class VysionResponse():
    pass


class VysionData:
    pass


class VysionErrors:
    
    class StatusCode(Enum):

        OK = 200
        INTERNAL_ERROR = 500
        REQ_ERROR = 400
        UNAUTHORIZED = 403



class Client():

    def __init__(self, apiKey:str, headers: dict = dict(), proxy: dict=None):
        
        assert isinstance(apiKey, str), "API key MUST be a string"

        self.apiKey = apiKey
        self.proxy = proxy
        self.headers=headers

        self._session = None

    def __get_session__(self) -> requests.Session:

        if self._session is None:

            headers = self.headers.copy()
            headers.update({
                "X-API-KEY": self.apiKey,
            })

            self._session = requests.Session()
            self._session.headers.update(headers)

        return self._session

    # def add_url(self, url:str, type:VysionURL.Type):
    #     """Add a Tor URL to be analyzed by PARCHE.

    #     :param url: URL to be scanned.
    #     :param type: Instance of :class:`VysionURL.Type`
    #     :returns: An instance of :class:`VysionResponse`
    #     """
    #     pass

    def _build_api_url_(self, endpoint, param, **query_params):
      
      base = urljoin(_BASE_API, f"{endpoint}/{param}")

      query_params_initialzed = query_params.copy()

      for i, v in query_params.items():
        if v is None:
          del query_params_initialzed[i]

      query = "?" + urlencode(query_params_initialzed)

      return urljoin(base, query)

    def search(self, query: str, exact: bool = False, network: model.Network = None, language: model.Language = None, page: int = 1, before: datetime = None, after: datetime = None):
      
      url = self._build_api_url_(
            "search", query, 
            exact = exact, 
            network = network, 
            language = language, 
            page=page, 
            before=before, 
            after=after
      )

      session = self.__get_session__()
      r = session.get(url)

      response = r.json()
      raw_hits = response.get('hits', [])

      return process_response(raw_hits)


    def get_document(self, document_id: str):
      
      url = self._build_api_url_("document", document_id)

      session = self.__get_session__()
      r = session.get(url)

      response = r.json()
      raw_hits = response.get('hits', [])

      return process_response(raw_hits)

    # def find_btc(self):
    #   pass

    # def find_onion(self):
    #   pass

    # def add_onion(self):
    #   pass

    # def consume_feed(self):
    #   pass

    def find_email(self, email: str, page: int = 1, before: datetime = None, after: datetime = None) -> model.Result:
      
      url = self._build_api_url_("email", email, page=page, before=before, after=after)

      session = self.__get_session__()
      r = session.get(url)

      response = r.json()
      raw_hits = response.get('hits', [])

      return process_response(raw_hits)


# https://vysion-api-secured-afkbm06.nw.gateway.dev/api/v1/email/purplefdw@protonmail.ch' \

'''
SAMPLE API's RESPONSE (20220613)
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

# TODO /api/v1/feeds