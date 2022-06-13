#!/bin/env python3

# TODO Referenciar vt-py

import requests
import json
from enum import Enum

from vysion.model import models


_API_HOST = 'https://api.vysion.ai'

# All API endpoints start with this prefix, you don't need to include the
# prefix in the paths you request as it's prepended automatically.
_ENDPOINT_PREFIX = '/api/v1'


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


class VysionURL():
  pass
      
class VysionPage(VysionData):

  def __init__(self, page:models.Page):


class Client():

    def __init__(self, apiKey:str, headers:dict=None, proxy:dict=None):
        
        assert isinstance(apiKey, str)

        self.apiKey = apiKey
        self.proxy = proxy

    def __get_session__(self) --> requests.requests.Session:

        if not self._session_:

            headers = self.headers.copy()
            headers.update({
                "X-API-KEY": self.apiKey,
            })

            self._session_ = requests.Session(headers=headers)

        return self._session_

    def add_url(self, url:str, type:VysionURL.Type):
        """Add a Tor URL to be analyzed by PARCHE.

        :param url: URL to be scanned.
        :param type: Instance of :class:`VysionURL.Type`
        :returns: An instance of :class:`VysionResponse`
        """
        pass

    def find_btc(self):
        pass

    def find_onion(self):
        pass

    def find_email(self, value):
        session = self.__get_session__()




'''
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