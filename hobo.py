"""
Python package for working with HOBO data logger data.

Specifically, this has been tested with CSV exports from Onset HOBO U23-001
data loggers. It may or may not handle data from other HOBO loggers, though
HoboWare likely produces a compatible CSV format for other similar hardware.

License: As a work of the United States Government, this project is in the
public domain within the United States.

2016-02-24  David A. Riggs, Physical Science Tech, Lava Beds National Monument
"""

from __future__ import print_function

import sys
import re
import csv
from datetime import datetime, timedelta, tzinfo
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


__version__ = '0.0.1'

__all__ = 'HoboCSVReader',


TIME_FMTS = [
    '%m/%d/%y %I:%M:%S %p',  # Hoboware export
    '%m/%d/%Y %H:%M'         # Excel edit and save (*thanks* Microsoft)
]


TZ_REGEX = re.compile('GMT[-+]\d\d:\d\d')
SN_REGEX = re.compile('LGR S/N: (\d+)')


class TZFixedOffset(tzinfo):
    """
    A fixed-offset timezone implementation for HOBO format `GMT-07:00`.
    """

    def __init__(self, offset):
        if type(offset) in (int, float):
            self.offset_hrs = offset
        elif type(offset) == str:
            if len(offset) != 9 or offset[:3] != 'GMT' or offset[7:] != '00':
                raise ValueError(offset)
            self.offset_hrs = int(offset[3:6])
        else:
            raise ValueError(offset)
        self.offset = timedelta(hours=self.offset_hrs)
    
    def utcoffset(self, dt):
        return self.offset
    
    def dst(self, dt):
        return timedelta(0)
    
    def tzname(self, dt):
        return str(self)

    def __str__(self):
        return 'GMT%+03d:00' % self.offset_hrs

    def __repr__(self):
        return str(self)


def timestamp(s, tz=None):
    """Parse a HOBO timestamp value to Python DateTime"""
    for fmt in TIME_FMTS:
        try:
            dt = datetime.strptime(s, fmt)
            return dt.replace(tzinfo=tz) if tz else dt
        except ValueError as e:
            pass
    raise ValueError('time data "%s" does not match formats: %s' % (s, ', '.join(TIME_FMTS)))


class HoboCSVReader(object):
    """
    Iterator over a HOBO CSV file, produces (timestamp, temperature, RH,
    battery) rows.

    :param str fname: CSV filename
    :param tzinfo as_timezone: explicit timezone to cast timestamps to
    :param bool strict: whether we should be strict or lenient in parsing CSV

    :raises Exception: if this doesn't appear to be a HoboWare exported CSV

    :ivar str fname:
    :ivar str title:
    :ivar str sn:
    :ivar tzinfo tz:
    :ivar tzinfo as_timezone:
    """
    # TODO: extract timezone from title row
    
    def __init__(self, fname, as_timezone=None, strict=True):
        self.fname = fname
        self._f = open(fname, 'rt')

        self.title = next(self._f)   # line 1: plot title
        header = next(self._f)  # line 2: headers
        try:
            self.sn = SN_REGEX.findall(header)[0]
        except Exception as e:
            self.sn = ''
        self._find_columns(header)
        
        self.tz = TZFixedOffset(TZ_REGEX.search(header).group())
        self.as_timezone = TZFixedOffset(as_timezone) if type(as_timezone) in (int, float, str) else as_timezone
        
        if 'Temp' not in header:
            raise ValueError('File %s does not contain Temperature data.' % fname)

        self.reader = csv.reader(self._f, strict=strict)

    def _find_columns(self, header):
        """Return integer index for (timestamp, temp, RH, battery)"""
        self._itimestamp, self._itemp, self._irh, self._ibatt = None, None, None, None
        headers = next(csv.reader(StringIO(header)))
        for i, header in enumerate(headers):
            if 'Date Time' in header:
                self._itimestamp = i
            elif 'Temp,' in header or 'High Res. Temp.' in header:
                self._itemp = i
            elif 'RH, %' in header:
                self._irh = i
            elif 'Batt, V' in header:
                self._ibatt = i

    def __iter__(self):
        """
        Iterator for accessing the actual CSV rows.
        
        :return: yields (timestamp, temperature, RH, battery)
        :rtype: tuple(datetime, float, float, float)
        """
        for row in self.reader:
            if not row[self._itemp]:  # is this too lenient?
                continue  # skip event-only rows
            if not row[0].strip():
                continue  # skip blank rows
            ts = timestamp(row[self._itimestamp], self.tz)
            if self.as_timezone:
                ts = ts.astimezone(self.as_timezone)
            temp = float(row[self._itemp])
            rh = float(row[self._irh]) if self._irh is not None and row[self._irh] else None
            batt = float(row[self._ibatt]) if self._ibatt is not None else None
            yield ts, temp, rh, batt

    def unzip(self):
        """
        Rather than iterate row-by-row, return individual column lists
        (timestamps, temperatures, RHs, batts)

        :rtype: tuple of lists (timestamps, temperatures, RHs, batts)
        """
        return zip(*[row for row in self])


if __name__ == '__main__':
    for row in HoboCSVReader(sys.argv[1]):
        print(row)
