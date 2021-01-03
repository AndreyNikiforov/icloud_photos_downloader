from unittest import TestCase
from hypothesis import given, settings
import hypothesis.strategies as st
from collections import defaultdict

import icloudpd.domain

class DomainTest(TestCase):

    @given(t=st.text(), ts=st.datetimes())
    def test_folder_mapper_valid(self, t, ts):
        mapper = icloudpd.domain.folder_mapper("{:%Y/%m/%d}")
        photo = (t, ts.timestamp())
        result = mapper(photo)
        self.assertFalse('%' in result, "Contains template symbols")



