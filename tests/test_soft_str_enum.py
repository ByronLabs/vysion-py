"""
Regression tests for https://github.com/ByronLabs/vysion-py/issues/67

The external ``softenum`` package caused RecursionError on Python 3.13/3.14.
It has been replaced by ``vysion.model.enum.base.SoftStrEnum``, a stdlib
``Enum`` with a ``_missing_`` hook that accepts unknown values.
"""

from vysion.dto.tag import Namespace, Predicate, Tag
from vysion.model.enum import RansomGroup
from vysion.model.enum.base import SoftStrEnum


def test_known_value_resolves_to_member():
    assert RansomGroup("LockBit") is RansomGroup.lockbit
    assert Namespace("cccs") is Namespace.cccs


def test_unknown_value_does_not_raise():
    group = RansomGroup("Some Brand New Group")
    assert isinstance(group, RansomGroup)
    assert isinstance(group, str)
    assert group == "Some Brand New Group"
    assert group.value == "Some Brand New Group"


def test_members_are_plain_strings():
    assert RansomGroup.lockbit == "LockBit"
    assert isinstance(RansomGroup.lockbit, str)
    assert Namespace.cccs + "-suffix" == "cccs-suffix"


def test_non_str_value_still_raises():
    import pytest

    with pytest.raises(ValueError):
        RansomGroup(42)


def test_tag_parse_roundtrip():
    tag = Tag.parse('cccs:malware-category="ransomware"')
    assert tag.namespace == "cccs"
    assert tag.predicate == "malware-category"
    assert tag.value == "ransomware"
    assert str(tag) == 'cccs:malware-category="ransomware"'


def test_tag_parse_unknown_namespace():
    tag = Tag.parse('some-new-namespace:some-predicate="value"')
    assert tag.namespace == "some-new-namespace"
    assert tag.predicate == "some-predicate"


def test_enum_classes_use_stdlib_only():
    import enum

    assert issubclass(SoftStrEnum, enum.Enum)
    assert issubclass(RansomGroup, enum.Enum)
    assert issubclass(Namespace, enum.Enum)
    assert issubclass(Predicate, enum.Enum)
