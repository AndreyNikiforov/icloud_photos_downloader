from unittest import TestCase
from hypothesis import given, settings, HealthCheck
import hypothesis.strategies as st

import icloudpd.core as core
import icloudpd.util.path

class PathTest(TestCase):

    @given(s=st.text(min_size=1, max_size=2).filter(lambda p: not icloudpd.util.path.is_pathname_valid(p)))
    @settings(suppress_health_check=(HealthCheck.filter_too_much,HealthCheck.too_slow))
    def test_make_valid_filename_symbols(self, s):
        result = core.make_valid_filename(s)
        print(f"before={s}, after={result}")
        self.assertTrue(icloudpd.util.path.is_pathname_valid(result))

    def test_make_valid_filename_long(self):
        s = ''.join(['a']*300)
        self.assertFalse(icloudpd.util.path.is_pathname_valid(s))
        result = core.make_valid_filename(s)
        self.assertTrue(icloudpd.util.path.is_pathname_valid(result))
