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
from pymisp import MISPAttribute, MISPEvent, MISPObject

try:
    from types import NoneType
except:
    NoneType = type(None)

import vysion.model as model
from vysion.model.model import Hit, RansomFeedHit


class MISPProcessor():

    def __init__(self):
        self.misp_event = MISPEvent()

    def parse_hit(self, hit: model.Hit):

        page: model.Page = hit.page

        misp_object = MISPObject('vysion-page')

        page_id = page.id
        misp_object.add_attribute('id', type='text', value=page_id)

        url = page.url
        misp_object.add_attribute('url', type='url', value=url.build())

        network = url.network
        misp_object.add_attribute('network', type='text', value=network)

        # misp_object.add_reference(misp_attribute.uuid, 'associated-to')

        # TODO Add more page parameters

        self.misp_event.add_object(misp_object)

        vysion_reference_id = misp_object.uuid

        # TODO Remove this addition when the vysion-page object works
        self.misp_event.add_attribute('url', value=url.build())

        self.misp_event.add_attribute('domain', value=url.domain)

        for email in hit.email:
            self.misp_event.add_attribute('email', value=email.value)

        for btc in hit.bitcoin_address:
            self.misp_event.add_attribute('btc', value=btc.value)

    def parse_ransom_feed_hit(self, hit: model.RansomFeedHit):

        misp_object = MISPObject('vysion-ransomware-feed')
        misp_object.add_attribute('id', type='text', value=hit.id)
        misp_object.add_attribute(
            'company', type='target-org', value=hit.company)
        misp_object.add_attribute(
            'company_link', type='link', value=hit.company_link)
        misp_object.add_attribute('link', type='link', value=hit.link)
        misp_object.add_attribute(
            'group', type="threat-actor", value=hit.group)
        misp_object.add_attribute('date', type='date', value=hit.date)
        misp_object.add_attribute('info', type='text', value=hit.info)
        self.misp_event.add_object(misp_object)

    def process(self, result: model.Result) -> MISPEvent:

        processor = {
            Hit: self.parse_hit,
            RansomFeedHit: self.parse_ransom_feed_hit
        }.get(result.get_type(), lambda *_, **__: {})

        for hit in result.hits:
            processor(hit)

        return self.misp_event
