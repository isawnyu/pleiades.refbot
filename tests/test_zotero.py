#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test Zotero support for pleiades.refbot"""

import logging
from nose.tools import assert_equal, assert_false, assert_true, raises
from os.path import abspath, join, realpath
from pleiades.refbot.zotero import ZoteroRecord
from unittest import TestCase

logger = logging.getLogger(__name__)
test_data_path = ['tests', 'data']


def setup_module():
    """Change me"""
    pass


def teardown_module():
    """Change me"""
    pass


class Test_Zotero(TestCase):

    def setUp(self):
        """Change me"""
        pass

    def tearDown(self):
        """Change me"""
        pass

    def test_zotero_record(self):
        """Test Zotero record"""
        pass
