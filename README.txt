Python package for working with HOBO temperature and RH data logger data.

At this time it supports HOBOware and HOBOmobile CSV exports from Onset models:
  * HOBO Pro v2 U23-001, U23-002
  * HOBO Pro H08-030-08, H08-032-08
  * HOBO MX2301, MX2302

It may or may not handle data from other HOBO loggers, though
HOBOware should produce a compatible CSV format for other similar hardware.
The data is assumed to have a timestamp field and a temperature field;
fields for relative humidity and battery are supported when present.

Data exported from the discontinued BoxCar Pro software is not yet supported,
nor is highly customized HOBOware .CSV output.


Example usage:

	from hobo import HoboCSVReader

	with HoboCSVReader('my_hobo_data.csv') as reader:

		print('Reading %s ...' % reader.fname)
		print('Serial Number: %s  Title: %s' % (reader.sn, reader.title))

		for timestamp, temperature, rh, battery in reader:
			print('%s   %03.1f F   %02.1f %%   %.1f V' % (timestamp, temperature, rh, battery))

	>>> Reading my_hobo_data.cvs ...
	>>> Serial Number: 10173910  Title: My Hobo Data"
	>>> 2017-01-13 01:00:00-08:00   31.4 F   79.6 %   3.5 V
	>>> 2017-01-13 02:00:00-08:00   31.4 F   78.9 %   3.5 V
	>>> 2017-01-13 03:00:00-08:00   31.4 F   77.9 %   3.5 V
	>>> 2017-01-13 04:00:00-08:00   31.3 F   77.2 %   3.5 V


License: As a work of the United States Government, this project is in the
public domain within the United States.

2016-02-24  David A. Riggs, Physical Science Tech, Lava Beds National Monument
