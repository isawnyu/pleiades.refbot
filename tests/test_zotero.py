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
            'Date': '2009-10-07',
            'Date Added': '2009-10-14 13:33:17',
            'Date Modified': '2009-10-14 13:33:58',
            'Access Date': '2009-10-14 13:33:17'
        }
        zr = ZoteroRecord(**data)
        for k in data.keys():
            assert_equal(zr[k], data[k])

    def test_zotero_collection(self):
        """Test Zotero collection"""
        data = [
            {
                'Key': '6S3UA6RW',
                'Item Type': 'blogPost',
                'Publication Year': '2009',
                'Author': 'Dempsey, Lorcan',
                'Title': "Discoverability .. a report that's worth a look",
                'Publication Title': "Lorcan Dempsey's weblog",
                'Url': 'http://orweblog.oclc.org/archives/002012.html',
                'Date': '2009-10-07',
                'Date Added': '2009-10-14 13:33:17',
                'Date Modified': '2009-10-14 13:33:58',
                'Access Date': '2009-10-14 13:33:17'
            },
            {
                'Author': 'Erzen, Afif',
                'Call Number': 'DS51.T2 E79 1943',
                'Date': '1943',
                'Date Added': '2014-02-05 17:43:29',
                'Date Modified': '2016-02-25 11:15:05',
                'Extra': 'OCLC: 827268834',
                'Item Type': 'book',
                'Key': 'CUZWAHIZ',
                'Language': 'Turkish',
                'Library Catalog': 'Open WorldCat',
                'Num Pages': '30',
                'Place': 'İstanbul',
                'Publication Year': '1943',
                'Publisher': 'Maarif Matbaası',
                'Series': 'Maarif Vekilliği, Antikiteler ve Müzeler '
                          'Direktörlüğü, Anıtları Koruma Kurulu',
                'Series Number': 'sayı 7',
                'Title': 'Tarsus kılavuzu'
            }
        ]
        zc = ZoteroCollection(data)
        assert_equal(len(zc), 2)
        del zc
        zc = ZoteroCollection()
        assert_equal(len(zc), 0)
        zc.records = data
        assert_equal(len(zc), 2)

    def test_zotero_collection_load_csv(self):
        """Test collection CSV loading"""
        path = join('tests', 'data', 'zotero.csv')
        zc = ZoteroCollection()
        zc.load_csv(path)
        assert_equal(len(zc), 2)

    def test_zotero_match_and(self):
        """Test Zotero collection matching using logical 'and' operator."""
        path = join('tests', 'data', 'zotero.csv')
        zc = ZoteroCollection()
        zc.load_csv(path)
        m = zc.match({'Key': 'CUZWAHIZ'})
        assert_equal(len(m), 1)
        assert_equal(m[0]['Title'], 'Tarsus kılavuzu')
        m = zc.match({'Item Type': 'blogPost', 'Date': '2009-10-07'})
