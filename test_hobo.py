import os.path
import unittest

import hobo


class TestTimezones(unittest.TestCase):

	def test_tz(self):
		data = [
			('GMT-08:00',  -8, 'U23 and H08 PST'),
			('GMT+05:00',  +5, 'U23 and H08 Nepal'),
			('GMT +05:00', +5, 'MX2301 Nepal'),
			('GMT -08:00', -8, 'MX2301 PST')
		]
		for value, offset, desc in data:
			tz = hobo.TZFixedOffset(value)
			self.assertEqual(tz.offset_hrs, offset, desc)
		for _, offset, desc in data:
			tz = hobo.TZFixedOffset(offset)
			self.assertEqual(tz.offset_hrs, offset, desc)


class TestSampleData(unittest.TestCase):

	def test_u23_hoboware(self):
		fname = os.path.join('test_data', 'U23-001_HOBOware.csv')
		with hobo.HoboCSVReader(fname) as reader:
			self.assertEqual(reader.fname, fname)
			self.assertEqual(reader.sn, '10173910')
			#self.assertEqual(reader.title, 'Hobo U23-001 Sample Data')  # FIXME: remove BOM and "Plot Title:"
			self.assertEqual(reader.tz, hobo.TZFixedOffset(-8))

	def test_h08_hoboware(self):
		fname = os.path.join('test_data', 'H08-030-08_HOBOware.csv')
		with hobo.HoboCSVReader(fname) as reader:
			self.assertEqual(reader.fname, fname)
			self.assertEqual(reader.sn, '274341')
			#self.assertEqual(reader.title, 'Hobo H08-030-08 Sample Data')
			self.assertEqual(reader.tz, hobo.TZFixedOffset(-7))

	def test_mx2301(self):
		fname = os.path.join('test_data', 'MX2301_HOBOmobile.csv')
		with hobo.HoboCSVReader(fname) as reader:
			self.assertEqual(reader.fname, fname)
			self.assertEqual(reader.sn, '20293298')
			#self.assertEqual(reader.title, 'Hobo H08-030-08 Sample Data')
			self.assertEqual(reader.tz, hobo.TZFixedOffset(+5))


if __name__ == '__main__':
	unittest.main()
