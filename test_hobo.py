import os.path
import unittest

import hobo


class TestHobo(unittest.TestCase):

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


if __name__ == '__main__':
	unittest.main()
