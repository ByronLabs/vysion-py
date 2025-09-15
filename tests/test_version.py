import pytest

from vysion import __version__


def test_version():
    assert __version__ == "2.1.6"
