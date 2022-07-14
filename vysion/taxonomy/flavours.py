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


class Flavour:

    _reference: str = None
    _version: str = None

    def __init_subclass__(cls) -> None:

        super().__init_subclass__()

        assert cls._reference is not None, f"{cls.__name__} class needs reference field"
        assert cls._version is not None, f"{cls.__name__} class needs_version field"

    def __init__(self, namespace: str, predicate: str, value: str):

        self._namespace = namespace
        self.predicate = predicate
        self.value = value

    def __repr__(self):
        return f'{self._namespace}:{self.predicate}:"{self.value}"'


class EmptyFlavour(Flavour):

    _reference = "nil"
    _version = "0.0"

    def __init__(self):
        super().__init__(None, None, None)


class DBSafe(Flavour):

    # TODO ¿Por ejemplo?
    _reference = "https://peps.python.org/pep-0008/#naming-conventions"
    _version = "2001"


class MISP(Flavour):

    _reference = "https://github.com/MISP/misp-taxonomies"
    _version = "20220609"


# class STIX(Flavour):
#     pass


# class CASE(Flavour):
#     pass


class Vysion(Flavour):

    _reference = "api.vysion.io"
    _version = "0.0.1"

    def __init__(self, namespace, predicate, value, description=None):

        super().__init__(namespace, predicate, value)
        self.description = description


class Flavours:
    def __init__(self, vysion=None, misp=None, stix=None, case=None, dbsafe=None):

        assert None not in (vysion, misp, stix, case, dbsafe)

        # TODO Each one should contain a list of names?
        self.vysion = vysion
        self.misp = misp
        self.stix = stix
        self.case = case
        self.dbsafe = dbsafe

    def get_flavours(self):
        return [self.vysion, self.misp, self.stix, self.case, self.dbsafe]
