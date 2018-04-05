#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validate the Pleiades Zotero Library
"""

from airtight.cli import configure_commandline
import csv
import logging
from os.path import abspath, isdir, join, realpath
from pleiades.refbot.zotero import ZoteroCollection


DEFAULT_LOG_LEVEL = logging.WARNING
OPTIONAL_ARGUMENTS = [
    # each row is a list with 5 elements: short option, long option,
    # default value, help text, required
    ['-l', '--loglevel', 'NOTSET',
        'desired logging level (' +
        'case-insensitive string: DEBUG, INFO, WARNING, or ERROR',
        False],
    ['-o', '--output', 'NOTSET', 'path to directory for CSV output of errors',
        False],
    ['-v', '--verbose', False, 'verbose output (logging level == INFO)',
        False],
    ['-w', '--veryverbose', False,
        'very verbose output (logging level == DEBUG)', False]
]
POSITIONAL_ARGUMENTS = [
    # each row is a list with 3 elements: name, type, help text
    ['zotero_csv', str, 'path to the Zotero csv file']
]


def main(**kwargs):
    """
    main function
    """
    # logger = logging.getLogger(sys._getframe().f_code.co_name)
    path = abspath(realpath(kwargs['zotero_csv']))
    zc = ZoteroCollection()
    if kwargs['verbose']:
        print('Loading Zotero CSV file at {} ...'.format(path))
    zc.load_csv(path)
    if kwargs['verbose']:
        print('   Loaded {} records.'.format(len(zc)))
    criteria = {
        'required': ['Title', 'Short Title']
    }
    if kwargs['verbose']:
        print('Validating ...')
    invalid_records = zc.validate(criteria)
    if kwargs['verbose']:
        print('   Validation complete.')
    print('There are {} invalid records.'.format(len(invalid_records)))
    outpath = None
    if kwargs['output'] != 'NOTSET':
        outpath = abspath(realpath(kwargs['output']))
        if not isdir(outpath):
            raise IOError('{} is not a directory'.format(path))
        outf = open(join(outpath, 'zotero_errors.csv'), 'w')
        fieldnames = ['key', 'title', 'criterion', 'fields']
        writer = csv.DictWriter(
            outf, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
    if kwargs['verbose'] or outpath is not None:
        for k, v in invalid_records.items():
            if kwargs['verbose']:
                print('INVALID Zotero Record {}:'.format(k))
                print('        {}'.format(zc.get_record(k)['Title']))
            for criterion, fields in v.items():
                if kwargs['verbose']:
                    print(
                        '        👾  {}: "{}"'
                        ''.format(criterion.upper(), '", "'.join(fields)))
                if outpath is not None:
                    writer.writerow(
                        {
                            'key': k,
                            'title': zc.get_record(k)['Title'],
                            'criterion': criterion,
                            'fields': '|'.join(fields)
                        })

if __name__ == "__main__":
    main(
        **configure_commandline(
            OPTIONAL_ARGUMENTS, POSITIONAL_ARGUMENTS, DEFAULT_LOG_LEVEL))
