#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check PECS references
"""

from airtight.cli import configure_commandline
from pleiades.refbot.zotero import ZoteroCollection
import logging
from os.path import abspath, realpath
from pleiades.refbot.place_crawler import PlaceCrawler
import sys

logger = logging.getLogger(__name__)

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
    ['zotero_csv', str, 'Path to Zotero CSV file to use'],
    ['places_json', str, 'Path to Pleiades place JSON to use']
]


def main(**kwargs):
    """
    main function
    """

    csv_path = abspath(realpath(kwargs['zotero_csv']))
    zc = ZoteroCollection()
    zc.load_csv(csv_path)
    logger.info('Zotero CSV loaded {} records'.format(len(zc)))

    json_path = abspath(realpath(kwargs['places_json']))
    pc = PlaceCrawler(json_path, count=False)
    place_refs = pc.get_references()
    logger.info(
        'PlaceCrawler found {} places with references'.format(len(place_refs)))

    pecs_places = []
    for pid, pdata in place_refs.items():
        for ref in pdata['references']:
            if (
                ref.shortTitle == 'PECS' or
                ref.shortTitle.startswith('PECS ') or
                ref.citationDetail.startswith('PECS ') or
                ref.fullCitation.startswith('PECS ')
            ):
                print('PECS!')





if __name__ == "__main__":
    main(
        **configure_commandline(
            OPTIONAL_ARGUMENTS, POSITIONAL_ARGUMENTS, DEFAULT_LOG_LEVEL))
