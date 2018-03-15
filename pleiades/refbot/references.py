#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix references."""

import logging
from urllib.parse import urlparse
import validators

logger = logging.getLogger(__name__)

DEFAULT_BIBLIOGRAPHIC_URI_DOMAINS = ['zotero.org']


class ReferenceFixer:
    """This class kills crummy references and resurrects them in glory."""

    def __init__(self):
        pass


class PleiadesReference():
    """House and manipulate a single Pleiades reference."""

#    short_title = ''
#    citation_detail = ''
#    formatted_citation = ''
#    bibliographic_uri = ''
#    access_uri = ''
#    alternate_uri = ''
#    other_identifier = ''

    def __init__(self, **kwargs):
        self.history = {}
        try:
            domains = kwargs['bibliographic_uri_domains']
        except KeyError:
            self.bibliographic_uri_domains = DEFAULT_BIBLIOGRAPHIC_URI_DOMAINS
        else:
            self.bibliographic_uri_domains = domains
        for k, v in kwargs.items():
            if k in [
                'short_title',
                'citation_detail',
                'formatted_citation',
                'bibliographic_uri',
                'bibliographic_uri_domains',
                'access_uri',
                'alternate_uri',
                'other_identifier'
            ]:
                setattr(self, k, v)
            else:
                raise AttributeError(
                    'PleiadesReference does not support "{}" attributes'
                    ''.format(k))

    # short_title
    @property
    def short_title(self):
        return self.__short_title

    @short_title.setter
    def short_title(self, value):
        self._push_history('short_title', value)
        self.__short_title = value

    # citation_detail
    @property
    def citation_detail(self):
        return self.__citation_detail

    @citation_detail.setter
    def citation_detail(self, value):
        self._push_history('citation_detail', value)
        self.__citation_detail = value

    # full_citation
    @property
    def full_citation(self):
        return self.__full_citation

    @full_citation.setter
    def full_citation(self, value):
        self._push_history('full_citation', value)
        self.__full_citation = value

    # bibliographic_uri
    @property
    def bibliographic_uri(self):
        return self.__bibliographic_uri

    @bibliographic_uri.setter
    def bibliographic_uri(self, value):
        if validators.url(value):
            url_components = urlparse(value)
            if validators.domain(url_components.netloc):
                domains = [url_components.netloc]
                parts = domains[0].split('.')
                if parts[0] == 'www':
                    domains.append('.'.join(parts[1:]))
                invalid = True
                for domain in domains:
                    if domain in self.bibliographic_uri_domains:
                        invalid = False
                        break
                if invalid:
                    raise ValueError(
                        '"{}" from "{}" is not in the list of recognized '
                        'domains for bibliographic_uri ({})'
                        ''.format(
                            domains[0], value, self.bibliographic_uri_domains))
                else:
                    self._push_history('bibliographic_uri', value)
                    self.__bibliographic_uri = value
            else:
                raise ValueError(
                    '"{}" from "{}" is not a valid domain'
                    ''.format(url_components.netloc, value))
        else:
            raise ValueError('"{}" is not a valid URL'.format(value))

    # access_uri
    @property
    def access_uri(self):
        return self.__access_uri

    @access_uri.setter
    def access_uri(self, value):
        if validators.url(value):
            self._push_history('access_uri', value)
            self.__access_uri = value
        else:
            raise ValueError('"{}" is not a valid URL'.format(value))

    # alternate_uri
    @property
    def alternate_uri(self):
        return self.__alternate_uri

    @alternate_uri.setter
    def alternate_uri(self, value):
        if validators.url(value):
            self._push_history('alternate_uri', value)
            self.__alternate_uri = value
        else:
            raise ValueError('"{}" is not a valid URL'.format(value))

    # other_identifier
    @property
    def other_identifier(self):
        return self.__other_identifier

    @other_identifier.setter
    def other_identifier(self, value):
        self._push_history('other_identifier', value)
        self.__other_identifier = value

    # manage property history
    def get_history(self, field_name):
        try:
            h = self.history[field_name]
        except KeyError:
            return []
        else:
            return h

    def _push_history(self, field_name, value):
        try:
            h = self.history[field_name]
        except KeyError:
            self.history[field_name] = []
            h = self.history[field_name]
        finally:
            h.append(value)
        return len(self.history[field_name])
