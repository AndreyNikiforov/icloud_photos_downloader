from unittest import TestCase
from hypothesis import given, settings, HealthCheck
import hypothesis.strategies as st
from collections import defaultdict
import os, math, datetime

import icloudpd.cloud.map as getters
import icloudpd.util

class GetterTest(TestCase):

    @given(s=st.text(min_size=1, max_size=5))
    def test_get_filename_missing(self, s):
        pair = (defaultdict(dict), defaultdict(dict))
        pair[0]["recordName"] = s
        result = getters._get_filename(pair)
        self.assertIsNone(result)

    @given(s=st.text(min_size=1, max_size=5))
    def test_get_id_valid(self, s):
        pair = (defaultdict(dict), defaultdict(dict))
        pair[0]["recordName"] = s
        result = getters._get_id(pair)
        self.assertEqual(result,s)

    def test_get_asset_timestamp_missing(self):
        pair = (defaultdict(dict), defaultdict(dict))
        result = getters._get_asset_timestamp(pair)
        self.assertIsNone(result)

    @given(s=st.integers())
    def test_get_asset_timestamp(self, s):
        pair = (defaultdict(dict), defaultdict(dict))
        pair[1]["fields"] = defaultdict(dict)
        pair[1]["fields"]["assetDate"] = defaultdict(dict)
        pair[1]["fields"]["assetDate"]["value"] = s
        result = getters._get_asset_timestamp(pair)
        self.assertEqual(result,s)

    @given(s=st.text(min_size=1))
    def test_get_id(self, s):
        pair = (defaultdict(dict), defaultdict(dict))
        pair[0]["recordName"] = s
        result = getters._get_id(pair)
        self.assertEqual(result,s)

    @given(t=st.text(), s=st.integers(), l=st.text())
    def test_get_url_adjustment(self, t, s, l):
        pair = (defaultdict(dict), defaultdict(dict))
        pair[1]["fields"] = defaultdict(dict)
        pair[1]["fields"]["resJPEGFullFileType"] = defaultdict(dict)
        pair[1]["fields"]["resJPEGFullRes"] = defaultdict(dict)
        pair[1]["fields"]["resJPEGFullRes"]["value"] = defaultdict(dict)
        pair[1]["fields"]["resJPEGFullFileType"]["value"] = t
        pair[1]["fields"]["resJPEGFullRes"]["value"]["size"] = s
        pair[1]["fields"]["resJPEGFullRes"]["value"]["downloadURL"] = l
        result = getters._get_url_adjustment(pair)
        self.assertEqual(result,(t,s,l))

    @given(tsl=st.tuples(st.none() | st.text(), st.none() | st.integers(), st.none() | st.text()).filter(lambda x: any(map(lambda m: m is None, x))))
    def test_get_url_adjustment_partial(self, tsl):
        print(tsl)
        t,s,l = tsl
        pair = (defaultdict(dict), defaultdict(dict))
        pair[1]["fields"] = defaultdict(dict)
        pair[1]["fields"]["resJPEGFullFileType"] = defaultdict(dict)
        pair[1]["fields"]["resJPEGFullRes"] = defaultdict(dict)
        pair[1]["fields"]["resJPEGFullRes"]["value"] = defaultdict(dict)
        if t is not None:
            pair[1]["fields"]["resJPEGFullFileType"]["value"] = t
        if s is not None:
            pair[1]["fields"]["resJPEGFullRes"]["value"]["size"] = s
        if l is not None:
            pair[1]["fields"]["resJPEGFullRes"]["value"]["downloadURL"] = l
        result = getters._get_url_adjustment(pair)
        self.assertEqual(result, (t,s,l))

    @given(t=st.text(), s=st.integers(), l=st.text())
    def test_get_url_original(self, t, s, l):
        pair = (defaultdict(dict), defaultdict(dict))
        pair[0]["fields"] = defaultdict(dict)
        pair[0]["fields"]["resOriginalFileType"] = defaultdict(dict)
        pair[0]["fields"]["resOriginalRes"] = defaultdict(dict)
        pair[0]["fields"]["resOriginalRes"]["value"] = defaultdict(dict)
        pair[0]["fields"]["resOriginalFileType"]["value"] = t
        pair[0]["fields"]["resOriginalRes"]["value"]["size"] = s
        pair[0]["fields"]["resOriginalRes"]["value"]["downloadURL"] = l
        result = getters._get_url_original(pair)
        self.assertEqual(result,(t,s,l))

    @given(tsl=st.tuples(st.none() | st.text(), st.none() | st.integers(), st.none() | st.text()).filter(lambda x: any(map(lambda m: m is None, x))))
    def test_get_url_original_partial(self, tsl):
        print(tsl)
        t, s, l = tsl
        pair = (defaultdict(dict), defaultdict(dict))
        pair[0]["fields"] = defaultdict(dict)
        pair[0]["fields"]["resOriginalFileType"] = defaultdict(dict)
        pair[0]["fields"]["resOriginalRes"] = defaultdict(dict)
        pair[0]["fields"]["resOriginalRes"]["value"] = defaultdict(dict)
        if t is not None:
            pair[0]["fields"]["resOriginalFileType"]["value"] = t
        if s is not None:
            pair[0]["fields"]["resOriginalRes"]["value"]["size"] = s
        if l is not None:
            pair[0]["fields"]["resOriginalRes"]["value"]["downloadURL"] = l
        result = getters._get_url_original(pair)
        self.assertEqual(result, (t,s,l))

    @given(t=st.text(), s=st.integers(), l=st.text())
    def test_get_url_complimentary(self, t, s, l):
        pair = (defaultdict(dict), defaultdict(dict))
        pair[0]["fields"] = defaultdict(dict)
        pair[0]["fields"]["resOriginalVidComplFileType"] = defaultdict(dict)
        pair[0]["fields"]["resOriginalVidComplRes"] = defaultdict(dict)
        pair[0]["fields"]["resOriginalVidComplRes"]["value"] = defaultdict(dict)
        pair[0]["fields"]["resOriginalVidComplFileType"]["value"] = t
        pair[0]["fields"]["resOriginalVidComplRes"]["value"]["size"] = s
        pair[0]["fields"]["resOriginalVidComplRes"]["value"]["downloadURL"] = l
        result = getters._get_url_complimentary(pair)
        self.assertEqual(result,(t,s,l))

    @given(tsl=st.tuples(st.none() | st.text(), st.none() | st.integers(), st.none() | st.text()).filter(lambda x: any(map(lambda m: m is None, x))))
    def test_get_url_complimentary_partial(self, tsl):
        print(tsl)
        t, s, l = tsl
        pair = (defaultdict(dict), defaultdict(dict))
        pair[0]["fields"] = defaultdict(dict)
        pair[0]["fields"]["resOriginalVidComplFileType"] = defaultdict(dict)
        pair[0]["fields"]["resOriginalVidComplRes"] = defaultdict(dict)
        pair[0]["fields"]["resOriginalVidComplRes"]["value"] = defaultdict(dict)
        if t is not None:
            pair[0]["fields"]["resOriginalVidComplFileType"]["value"] = t
        if s is not None:
            pair[0]["fields"]["resOriginalVidComplRes"]["value"]["size"] = s
        if l is not None:
            pair[0]["fields"]["resOriginalVidComplRes"]["value"]["downloadURL"] = l
        result = getters._get_url_complimentary(pair)
        self.assertEqual(result, (t,s,l))

    def test_all(self):
        triplet = (1,2,3)
        self.assertTrue(all(triplet))
        triplet = (1,None,3)
        self.assertFalse(all(triplet))

