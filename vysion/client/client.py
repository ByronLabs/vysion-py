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

import logging
from datetime import datetime, timedelta
from typing import Union
from urllib.parse import urlencode, urljoin

# from pydantic import validate_arguments
import requests

import vysion.dto as dto
from vysion.client.error import APIError
from vysion.dto import VysionError
from vysion.version import __version__ as vysion_version

_API_HOST = "https://api.vysion.ai"

# All API endpoints start with this prefix, you don't need to include the
# prefix in the paths you request as it's prepended automatically.
_ENDPOINT_PREFIX = "/api/v1/"

_BASE_API = urljoin(_API_HOST, _ENDPOINT_PREFIX)

LOGGER = logging.getLogger("vysion-py")
LOGGER.setLevel(logging.INFO)

# __all__ = []


class BaseClient:

    # __attrs__ = []

    # @validate_arguments #
    def __init__(self, api_key: str = None, headers: dict = dict(), proxy: dict = None):

        assert api_key is not None, "API key MUST be provided"
        assert isinstance(api_key, str), "API key MUST be a string"

        self.api_key = api_key
        self.proxy = proxy  # TODO Rename proxy to proxies
        self.headers = headers

    def __get_session__(self) -> requests.Session:

        # TODO Configure proxy

        # If session is undefined
        try:
            self._session
        except (NameError, AttributeError):

            headers = self.headers.copy()
            headers.update(
                {
                    "X-API-KEY": self.api_key,
                    "User-Agent": "vysion-py/%s" % vysion_version,
                }
            )

            self._session: requests.Session = requests.Session()
            self._session.headers.update(headers)
            self._session.proxies = self.proxy

        return self._session

    def _build_api_url__(self, endpoint, param, **query_params):

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

    def _make_request(self, url: str) -> dto.VysionResponse:

        session = self.__get_session__()
        r = session.get(url)

        # TODO Improve this
        if r.status_code != 200:
            try:
                err = r.json()
                code = err.get("code")
                message = err.get("message")
            except:
                code = r.status_code
                message = r.text

            raise APIError(code, message)

        payload = r.json()

        result = dto.VysionResponse.parse_obj(payload)

        return result


def vysion_error_manager(method) -> Union[dto.Result, VysionError]:

    def manage(*args, **kwargs):
        try:
            result = method(*args, **kwargs)
            return result
        except APIError as e:
            return VysionError(code=e.code, message=e.message)
        except Exception as e:
            LOGGER.error(e)
            return VysionError()

    return manage


class Client(BaseClient):

    # def add_url(self, url:str, type:VysionURL.Type):
    #     """Add a Tor URL to be analyzed by PARCHE.

    #     :param url: URL to be scanned.
    #     :param type: Instance of :class:`VysionURL.Type`
    #     :returns: An instance of :class:`VysionResponse`
    #     """
    #     pass

    # def find_onion(self):
    #   pass

    # def add_onion(self):
    #   pass

    # def consume_feed(self):
    #   pass

    @vysion_error_manager
    def status(self):
        # TODO Check API status
        pass

    @vysion_error_manager
    def search(
        self,
        query: str,
        tag: str = None,
        notTag: str = None,
        exact: bool = False,
        network: dto.Network = None,
        language: dto.Language = None,
        page: int = 1,
        lte: datetime = None,
        gte: datetime = None,
    ) -> dto.Result:

        url = self._build_api_url__(
            "search",
            query,
            tag=tag,
            notTag=notTag,
            exact=exact,
            network=network,
            language=language,
            page=page,
            lte=lte,
            gte=gte,
        )

        result = self._make_request(url)
        return result.data

    @vysion_error_manager
    def find_btc(
        self, btc: str, page: int = 1, lte: datetime = None, gte: datetime = None
    ) -> dto.Result:

        url = self._build_api_url__("btc", btc, page=page, lte=lte, gte=gte)

        result = self._make_request(url)
        return result.data

    @vysion_error_manager
    def find_eth(
        self, eth: str, page: int = 1, lte: datetime = None, gte: datetime = None
    ) -> dto.Result:

        url = self._build_api_url__("eth", eth, page=page, lte=lte, gte=gte)

        result = self._make_request(url)
        return result.data

    @vysion_error_manager
    def find_dot(
        self, dot: str, page: int = 1, lte: datetime = None, gte: datetime = None
    ) -> dto.Result:

        url = self._build_api_url__("dot", dot, page=page, lte=lte, gte=gte)

        result = self._make_request(url)
        return result.data

    @vysion_error_manager
    def find_xrp(
        self, xrp: str, page: int = 1, lte: datetime = None, gte: datetime = None
    ) -> dto.Result:

        url = self._build_api_url__("xrp", xrp, page=page, lte=lte, gte=gte)

        result = self._make_request(url)
        return result.data

    @vysion_error_manager
    def find_xmr(
        self, xmr: str, page: int = 1, lte: datetime = None, gte: datetime = None
    ) -> dto.Result:

        url = self._build_api_url__("xmr", xmr, page=page, lte=lte, gte=gte)

        result = self._make_request(url)
        return result.data

    @vysion_error_manager
    def find_zec(
        self, zec: str, page: int = 1, lte: datetime = None, gte: datetime = None
    ) -> dto.Result:

        url = self._build_api_url__("zec", zec, page=page, lte=lte, gte=gte)

        result = self._make_request(url)
        return result.data

    # TODO find_domain?
    @vysion_error_manager
    def find_url(
        self,
        query_url: str,
        page: int = 1,
        lte: datetime = None,
        gte: datetime = None,
    ) -> dto.Result:

        url = self._build_api_url__(
            "url", query_url, page=page, lte=lte, gte=gte
        )

        result = self._make_request(url)
        return result.data

    @vysion_error_manager
    def find_email(
        self, email: str, page: int = 1, lte: datetime = None, gte: datetime = None
    ) -> dto.Result:

        url = self._build_api_url__(
            "email", email, page=page, lte=lte, gte=gte
        )

        result = self._make_request(url)
        return result.data

    @vysion_error_manager
    def get_document(self, document_id: str) -> dto.Result:

        url = self._build_api_url__("document", document_id)

        result = self._make_request(url)
        return result.data

    @vysion_error_manager
    def get_tag(self, tag: str) -> dto.Result:

        url = self._build_api_url__("tag", tag)

        result = self._make_request(url)
        return result.data

    # FEEDS
    @vysion_error_manager
    def consume_feed_ransomware(self, batch_day: datetime = datetime.today()):
        pass


# TODO Develop feeds logic
# Example: https://github.com/VirusTotal/vt-py/blob/master/vt/feed.py
class DaylyFeed(Client):
    def _consume_batch(self, start_time, end_time):
        raise NotImplementedError()

    def consume(self, batch_day: datetime = datetime.today()):
        start_time = datetime(datetime.year, datetime.month, datetime.day)
        end_time = start_time + timedelta(days=1)
        return self._consume_batch(start_time, end_time)


class RansomwareFeed(DaylyFeed):
    def _consume_batch(self, start_time, end_time):

        days = (datetime.now() - start_time).days
        pages = (end_time - start_time).days

        for page in range(pages):
            url = self._build_api_url__("feed", "ransomware", days=days, page=page + 1)
            yield self._make_request(url)



# TODO /api/v1/feeds
