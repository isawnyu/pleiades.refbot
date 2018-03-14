#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test the place_crawler module."""

import logging
from nose.tools import assert_equal, assert_false, assert_true, raises
from os.path import abspath, join, realpath
from pleiades.refbot.place_crawler import PlaceCrawler
from unittest import TestCase

logger = logging.getLogger(__name__)
test_data_path = ['tests', 'data']
place_json_path = test_data_path
place_json_path.append('place_json')


def setup_module():
    """Module-level setup steps for all place_crawler tests."""
    pass


def teardown_module():
    """Change me"""
    pass


class Test_This(TestCase):

    def setUp(self):
        """Setup steps to run before each place_crawler test."""
        global place_json_path
        self.place_json_path = abspath(realpath(join(*place_json_path)))

    def tearDown(self):
        """Change me"""
        pass

    def test_crawl_count(self):
        """Verify PlaceCrawler successfully visits all JSON files."""
        pc = PlaceCrawler(self.place_json_path)
        assert_equal(pc.count, 11)

    def test_crawl_count_not(self):
        """Verify we can tell PlaceCrawler not to count what it visits."""
        pc = PlaceCrawler(self.place_json_path, count=False)
        assert_equal(pc.count, False)

