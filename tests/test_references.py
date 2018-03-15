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
        pr = PleiadesReference(
            short_title='Talbert 2000',
            citation_detail='37 A2 Moontown',
            formatted_citation='Sometimes laziness is a virtue')
        assert_equal(pr.short_title, 'Talbert 2000')
        assert_equal(pr.citation_detail, '37 A2 Moontown')
        pr.short_title = 'Talbert 2010'
        assert_equal(pr.short_title, 'Talbert 2010')
        assert_equal(len(pr.get_history('short_title')), 2)
        pr.citation_detail = 'p. 66'
        assert_equal(pr.citation_detail, 'p. 66')

    def test_bibliographic_uri(self):
        """Test bibliographic URI"""
        PleiadesReference(
            bibliographic_uri='https://www.zotero.org/groups/2533/items'
            '/9JN34TQ6')

    @raises(ValueError)
    def test_invalid_bibliographic_uri(self):
        """Test invalid bibliographic URI"""
        PleiadesReference(bibliographic_uri='qzt://hahaha-no')

    @raises(ValueError)
    def test_bibliographic_uri_unrecognized_domain(self):
        """Test bibliographic URI with unrecognized domain"""
        PleiadesReference(
            bibliographic_uri='http://www.worldcat.org/oclc/807699049')

    def test_bibliographic_uri_domains(self):
        """Test bibliographic URI with custom domains."""
        PleiadesReference(
            bibliographic_uri='http://www.worldcat.org/oclc/807699049',
            bibliographic_uri_domains=['zotero.org', 'worldcat.org'])

    def test_access_uri(self):
        """Test access URI"""
        PleiadesReference(
            access_uri='https://www.nytimes.com/')

    @raises(ValueError)
    def test_invalid_access_uri(self):
        """Test invalid access URI"""
        PleiadesReference(access_uri="Who doesn't love pickles?")

    def test_alternate_uri(self):
        """Test alternate URI"""
        PleiadesReference(
            alternate_uri='https://www.nytimes.com/')

    @raises(ValueError)
    def test_invalid_alternate_uri(self):
        """Test invalid alternate URI"""
        PleiadesReference(alternate_uri="Who doesn't love saffron?")

    def test_alternate_uri(self):
        """Test alternate URI"""
        PleiadesReference(
            alternate_uri='https://www.nytimes.com/')

    @raises(ValueError)
    def test_invalid_alternate_uri(self):
        """Test invalid alternate URI"""
        PleiadesReference(alternate_uri="Who doesn't love saffron?")

    def test_other_identifier(self):
        """Test other identifier"""
        pr = PleiadesReference(other_identifier="7773-025S")
        assert_equal(pr.other_identifier, '7773-025S')
