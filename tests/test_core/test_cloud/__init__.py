from unittest import TestCase
from hypothesis import given, settings
import hypothesis.strategies as st
from collections import defaultdict

import icloudpd.core as core

class DateTest(TestCase):

    def test_datetime_min_year_month_day(self):
        dt = datetime.datetime.fromisoformat('0001-01-01 06:54:27+00:00')
        ts = dt.timestamp()
        result = getters.datetime_cleansed(ts * 1000)
        self.assertEqual(result, datetime.datetime.fromisoformat('1970-01-01 06:54:27+00:00'))

    def test_datetime_missing_epoch_20(self):
        dt = datetime.datetime.fromisoformat('0085-02-03 06:54:27+00:00')
        ts = dt.timestamp()
        result = getters.datetime_cleansed(ts * 1000)
        self.assertEqual(result, datetime.datetime.fromisoformat('1985-02-03 06:54:27+00:00'))

    def test_datetime_missing_epoch_21(self):
        dt = datetime.datetime.fromisoformat('0012-02-03 06:54:27+00:00')
        ts = dt.timestamp()
        result = getters.datetime_cleansed(ts * 1000)
        self.assertEqual(result, datetime.datetime.fromisoformat('2012-02-03 06:54:27+00:00'))

