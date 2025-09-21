# csvio.py  (c)2025  Henrique Moreira

""" csvio - CSV reader, tailored for linkpdb
"""

# pylint: disable=missing-function-docstring

import csv
from linkpdb.pgen import PGeneric


class CsvGeneric(PGeneric):
    """ Generic CSV Input. """
    my_sep = ","

    def __init__(self, path, name="C"):
        super().__init__(name=name)
        self._path = path

    def my_path(self) -> str:
        return self._path


class CsvInput(CsvGeneric):
    """ CSV Input. """
    def __init__(self, path, name="C"):
        super().__init__(path, name=name)
        self._cont, self._comment = self._reader(path)
        self._data = [
            line.split(CsvGeneric.my_sep)
            for _, line in self._cont
        ]

    def comment(self) -> list:
        assert isinstance(self._comment, list), "comment"
        return self._comment

    def _reader(self, path, enc="ascii"):
        with open(path, "r", encoding=enc) as fdin:
            lines = [
                (idx, aba.rstrip()) for idx, aba in enumerate(fdin.readlines(), 1)
                if aba.strip()
            ]
        head, tail = lines[0][1], lines[1:]
        assert head[0] == "#", f"Comment ({self.name}): {head}"
        comment = head[1:].strip().split(CsvGeneric.my_sep)
        return tail, comment

    def stringify(self, sep="\n"):
        astr = ""
        for line in self._data:
            s_line = ','.join(line)
            assert s_line.count(',') + 1 == len(line), f"Comma fields {s_line.count(',')} {len(line)}"
            astr += s_line + sep
        return astr

    def __repr__(self):
        """ Return comment as a string. """
        return str(self._comment)

    def __str__(self):
        """ Return stringified string. """
        return self.stringify()
