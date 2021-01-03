from unittest import TestCase
from hypothesis import given
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
