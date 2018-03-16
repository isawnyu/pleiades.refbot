#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Crawl through Pleiades place resources."""

import logging
import json
from os import walk
from os.path import abspath, isdir, join, realpath, splitext

logger = logging.getLogger(__name__)


class Walker():
    """Selectively visit files in a tree and act on them.

    The following public methods are available:

    - __init__(): takes two arguments when constructing an instance:
      - path: the path to the root of the subtree that is to be walked
      - extensions: a list of strings, each containing a filename extension
        (including the leading '.') to be considered when acting on files found
        in a directory. An empty extensions argument (the default) means that
        all regular files found will be addressed.

    - walk(): Walk the directory subtree rooted at the path specified when
      the instance was constructed. For each batch of files considered (see the
      'extensions' argument to __init__()), the internal '_do()' method is
      called.

    The _do() method:

    Override this method in a subclass in order to specify fun things to do
    to the files that walk() finds.
    """

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
            self._do(root, select_files)
        return self.count

    def _do(self, root, files):
        """Perform some action on files at a directory node."""
        pass


class ReferenceWalker(Walker):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.places = {}

    def _do(self, root, files):
        for file_name in files:
            logger.debug('parsing {}'.format(file_name))
            file_path = join(root, file_name)
            with open(file_path, 'r', encoding='utf-8') as f:
                place = json.load(f)
            del f
            d = {
                'references': [r for r in place['references']],
                'locations': {},
                'names': {},
                'connections': {}
            }
            for location in place['locations']:
                d['locations'][location['id']] = [
                    r for r in location['references']]
            for name in place['names']:
                d['names'][name['id']] = [r for r in name['references']]
            # TBD: for connection in place['connections']:
            self.places[place['id']] = d
            del place


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

    def get_references(self):
        """Walk the tree and extract and store all references encountered."""
        walker = ReferenceWalker(path=self.json_path, extensions=['.json'])
        self.count = walker.walk()
        self.places = walker.places
        self.reference_count = 0
        for pid, pdata in self.places.items():
            self.reference_count += len(pdata['references'])
            for subtype in ['locations', 'names', 'connections']:
                for subid, subrefs in pdata[subtype].items():
                    self.reference_count += len(subrefs)
        return self.places
