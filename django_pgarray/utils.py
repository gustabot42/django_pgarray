# -*- coding: utf-8 -*-

from StringIO import StringIO
import unicodecsv as csv


class pgarray_dialect(csv.csv.excel):
    skipinitialspace = True
    lineterminator = ''


def parselist(value):
    f = StringIO()
    w = csv.writer(f, pgarray_dialect)
    w.writerow(value)
    f.seek(0)
    return f.read()

def parsestring(value):
    f = StringIO(value)
    return csv.reader(f, pgarray_dialect).next()