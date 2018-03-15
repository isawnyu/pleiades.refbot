#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix references."""

import logging
logger = logging.getLogger(__name__)


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
        for k, v in kwargs.items():
            setattr(self, k, v)

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

