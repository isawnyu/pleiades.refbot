#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fixers for Pleiades references"""

import logging
from pleiades.refbot.references import PleiadesReference


class Fixer:
    """Generic reference fixer."""

    def __init__(self, reference: PleiadesReference):
        self.raw = reference
        self.cooked = PleiadesReference()
        self.issues = []
        self.schema = {}

    def fix(self):
        print("RAW")
        print(self.raw)
        for field, directives in self.schema.items():
            print('field: {}'.format(field))
            # directive: value exists or not
            if isinstance(directives, bool):
                if directives:
                    # must exist
                    try:
                        value = getattr(self.raw, field)
                    except AttributeError:
                        try:
                            value = getattr(self, '_fix_{}'.format(field))()
                        except AttributeError:
                            raise ValueError(
                                '{} cannot be empty'.format(field))
                        else:
                            setattr(self.cooked, field, value)
                            self.issues.append(field)
                    else:
                        setattr(self.cooked, field, value)
                else:
                    try:
                        value = getattr(self.raw, field)
                    except AttributeError:
                        pass
                    else:
                        raise ValueError(
                            '{} must be empty, but it is "{}"'
                            ''.format(field, value))
                continue
            try:
                value = getattr(self.raw, field)
            except AttributeError:
                value = ''
            # directive: exact match
            try:
                match_value = directives['matches']
            except KeyError:
                pass
            else:
                if match_value != value:
                    setattr(self.cooked, field, match_value)
                    self.issues.append(field)
                else:
                    setattr(self.cooked, field, value)
            # directive: starts with
            try:
                match_value = directives['starts_with']
            except KeyError:
                pass
            else:
                if value.startswith(match_value):
                    setattr(self.cooked, field, value)
                else:
                    try:
                        value = getattr(self, '_fix_{}'.format(field))()
                    except AttributeError:
                        raise ValueError(
                            '{} must start with "{}", but instead is "{}"'
                            ''.format(field))
                    else:
                        setattr(self.cooked, field, value)
                        self.issues.append(field)
        print("COOKED")
        print(self.cooked)
        print('Modified: {}'.format(repr(self.issues)))


class WHLFixer(Fixer):
    """Fix UNESCO World Heritage Site references."""

    def __init__(self, reference: PleiadesReference):
        super().__init__(reference=reference)
        self.schema = {
            'short_title': {'matches': 'WHL'},
            'citation_detail': True,
            'bibliographic_uri': {
                'matches': 'https://www.zotero.org/groups/2533/items/BIIFWTIR',
                'alternate_matches': [
                    'https://www.zotero.org/groups/2533/pleiades/items/'
                    'itemKey/BIIFWTIR']
            },
            'access_uri': {
                'starts_with': 'http://whc.unesco.org/en/list/'
            },
            'formatted_citation': {
                'starts_with': 'UNESCO World Heritage Centre, World Heritage '
                               'List, 1978. See: "'
            },
            'citation_type': {'matches': 'seeFurther'}
        }

    def _fix_formatted_citation(self):
        """Try to fix formatted citation."""

        tpl = (
            'UNESCO World Heritage Centre, World Heritage List, 1978. See: '
            '"{}."')
        try:
            detail = self.cooked.citation_detail
        except AttributeError:
            pass
        else:
            if detail != '':
                return tpl.format(detail)
        raise RuntimeError('could not fix formatted citation')

    def _fix_citation_detail(self):
        """Try to fix citation detail."""

        detail = ''

        # maybe the formatted citation includes the citation detail
        try:
            value = self.raw.formatted_citation
        except AttributeError:
            pass
        else:
            if value.startswith('UNESCO World Heritage List, '):
                detail = ','.join(value.split(',')[1:])
            elif value.startswith('UNESCO World Heritage List: '):
                detail = ':'.join(value.split(':')[1:])
            detail = detail.strip()
            if detail != '':
                return detail

        # maybe the short title includes the citation detail
        try:
            value = self.raw.short_title
        except AttributeError:
            pass
        else:
            if value.startswith('UNESCO World Heritage List, '):
                detail = ','.join(value.split(',')[1:])
            elif value.startswith('UWHL: '):
                detail = ':'.join(value.split(':')[1:])
            elif value.startswith('UNESCO World Heritage Centre, '):
                detail = ','.join(value.split(',')[1:])
            detail = detail.strip()
            if detail != '':
                return detail

        # maybe the formatted citation *is* the citation detail
        try:
            value = self.raw.formatted_citation
        except AttributeError:
            pass
        else:
            canary = False
            for stop in [',', ':', 'UNESCO', 'WHL']:
                if stop in value:
                    canary = True
                    break
            if not canary:
                detail = value.strip()
                if detail != '':
                    return detail

        # maybe the short title *is* the citation detail
        try:
            value = self.raw.short_title
        except AttributeError:
            pass
        else:
            canary = False
            for stop in [',', ':', 'UNESCO', 'WHL']:
                if stop in value:
                    canary = True
                    break
            if not canary:
                detail = value.strip()
                if detail != '':
                    return detail

        raise ValueError('cannot fix citation detail')


