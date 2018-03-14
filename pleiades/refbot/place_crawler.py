#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Crawl through Pleiades place resources."""

import logging
from os import walk
from os.path import abspath, isdir, realpath

logger = logging.getLogger(__name__)


class PlaceCrawler():
    """A class to crawl a hierarchical directory tree of Pleiades place JSON.
    """

    def __init__(self, json_path, sniff=True):
        """Initialize the PlaceCrawler class and sniff the JSON tree."""
        self.json_path = abspath(realpath(json_path))
        if sniff:
            if not isdir(self.json_path):
                raise IOError(
                    '{} is not a valid directory path'.format(self.json_path))
            self._count_json_files()
        else:
            self.count = -1

    def _count_json_files(self):
        """Walk the tree and json_path and count each JSON file visited."""
        self.count = 0
        for root, dirs, files in walk(self.json_path):
            logger.debug('at {}: {}'.format(root, repr(files)))
            json_files = [f for f in files if f.endswith('.json')]
            logger.debug('json_files: {}'.format(repr(json_files)))
            self.count += len(json_files)
