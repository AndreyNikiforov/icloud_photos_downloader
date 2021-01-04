from unittest import TestCase
from hypothesis import given, settings
import hypothesis.strategies as st
from collections import defaultdict
import datetime

import icloudpd.core.cloud

class ToPhotoTest(TestCase):

    @given(s=st.tuples(
        st.text(),
        st.integers(
            min_value=0, 
            max_value=datetime.datetime(9999, 12, 31).timestamp()
        ),
        st.text(),
        # st.tuples(
        #     st.none(), st.none(), st.none()
        # ),
        st.none(),
        st.tuples(
            st.text(), st.integers(), st.text()
        ),
        st.tuples(
            st.text(), st.integers(), st.text()
        ),
        )
    )
    def test_to_photo_live(self, s):
        s_i, s_ts, s_f, s_i0, s_i1, s_i2 = s
        result = icloudpd.core.cloud.to_photo(s)
        t_i, t_d, t_f, t_i0, t_i1 = result
        self.assertEqual(t_i, s_i)
        self.assertEqual(t_d.timestamp(), s_ts / 1000)
        self.assertEqual(t_f, s_f)
        self.assertEqual(t_i0, s_i1)
        self.assertEqual(t_i1, s_i2)
