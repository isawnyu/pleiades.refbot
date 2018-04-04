#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Provide Zotero support for pleiades.refbot."""

import csv
import logging
from os.path import abspath, realpath
logger = logging.getLogger(__name__)


class ZoteroRecord(dict):
    """Store and manipulate data from a single Zotero record."""

    __getattr__ = dict.__getitem__

    def __init__(self, **kwargs):
        dict.__init__(self, **kwargs)

    def __str__(self):
        f = '{}({{}}): "{{}}"'.format(
            str(type(self)).split("'")[1].split('.')[-1])
        s = ''
        for k in ['ShortTitle', 'Title']:
            try:
                s = self[k]
            except KeyError:
                continue
            else:
                break
        if s != '':
            return f.format(self['Key'], s)
        return repr(self)


class ZoteroCollection:
    """Store and manipulate data for a collection of Zotero records."""

    def __init__(self, records: list = None):
        self.__records = {}
        if records is not None:
            self.records = records

    def __len__(self):
        return len(self.__records)

    def load_csv(self, path):
        self.filename = abspath(realpath(path))
        with open(self.filename, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.add_record(row)

    def add_record(self, record: dict):
        self.__records[record['Key']] = ZoteroRecord(**record)

    def match(self, fields: dict, operator='and'):
        candidates = self.records
        if operator == 'and':
            for key, value in fields.items():
                candidates = [c for c in candidates if c[key] == value]
            return candidates
        else:
            raise NotImplementedError(
                'operator "{}" is not supported'.format(operator))

    def validate(self, criteria={}):
        failures = {}
        for ck, cv in criteria.items():
            if ck == 'required':
                for field in cv:
                    for r in self.records:
                        try:
                            value = r[field]
                        except KeyError:
                            _fail(failures, r['Key'], 'unexpected', field)
                        else:
                            if len(value.strip()) == 0:
                                _fail(failures, r['Key'], ck, field)
            else:
                raise NotImplementedError(
                    'cannot validate a ZoteroCollection based on {}'
                    ''.format(ck))
        return failures

    @property
    def records(self):
        return [v for k, v in self.__records.items()]

    @records.setter
    def records(self, records: list):
        for record in records:
            self.add_record(record)


def _fail(failures, record_key, criterion, detail):
    try:
        invalid = failures[record_key]
    except KeyError:
        failures[record_key] = {}
        invalid = failures[record_key]
    try:
        failure = invalid[criterion]
    except KeyError:
        invalid[criterion] = []
        failure = invalid[criterion]
    failure.append(detail)
