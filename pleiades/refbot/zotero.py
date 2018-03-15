#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Provide Zotero support for pleiades.refbot."""

import logging
logger = logging.getLogger(__name__)


class ZoteroRecord(dict):
    """Store and manipulate data from a single Zotero record."""

    __getattr__ = dict.__getitem__

    def __init__(self, **kwargs):
        dict.__init__(self, **kwargs)

    def __str__(self):
        f = '<{}={{}}:{{}}>'.format(str(type(self)).split("'")[1])
        for k in ['shortTitle', 'title']:
            s = self[k]
            if s != '':
                return f.format(self['key'], s)
        return repr(self)


class ZoteroCollection:
    """Store and manipulate data for a collection of Zotero records."""

    def __init__(self):
        pass
