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

# TODO Referenciar vt-py

from datetime import datetime
from enum import Enum
import json
from urllib.parse import urljoin, urlencode
from pydantic import validate_arguments
import requests
from vysion.client.error import APIError

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

    def __init__(self, api_key: str, headers: dict = dict(), proxy: dict = None):

        assert isinstance(api_key, str), "API key MUST be a string"

        self.api_key = api_key
        self.proxy = proxy
        self.headers=headers

        self._session = None

    def __get_session__(self) -> requests.Session:

        if self._session is None:

            headers = self.headers.copy()
            headers.update({
                "X-API-KEY": self.api_key,
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

      # TODO Improve this
      if r.status_code != 200:
        raise APIError(r.status_code, r.text)

      response = r.json()
      raw_hits = response.get('hits', [])

      return process_response(raw_hits)


# TODO /api/v1/feeds