from unittest import TestCase

import datetime

import icloudpd.core as core

class DateTimeTest(TestCase):

    def test_cleanse_datetime_min_year_month_day(self):
        dt = datetime.datetime.fromisoformat('0001-01-01 06:54:27+00:00')
        result = core.cleanse_datetime(dt)
        self.assertEqual(result, datetime.datetime.fromisoformat('1970-01-01 06:54:27+00:00'))

    def test_cleanse_datetime_missing_epoch_20(self):
        dt = datetime.datetime.fromisoformat('0085-02-03 06:54:27+00:00')
        result = core.cleanse_datetime(dt)
        self.assertEqual(result, datetime.datetime.fromisoformat('1985-02-03 06:54:27+00:00'))

    def test_cleanse_datetime_missing_epoch_21(self):
        dt = datetime.datetime.fromisoformat('0012-02-03 06:54:27+00:00')
        result = core.cleanse_datetime(dt)
        self.assertEqual(result, datetime.datetime.fromisoformat('2012-02-03 06:54:27+00:00'))

