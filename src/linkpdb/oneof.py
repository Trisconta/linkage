# oneof.py  (c)2025  Henrique Moreira

""" oneof - reader for all 'linkage' files.
"""

# pylint: disable=missing-function-docstring

import os
import linkpdb.pgen
from linkpdb.csvio import CsvInput


def test_main():
    """ Remove me, please! """
    path = "/home/henrique/anaceo/Trisconta/wsound/gather/external/jad-links"
    new = PAll(path)
    print("PAll():")
    for one in new.briefs():
        print(one, end="\n\n")
    for dom in new.domain_listed():
        print(f"{dom.name} -->\n{dom}<---")
    xlink = new.meta()[0][0]
    for dom in xlink:
        print(f"{dom}: {xlink[dom]}", end="\n\n")
    return True


class PAll(linkpdb.pgen.PGeneric):
    """ Gathers all infos.
    """
    def __init__(self, pname="/", name="P"):
        super().__init__(name=name)
        self._pdir = os.path.realpath(pname) if pname else ""
        self._domains, self._ids = [], []
        self._raw_flist = []
        self._objs, self._d_data = {}, {}
        self._xlink = {}
        if pname:
            self._scan_all(self._pdir)
        self._tidy()

    def meta(self):
        infos = (
            self._xlink,
            self._objs,
        )
        return infos

    def briefs(self):
        res = []
        for key in sorted(self._objs):
            item = self._objs[key]
            res.append(
                (key, item, len(item.content())),
            )
        return res

    def get_domains(self):
        assert self._domains, "No domains"
        return self._domains

    def data_domain(self):
        return self._d_data

    def domain_listed(self):
        lst = sorted(
            self._d_data,
            key=lambda k: int(k[1:]), # ignores leading 'd'
        )
        res = [
            self._d_data[dom]
            for dom in lst
        ]
        return res

    def _tidy(self):
        """ Gathers all data newly (or the first time). """
        if not self._raw_flist:
            return False
        dom, rest = self._raw_flist[0], self._raw_flist[1:]
        last = rest[-1]
        strict = (dom[0], last[0])
        assert strict == ("domains", "linka"), f"Bad PDB: {strict}"
        self._objs = {
            "domain": CsvInput(dom[2].path, name="domain"),
            "linka": CsvInput(last[2].path, name="linka"),
        }
        for tup in rest[:-1]:
            key = tup[0]
            d_num = key.split("-")[-1]
            mycsv = CsvInput(tup[2].path, name=d_num)
            self._objs[key] = mycsv
            self._d_data[d_num] = mycsv  # 'd_num'='d1', ...
        self._xlink = self._grab_xlinks(self._objs, self._d_data)
        return True

    def _grab_xlinks(self, objs, d_data):
        link = objs["linka"]
        dct, d_all = {}, {}
        uuid2dyid = {}	# Google UUID of a photo into d1:n
        for key in d_data:
            dct[key] = {}
        for trip in link.content():
            d_num, y_id, uuid = trip
            key = f"d{d_num}"
            assert y_id not in dct[key], f"Duplicate y_id: {y_id}"
            dct[key][y_id] = uuid
            d_and_yid = key + ":" + y_id
            if d_and_yid in d_all:
                d_all[d_and_yid].append(uuid)
            else:
                d_all[d_and_yid] = [uuid]
            assert uuid not in uuid2dyid, f"Duplicate uuid: {d_and_yid}"
            uuid2dyid[uuid] = d_and_yid
        return [
            dct,
            d_all,
            uuid2dyid[uuid],
        ]

    def _scan_all(self, pdir:str):
        lst = sorted(
            [
                (normalized(aba.name), aba.name, aba) for aba in os.scandir(pdir)
                if aba.name.endswith(".csv") and aba.name.lower()[0] in "dl"
            ],
            key=lambda k: k[0],
        )
        self._raw_flist = lst
        return lst


def normalized(astr:str) -> str:
    """ Returns a normalized string from relative path. """
    res, _ = os.path.splitext(astr.lower())
    return res


if __name__ == "__main__":
    test_main()
