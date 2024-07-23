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
import os
from datetime import datetime, timedelta
from typing import Union
from urllib.parse import quote, urlencode, urljoin

# from pydantic import validate_arguments
import requests

import vysion.dto as dto
from vysion.client.error import APIError
from vysion.dto import Error
from vysion.version import __version__ as vysion_version

# All API endpoints start with this prefix, you don't need to include the
# prefix in the paths you request as it's prepended automatically.
_ENDPOINT_PREFIX = "/api/v2/"

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

    def _get_api_host(self):
        if os.getenv("API_HOST") is not None:
            api_host = os.getenv("API_HOST")

        else:
            api_host = "https://api.vysion.ai"

        return api_host

    def _build_api_url__(self, endpoint, param=None, **query_params):
        _API_HOST = self._get_api_host()
        _BASE_API = urljoin(_API_HOST, _ENDPOINT_PREFIX)
        base = urljoin(_BASE_API, endpoint)

        if param is not None:
            param = quote(param, safe="")
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
        print(url)
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

        result = dto.VysionResponse.model_validate(payload)

        return result


def vysion_error_manager(method) -> Union[dto.VysionResponse, Error]:
    def manage(*args, **kwargs):
        try:
            result = method(*args, **kwargs)
            return result
        except APIError as e:
            return Error(code=e.code, message=e.message)
        except Exception as e:
            LOGGER.error(e)
            return Error()

    return manage


class Client(BaseClient):
    @vysion_error_manager
    def status(self):
        # TODO Check API status
        pass

    #
    # Darknet document search
    #

    @vysion_error_manager
    def search(
        self,
        q: str,
        lte: datetime = None,
        gte: datetime = None,
        page: int = 1,
        page_size: int = 10,
        network: dto.Network = None,
        language: dto.Language = None,
        include_tag: str = None,
        exclude_tag: str = None,
    ) -> dto.VysionResponse:
        url = self._build_api_url__(
            "document/search",
            q=q,
            lte=lte,
            gte=gte,
            page=page,
            page_size=page_size,
            network=network,
            language=language,
            include_tag=include_tag,
            exclude_tag=exclude_tag,
        )

        result = self._make_request(url)
        return result.data

    @vysion_error_manager
    def get_document(self, document_id: str) -> dto.VysionResponse:
        url = self._build_api_url__("document", document_id)

        result = self._make_request(url)
        return result.data

    @vysion_error_manager
    def find_url(
        self,
        url: str,
        page: int = 1,
        lte: datetime = None,
        gte: datetime = None,
    ) -> dto.VysionResponse:
        url = self._build_api_url__("document/url", url, page=page, lte=lte, gte=gte)

        result = self._make_request(url)
        return result.data

    @vysion_error_manager
    def get_tag(self, tag: str) -> dto.VysionResponse:
        url = self._build_api_url__("document/tag", tag)

        result = self._make_request(url)
        return result.data

    @vysion_error_manager
    def find_email(
        self, email: str, page: int = 1, lte: datetime = None, gte: datetime = None
    ) -> dto.VysionResponse:
        url = self._build_api_url__(
            "document/email", email, page=page, lte=lte, gte=gte
        )

        result = self._make_request(url)
        return result.data

    @vysion_error_manager
    def find_wallet(
        self,
        chain: str,
        address: str,
        page: int = 1,
        lte: datetime = None,
        gte: datetime = None,
    ) -> dto.VysionResponse:
        url = self._build_api_url__(
            "document/wallet", chain + "/" + address, page=page, lte=lte, gte=gte
        )

        result = self._make_request(url)
        return result.data

    @vysion_error_manager
    def get_document_html(self, document_id: str) -> str:
        url = self._build_api_url__("html", document_id)

        result = requests.get(url)

        return result.text

    #
    # Ransowmare Victims Search
    #

    @vysion_error_manager
    def search_ransomware_victim(
        self,
        q: str,
        lte: datetime = None,
        gte: datetime = None,
        page: int = 1,
        page_size: int = 10,
        network: dto.Network = None,
        country: str = None,
        language: dto.Language = None,
    ) -> dto.VysionResponse:
        url = self._build_api_url__(
            "victim/search",
            q=q,
            lte=lte,
            gte=gte,
            page=page,
            page_size=page_size,
            network=network,
            country=country,
            language=language,
        )

        result = self._make_request(url)
        return result.data

    #
    # Ransomware Stats
    #

    @vysion_error_manager
    def ransomware_countries_stats(
        self,
        gte: datetime = None,
        lte: datetime = None,
    ) -> dto.VysionResponse[dto.Stat]:
        url = self._build_api_url__("stats/countries", gte=gte, lte=lte)

        result = self._make_request(url)
        return result.data

    @vysion_error_manager
    def ransomware_groups_stats(
        self,
        gte: datetime = None,
        lte: datetime = None,
    ) -> dto.VysionResponse[dto.Stat]:
        url = self._build_api_url__("stats/groups", gte=gte, lte=lte)

        result = self._make_request(url)
        return result.data

    @vysion_error_manager
    def ransomware_attacks_stats(
        self,
        gte: datetime = None,
        lte: datetime = None,
    ) -> dto.VysionResponse[dto.Stat]:
        url = self._build_api_url__("stats/attacks", gte=gte, lte=lte)

        result = self._make_request(url)
        return result.data

    #
    # IM Search
    #

    @vysion_error_manager
    def search_im(
        self,
        platform: str,
        q: str,
        gte: datetime = None,
        lte: datetime = None,
        page: int = 1,
        username: str = None,
    ) -> dto.VysionResponse[dto.ImMessageHit]:
        url = self._build_api_url__(
            "im/" + platform + "/search",
            q=q,
            gte=gte,
            lte=lte,
            page=page,
            username=username,
        )

        result = self._make_request(url)
        return result.data

    @vysion_error_manager
    def get_im_chat(
        self, platform: str, channelId: str
    ) -> dto.VysionResponse[dto.ImMessageHit]:
        url = self._build_api_url__("im/" + platform + "/chat/", channelId)

        result = self._make_request(url)
        return result.data

    @vysion_error_manager
    def get_im_profile(
        self, platform: str, userId: str
    ) -> dto.VysionResponse[dto.ImProfileHit]:
        url = self._build_api_url__("im/" + platform + "/profile/", userId)

        result = self._make_request(url)
        return result.data

    @vysion_error_manager
    def get_im_message(
        self, platform: str, messageId: str
    ) -> dto.VysionResponse[dto.ImMessageHit]:
        url = self._build_api_url__("im/" + platform + "/message/", messageId)

        result = self._make_request(url)
        return result.data

    @vysion_error_manager
    def get_im_channel(
        self, platform: str, channelId: str
    ) -> dto.VysionResponse[dto.ImChannelHit]:
        url = self._build_api_url__("im/" + platform + "/channel/", channelId)

        result = self._make_request(url)
        return result.data

    #
    # FEEDS
    #

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
