from unittest import TestCase
from hypothesis import given, settings, HealthCheck
import hypothesis.strategies as st

import icloudpd.util

class UtilTest(TestCase):

    @given(s=st.integers(min_value=0, max_value=5))
    def test_buffer_with_count_odd(self, s):
        size = 1 + s * 2
        source= [size]*size
        result = list(icloudpd.util.buffer_with_count(2, source))
        self.assertEqual(len(result), s + 1, "pairs")


    @given(s=st.integers(min_value=0, max_value=5))
    def test_buffer_with_count_even(self, s):
        size = s * 2
        source= [size]*size
        result = list(icloudpd.util.buffer_with_count(2, source))
        self.assertEqual(len(result), s, "pairs")

    @given(s=st.text(min_size=1, max_size=2).filter(lambda p: not icloudpd.util.is_pathname_valid(p)))
    @settings(suppress_health_check=(HealthCheck.filter_too_much,HealthCheck.too_slow))
    def test_make_valid_filename_symbols(self, s):
        result = icloudpd.util.make_valid_filename(s)
        print(f"before={s}, after={result}")
        self.assertTrue(icloudpd.util.is_pathname_valid(result))

    def test_make_valid_filename_long(self):
        s = ''.join(['a']*300)
        self.assertFalse(icloudpd.util.is_pathname_valid(s))
        result = icloudpd.util.make_valid_filename(s)
        self.assertTrue(icloudpd.util.is_pathname_valid(result))
