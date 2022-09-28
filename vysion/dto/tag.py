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
from pydantic import BaseModel
from softenum import Softenum
from typing import Optional

'''
https://github.com/MISP/misp-taxonomies
'''


class Namespace(str, Softenum):

    cccs = "cccs"


class Predicate(str, Softenum):

    malware_category = "malware-category"


class Tag(BaseModel):

    namespace: Namespace
    predicate: Predicate
    value: Optional[str]

    @staticmethod
    def parse(tag_str):
        raise NotImplementedError()

    def __repr__(self):
        return f'''{self.namespace}:{self.predicate}:"{self.value}"'''
