# -*- coding: utf-8 -*-

from StringIO import StringIO
import unicodecsv as csv


class pgarray_dialect(csv.csv.excel):
    skipinitialspace = True


def list_to_csv(value):
    f = StringIO()
    w = csv.writer(f, pgarray_dialect)
    w.writerow(value)
    f.seek(0)
    return f.read()

def csv_to_list(value):
    value = value.encode('utf-8')
    f = StringIO(value)
    r = csv.reader(f, pgarray_dialect)
    values = []
    for i in r:
        values += i
    
    return values if value else None