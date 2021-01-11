from unittest import TestCase
from hypothesis import given, settings
import hypothesis.strategies as st
from collections import defaultdict
import icloudpd.core as core
import icloudpd.core.cloud as cloud
import icloudpd.core.typing as ty

class CoreTest(TestCase):

    @given(t=st.text(), ts=st.datetimes())
    def test_folder_map_builder_valid(self, t, ts):
        mapper = core.folder_map_builder("{:%Y/%m/%d}")
        photo = (t, ts)
        result = mapper(photo)
        self.assertFalse('%' in result, "Contains template symbols")

    @given(photo=st.tuples(
        st.text(),
        st.datetimes(),
        st.just("main_file_name.heic"),
        st.tuples(
            st.just("public.heic"),
            st.integers(),
            st.text(),
        ),
        st.tuples(
            st.text(),
            st.integers(),
            st.text()
        ),
        )
    )
    def test_get_complimentary_filename_from_main_ext_valid(self, photo):
        result = cloud.get_complimentary_filename_from_main_ext(photo)
        self.assertEqual(result, "main_file_name_HEIC.heic")
