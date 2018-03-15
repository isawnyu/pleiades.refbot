#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Python 3 tests template (changeme)"""

import logging
from nose.tools import assert_equal, assert_false, assert_true, raises
from os.path import abspath, join, realpath
from pleiades.refbot.references import PleiadesReference, ReferenceFixer
from unittest import TestCase

logger = logging.getLogger(__name__)
test_data_path = ['tests', 'data']


def setup_module():
    """Change me"""
    pass


def teardown_module():
    """Change me"""
    pass


class Test_References(TestCase):

    def setUp(self):
        """Change me"""
        pass

    def tearDown(self):
        """Change me"""
        pass

    def test_reference_construction(self):
        """Test Reference Construction"""
        pr = PleiadesReference(short_title='Talbert 2000')
        assert_equal(pr.short_title, 'Talbert 2000')

    def test_reference_history(self):
        """Test Reference History"""
        pr = PleiadesReference(short_title='Talbert 2000')
        assert_equal(pr.short_title, 'Talbert 2000')
        pr.short_title = 'Talbert 2010'
        assert_equal(pr.short_title, 'Talbert 2010')
        assert_equal(len(pr.get_history('short_title')), 2)


