#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Crawl through Pleiades place resources."""

import logging
from os import walk
from os.path import abspath, isdir, realpath, splitext

logger = logging.getLogger(__name__)


class Walker():
    """Change me."""

    def __init__(self, path: str, extensions=[]):
        self.path = abspath(realpath(path))
        if not isdir(self.path):
            raise IOError(
                '{} is not a valid directory path'.format(self.path))
        self.count = False
        self.extensions = [e.lower() for e in extensions]

    def walk(self, count=True):
        if count:
            self.count = 0
        for root, dirs, files in walk(self.path):
            logger.debug('at {}: {}'.format(root, repr(files)))
            if len(self.extensions) > 0:
                select_files = [
                    f for f in files if splitext(f)[1].lower()
                    in self.extensions]
            else:
                select_files = files
            logger.debug('selected files: {}'.format(sorted(select_files)))
            if count:
                self.count += len(select_files)
            self._do(select_files)
        return self.count

    def _do(self, files):
        """Perform some action on files at a directory node."""
        pass


class PlaceCrawler():
    """A class to crawl a hierarchical directory tree of Pleiades place JSON.
    """

    def __init__(self, json_path, count=True):
        """Initialize the PlaceCrawler class and sniff the JSON tree."""
        self.json_path = json_path
        self.count = False
        if count:
            self._count_json_files()

    def _count_json_files(self):
        """Walk the tree and json_path and count each JSON file visited."""
        walker = Walker(self.json_path, ['.json'])
        self.count = walker.walk(count=True)
