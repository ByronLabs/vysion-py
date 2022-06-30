import pytest

import vysion.model as model


def test_invalid():
    try:
        model.wrong()
        assert False
    except:
        assert True
