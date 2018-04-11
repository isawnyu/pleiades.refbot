#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix UNESCO World Heritage list citations
"""

from airtight.cli import configure_commandline
import json
import logging
from os.path import abspath, realpath
from pleiades.refbot.fixers import WHLFixer
from pleiades.refbot.walker import PleiadesReferenceWalker

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
    ['places_json', str, 'where is the pleiades json']
]

logger = logging.getLogger(__name__)


def main(**kwargs):
    """
    main function
    """
    json_path = abspath(realpath(kwargs['places_json']))
    w = PleiadesReferenceWalker(json_path)
    logger.info('preparing to walk')
    count, result = w.walk()
    logger.info(
        'PlaceCrawler found {} places with references'.format(
            len(w.references)))

    logger.debug('preparing to filter')
    filtered_references = []
    for pid, pdata in w.references.items():
        for i, ref in enumerate(pdata['place_references']):
            hit = False
            for snippet in ['whc.unesco.org/en/list', 'BIIFWTIR']:
                for field in [
                    'access_uri', 'bibliographic_uri', 'alternate_uri'
                ]:
                    try:
                        val = getattr(ref, field)
                    except AttributeError:
                        pass
                    else:
                        if snippet in val:
                            hit = True
                            break
                if hit:
                    break
            if hit:
                filtered_references.append((pid, i))

    logger.info('filtered references: {}'.format(len(filtered_references)))

    fix_count = 0
    changed_references = {}
    for pid, ref_i in filtered_references:
        pr = w.references[pid]['place_references'][ref_i]
        fixer = WHLFixer(pr)
        changes, fixed = fixer.fix()
        if len(changes) > 0:
            fix_count += 1
            try:
                crefs = changed_references[pid]
            except KeyError:
                changed_references[pid] = {}
                crefs = changed_references[pid]
            finally:
                crefs[ref_i] = (fixed)

    logger.info(
        'fixed {} out of {} references on {} place resources'.format(
            fix_count, len(filtered_references), len(changed_references)))

    #print(jsonpickle.encode(changed_references))
    output = {}
    for pid, crefs in changed_references.items():
        orefs = {}
        for idx, cref in crefs.items():
            attributes = [
                a for a in dir(cref) if not a.startswith('_') and
                a not in [
                    'history', 'get_history', 'bibliographic_uri_domains',
                    'full_citation']]
            orefs[idx] = {}
            for a in attributes:
                if not isinstance(a, str):
                    raise RuntimeError('wah: {}'.format(a))
                try:
                    orefs[idx][a] = getattr(cref, a)
                except AttributeError:
                    orefs[idx][a] = ''
                finally:
                    if not isinstance(orefs[idx][a], str):
                        raise RuntimeError("Foo: {}".format(a))
        output[pid] = orefs
    print(json.dumps(output, indent=4, sort_keys=True, ensure_ascii=False))
    #print(jsonpickle.encode(output))

if __name__ == "__main__":
    main(
        **configure_commandline(
            OPTIONAL_ARGUMENTS, POSITIONAL_ARGUMENTS, DEFAULT_LOG_LEVEL))
