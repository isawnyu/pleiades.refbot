#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validate the Pleiades Zotero Library
"""

from airtight.cli import configure_commandline
import logging
from os.path import abspath, realpath
from pleiades.refbot.zotero import ZoteroCollection


DEFAULT_LOG_LEVEL = logging.WARNING
OPTIONAL_ARGUMENTS = [
    # each row is a list with 5 elements: short option, long option,
    # default value, help text, required
    ['-l', '--loglevel', 'NOTSET',
        'desired logging level (' +
        'case-insensitive string: DEBUG, INFO, WARNING, or ERROR',
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
    if kwargs['verbose']:
        for k, v in invalid_records.items():
            print('INVALID Zotero Record {}:'.format(k))
            print('        {}'.format(zc.get_record(k)['Title']))
            for criterion, fields in v.items():
                print('        👾  {}: "{}"'.format(criterion.upper(), '", "'.join(fields)))


if __name__ == "__main__":
    main(
        **configure_commandline(
            OPTIONAL_ARGUMENTS, POSITIONAL_ARGUMENTS, DEFAULT_LOG_LEVEL))
