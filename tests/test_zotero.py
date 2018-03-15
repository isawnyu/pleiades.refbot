#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test Zotero support for pleiades.refbot"""

import logging
from nose.tools import assert_equal, assert_false, assert_true, raises
from os.path import abspath, join, realpath
from pleiades.refbot.zotero import ZoteroCollection, ZoteroRecord
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
        data = {
            'Key': '6S3UA6RW',
            'Item Type': 'blogPost',
            'Publication Year': '2009',
            'Author': 'Dempsey, Lorcan',
            'Title': "Discoverability .. a report that's worth a look",
            'Publication Title': "Lorcan Dempsey's weblog",
            'Url': 'http://orweblog.oclc.org/archives/002012.html',
            'Abstract Note': 'We are awash in assisted thinking, as I may '
                             'have remarked. One document that is worth a '
                             'look is Discoverability produced earlier this '
                             'year by a team at the University of Minnesota.',
            'Date': '2009-10-07', 'Date Added': '2009-10-14 13:33:17',
            'Date Modified': '2009-10-14 13:33:58',
            'Access Date': '2009-10-14 13:33:17'
        }
        zr = ZoteroRecord(**data)
        for k in data.keys():
            assert_equal(zr[k], data[k])

    def test_zotero_collection(self):
        """Test Zotero collection"""
        pass

