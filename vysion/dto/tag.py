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
import re
from typing import Optional

from pydantic import BaseModel, ConfigDict
from softenum import Softenum

"""
https://github.com/MISP/misp-taxonomies
"""


class Namespace(str, Softenum):

    cccs = "cccs"


class Predicate(str, Softenum):

    malware_category = "malware-category"


class Tag(BaseModel):

    namespace: str
    predicate: str
    value: Optional[str]

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @classmethod
    def parse(cls, tag_str):

        tag_parts = re.findall(r"(?:([^:]+):)?(?:([^=]+)=)?(?:\"(.*)\")", tag_str)[0]

        namespace = Namespace(tag_parts[0])
        predicate = Predicate(tag_parts[1])
        value = tag_parts[2]

        return cls(namespace=namespace, predicate=predicate, value=value)

    def __repr__(self):
        return f"Tag<{self}>"

    def __str__(self):
        return f'''{self.namespace}:{self.predicate}="{self.value}"'''
