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
from vysion.dto import Error


class APIError(Exception):
    """Class that encapsules errors returned by the Vysion API."""

    @classmethod
    def from_dict(cls, dict_error):
        return cls(dict_error["code"], dict_error.get("message"))

    def __init__(self, code: int, message: str):

        super().__init__()

        if code not in [i.value for i in Error.StatusCode]:
            self.code = Error.StatusCode.UNK
            self.message = f"{message} (Original code: {code})"
        else:
            self.code = code
            self.message = message
