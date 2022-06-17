#!/usr/bin/env python3
"""
   Copyright 2022 Byron Labs S.L.

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
from vysion.model.model import VysionError

_API_HOST = 'https://api.vysion.ai'

# All API endpoints start with this prefix, you don't need to include the
# prefix in the paths you request as it's prepended automatically.
_ENDPOINT_PREFIX = '/api/v1/'

_BASE_API = urljoin(_API_HOST, _ENDPOINT_PREFIX)


class Client:

    @validate_arguments
    def __init__(self, api_key: str, headers: dict = dict(), proxy: dict = None):

        assert isinstance(api_key, str), "API key MUST be a string"

        self.api_key = api_key
        self.proxy = proxy
        self.headers = headers

    def __get_session__(self) -> requests.Session:
        
        # TODO Configure proxy

        # If session is undefined
        try: self._session
        except (NameError, AttributeError):
          
            headers = self.headers.copy()
            headers.update({
                "X-API-KEY": self.api_key,
            })

            self._session = requests.Session()
            self._session.headers.update(headers)

        return self._session

    def _build_api_url_(self, endpoint, param, **query_params):
      
      base = urljoin(_BASE_API, f"{endpoint}/{param}")

      query_params_initialzed = query_params.copy()

      keys = list(query_params.keys())
      keys.sort()

      for i in keys:
        
        v = query_params[i]

        if v is None:
          del query_params_initialzed[i]

      query = "?" + urlencode(query_params_initialzed)

      return urljoin(base, query)

    def __make_request(self, url: str) -> model.VysionResponse:

      session = self.__get_session__()
      r = session.get(url)

      # TODO Improve this
      if r.status_code != 200:
        raise APIError(r.status_code, r.text)

      payload = r.json()

      result = model.VysionResponse.parse_obj(payload)

      return result

    # def add_url(self, url:str, type:VysionURL.Type):
    #     """Add a Tor URL to be analyzed by PARCHE.

    #     :param url: URL to be scanned.
    #     :param type: Instance of :class:`VysionURL.Type`
    #     :returns: An instance of :class:`VysionResponse`
    #     """
    #     pass

    def search(self, query: str, exact: bool = False, network: model.Network = None, language: model.Language = None, page: int = 1, before: datetime = None, after: datetime = None) -> model.Result:
      
      url = self._build_api_url_(
            "search", query, 
            exact = exact, 
            network = network, 
            language = language, 
            page=page, 
            before=before, 
            after=after
      )

      try:
        result = self.__make_request(url)
        return result.data
      except APIError as e:
        return VysionError(e.code, e.message)
      except:
        return VysionError()


    def get_document(self, document_id: str) -> model.Result:
      
      url = self._build_api_url_("document", document_id)

      try:
        result = self.__make_request(url)
        return result.data
      except APIError as e:
        return VysionError(e.code, e.message)
      except:
        return VysionError()

    def find_btc(self):
      
      url = self._build_api_url_("document", document_id)

      try:
        result = self.__make_request(url)
        return result.data
      except APIError as e:
        return VysionError(e.code, e.message)
      except:
        return VysionError()

    # def find_onion(self):
    #   pass

    # def add_onion(self):
    #   pass

    # def consume_feed(self):
    #   pass

    # TODO find_domain?
    def find_url(self, query_url: str, page: int = 1, before: datetime = None, after: datetime = None) -> model.Result:
      
      url = self._build_api_url_("url", query_url, page=page, before=before, after=after)

      try:
        result = self.__make_request(url)
        return result.data
      except APIError as e:
        return VysionError(e.code, e.message)
      except:
        return VysionError()


    def find_email(self, email: str, page: int = 1, before: datetime = None, after: datetime = None) -> model.Result:

      url = self._build_api_url_("email", email, page=page, before=before, after=after)

      try:
        result = self.__make_request(url)
        return result.data
      except APIError as e:
        return VysionError(e.code, e.message)
      except:
        return VysionError()

# TODO /api/v1/feeds
