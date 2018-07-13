#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fixers for Pleiades references"""

from pleiades.refbot.references import PleiadesReference
import logging
import sys

logger = logging.getLogger(__name__)


class Fixer:
    """Generic reference fixer."""

    def __init__(self, reference: PleiadesReference):
        self.raw = reference
        self.cooked = PleiadesReference()
        self.issues = []
        self.schema = {}

    def fix(self):
        logger.debug('RAW: {}'.format(self.raw))
        for field, directives in self.schema.items():
            logger.debug(
                'executing directives {} on field {}'.format(
                    repr(directives), field))

            # get current value of this field
            try:
                value = getattr(self.raw, field)
            except AttributeError:
                value = ''

            # directive: value exists or not
            if isinstance(directives, bool):
                if directives:
                    if value == '':
                        new_value = getattr(self, '_fix_{}'.format(field))()
                    else:
                        new_value = value
                    if new_value == '':
                        raise RuntimeError('{} cannot be empty'.format(field))
                    elif new_value != value:
                        setattr(self.cooked, field, new_value)
                        self.issues.append(field)
                    else:
                        setattr(self.cooked, field, new_value)
                else:
                    if value != '':
                        raise RuntimeError(
                            '{} must be empty, but it is "{}"'
                            ''.format(field, value))
                continue

            # other directives
            for d_key, d_value in directives.items():
                logger.debug(
                    'field="{}", d_key="{}", d_value="{}", value="{}"'
                    ''.format(field, d_key, d_value, value))
                if not getattr(self, '_test_{}'.format(d_key))(value, d_value):
                    fixed_value = getattr(
                        self, '_fix_{}'.format(field))(value, d_key, d_value)
                    if not getattr(
                            self,
                            '_test_{}'.format(d_key))(fixed_value, d_value):
                        raise RuntimeError('total failure')
                    self.issues.append(field)
                    setattr(self.cooked, field, fixed_value)
                else:
                    setattr(self.cooked, field, value)
            # # directive: exact match
            # try:
            #     match_value = directives['matches']
            # except KeyError:
            #     pass
            # else:
            #     if match_value != value:
            #         setattr(self.cooked, field, match_value)
            #         self.issues.append(field)
            #     else:
            #         setattr(self.cooked, field, value)
            # # directive: starts with
            # try:
            #     match_value = directives['starts_with']
            # except KeyError:
            #     pass
            # else:
            #     if value.startswith(match_value):
            #         setattr(self.cooked, field, value)
            #     else:
            #         try:
            #             value = getattr(self, '_fix_{}'.format(field))()
            #         except AttributeError:
            #             raise RuntimeError(
            #                 '{} must start with "{}", but instead is "{}"'
            #                 ''.format(field, match_value, value))
            #         else:
            #             setattr(self.cooked, field, value)
            #             self.issues.append(field)
        # copy over any fields for which there was no directive
        for a in [
            a for a in dir(self.raw) if not a.startswith('_') and
            a not in self.issues and
            a not in [
                    'history', 'get_history', 'bibliographic_uri_domains',
                    'full_citation']
        ]:
            try:
                raw_value = getattr(self.raw, a)
            except AttributeError:
                pass
            else:
                try:
                    getattr(self.cooked, a)
                except AttributeError:
                    setattr(self.cooked, a, raw_value)

        logger.debug('COOKED: {}'.format(self.cooked))
        logger.debug('Modified: {}'.format(repr(self.issues)))
        return (self.issues, self.cooked)

    def _test_matches(self, value, match_value):
        return value == match_value

    def _test_starts_with(self, value, start_value):
        return value.startswith(start_value)

    def _fix_access_uri(self, value, d_key, d_value):
        if d_key == 'matches':
            return d_value
        elif d_key == 'starts_with':
            return self._fix_uri_starts_with(value, d_value)
        else:
            raise NotImplementedError(d_key)

    def _fix_bibliographic_uri(self, value, d_key, d_value):
        if d_key == 'matches':
            return d_value
        elif d_key == 'starts_with':
            return self._fix_uri_starts_with(value, d_value)
        else:
            raise NotImplementedError(d_key)

    def _fix_citation_type(self, value, d_key, d_value):
        if d_key == 'matches':
            return d_value
        else:
            raise NotImplementedError(d_key)

    def _fix_short_title(self, value, d_key, d_value):
        if d_key == 'matches':
            return d_value
        else:
            raise NotImplementedError(d_key)

    def _fix_uri_starts_with(self, value, d_value):
        fixed_value = self._fix_uri_protocol(value, d_value)
        if self._test_starts_with(fixed_value, d_value):
            return fixed_value
        else:
            raise RuntimeError(
                'could not fix "{}" (starts_with: "{}")'
                ''.format(value, d_value))

    def _fix_uri_protocol(self, value, d_value):
        if value.startswith('http://') and d_value.startswith('https://'):
            return 'https://{}'.format(value.split('//')[1])
        else:
            return value


class WHLFixer(Fixer):
    """Fix UNESCO World Heritage Site references."""

    def __init__(self, reference: PleiadesReference):
        super().__init__(reference=reference)
        self.schema = {
            'short_title': {'matches': 'WHL'},
            'citation_detail': True,
            'bibliographic_uri': {
                'matches': 'https://www.zotero.org/groups/2533/items/BIIFWTIR'
            },
            'access_uri': {
                'starts_with': 'https://whc.unesco.org/en/list/'
            },
            'formatted_citation': {
                'starts_with': 'UNESCO World Heritage Centre, World Heritage '
                               'List, 1978. See: "'
            },
            'citation_type': {'matches': 'seeFurther'}
        }

    def _fix_formatted_citation(self, value, d_key, d_value):
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

