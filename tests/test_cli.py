# -*- coding: utf-8 -*-

import pytest

from mlox_rule_mgr.cli import fib

__author__ = "Kaben Nanlohy"
__copyright__ = "Kaben Nanlohy"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
