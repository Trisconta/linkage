# pgen.py  (c)2025  Henrique Moreira

""" pgen - Generic class for objects.
"""

# pylint: disable=missing-function-docstring


class PGeneric:
    """ Generic class, basically name and the content. """
    def __init__(self, data=None, name="P"):
        self.name = name
        self._data = [] if data is None else data

    def content(self) -> list:
        """ The content must be always be a list. """
        assert isinstance(self._data, list)
        return self._data
