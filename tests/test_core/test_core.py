from unittest import TestCase
from hypothesis import given, settings
import hypothesis.strategies as st
from collections import defaultdict
import icloudpd.core as core

class CoreTest(TestCase):

    @given(t=st.text(), ts=st.datetimes())
    def test_folder_mapper_valid(self, t, ts):
        mapper = core.folder_mapper("{:%Y/%m/%d}")
        photo = (t, ts)
        result = mapper(photo)
        self.assertFalse('%' in result, "Contains template symbols")

