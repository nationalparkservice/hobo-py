Python package for working with HOBO temperature and RH data logger data.

At this time it supports HOBOware CSV exports from Onset models:
  * HOBO Pro v2 U23-001, U23-002
  * HOBO Pro H08-030-08, H08-032-08

It may or may not handle data from other HOBO loggers, though
HOBOware should produce a compatible CSV format for other similar hardware.
The data is assumed to have a timestamp field and a temperature field;
fields for relative humidity and battery supported when present.

Data exported from the discontinued BoxCar Pro software is not yet supported,
nor is highly customized HOBOware .CSV output.

License: As a work of the United States Government, this project is in the
public domain within the United States.

2016-02-24  David A. Riggs, Physical Science Tech, Lava Beds National Monument
