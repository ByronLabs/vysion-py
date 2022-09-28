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
import json
from pymisp import MISPAttribute, MISPEvent, MISPObject, MISPTag

try:
    from types import NoneType
except:
    NoneType = type(None)

import vysion.dto as dto
from vysion.dto import Hit, RansomFeedHit, Page, URL


class MISPProcessor:

    def __init__(self):
        self.misp_event = MISPEvent()

    def parse_hit(self, hit: Hit, ref_attribute: MISPAttribute = None, **_):

        page: Page = hit.page

        # TODO Add more page parameters
        misp_object = MISPObject("vysion-page")
        misp_object.template_uuid = "4d0b66f1-5268-47e0-9d29-f2e4f3db8e7f"

        page_id = page.id
        misp_object.add_attribute("id", type="text", value=page_id)

        url: URL = page.url
        misp_object.add_attribute("url", type="url", value=url.build())

        network = url.network
        misp_object.add_attribute("network", type="text", value=network)

        title = page.title
        misp_object.add_attribute("title", type="text", value=title)

        if ref_attribute is not None:
            misp_object.add_reference(ref_attribute.uuid, "associated-to")
  
        self.misp_event.add_object(misp_object)

        vysion_reference_id = misp_object.uuid

        # TODO Remove this addition when the vysion-page object works
        self.misp_event.add_attribute("url", value=url.build())

        self.misp_event.add_attribute("domain", value=url.domain)

        for email in hit.email:
            self.misp_event.add_attribute("email", value=email.value)

        for btc in hit.bitcoin_address:
            self.misp_event.add_attribute("btc", value=btc.value)

        for dot in hit.polkadot_address:
            self.misp_event.add_attribute("dot", value=dot.value)

        for eth in hit.ethereum_address:
            self.misp_event.add_attribute("eth", value=eth.value)

        for xmr in hit.monero_address:
            self.misp_event.add_attribute("xmr", value=xmr.value)

        for xrp in hit.ripple_address:
            self.misp_event.add_attribute("xrp", value=xmr.value)

        for zec in hit.zcash_address:
            self.misp_event.add_attribute("zec", value=zec.value)

        for tag in hit.tag:
            self.misp_event.add_tag(str(tag))

    def parse_ransom_feed_hit(self, hit: RansomFeedHit, **kwargs):

        # TODO Add event info!

        misp_object = MISPObject("vysion-ransomware-feed")
        misp_object.template_uuid = "e0bfa994-c184-4894-bfaa-73b1350746e1"
        misp_object["meta-category"] = "misc" # TODO Esto se tiene que poder hacer de otra manera... Y sólo es necesario en los feeds

        misp_object.add_attribute("id", type="text", value=hit.id)
        misp_object.add_attribute("company", type="target-org", value=hit.company)
        misp_object.add_attribute("company_link", type="link", value=hit.company_link)
        misp_object.add_attribute("link", type="link", value=hit.link)
        misp_object.add_attribute("group", type="threat-actor", value=hit.group)
        misp_object.add_attribute("date", type="datetime", value=hit.date)
        misp_object.add_attribute("info", type="text", value=hit.info)
        misp_object.add_attribute("country", type="text", value=hit.country)

        self.misp_event.add_object(misp_object)

    def process(self, result: dto.Result, **kwargs) -> MISPEvent:

        processor = {
            Hit: self.parse_hit,
            RansomFeedHit: self.parse_ransom_feed_hit,
        }.get(result.get_type(), lambda *_, **__: {})

        for hit in result.hits:
            processor(hit, **kwargs)

        return self.misp_event
