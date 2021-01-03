from unittest import TestCase
from hypothesis import given, settings, HealthCheck
import hypothesis.strategies as st
import json
from collections import defaultdict
import os, math

import icloudpd.meta
import icloudpd.util

class MetaGetTest(TestCase):

    @given(s=st.text() | st.integers() | st.booleans() | st.floats(allow_nan=False) | st.decimals(allow_nan=False))
    def test_get_valid_leaf(self, s):
        source = defaultdict(dict)
        source["level1"]["level2"] = s
        result = icloudpd.meta._get(source, ["level1", "level2"])
        self.assertEqual(result, s)

    @given(s=st.text() | st.integers() | st.booleans() | st.floats())
    def test_get_long_path_returns_empty(self, s):
        source = defaultdict(dict)
        source["level1"] = defaultdict(dict)
        source["level1"]["sublevel11"] = defaultdict(dict)
        source["level1"]["sublevel11"]["sublevel12"] = defaultdict(dict)
        source["level1"]["sublevel11"]["sublevel12"]["level2"] = s
        result = icloudpd.meta._get(source, ["level1", "level2", "level3"])
        self.assertIsNone(result)

    @given(s=st.text() | st.integers() | st.booleans() | st.floats())
    def test_get_short_path_returns_dict_node(self, s):
        source = defaultdict(dict)
        source["level1"] = defaultdict(dict)
        source["level1"]["sublevel11"] = defaultdict(dict)
        source["level1"]["sublevel11"]["sublevel12"] = defaultdict(dict)
        source["level1"]["sublevel11"]["sublevel12"]["level2"] = s
        result = icloudpd.meta._get(source, ["level1", "sublevel11", "sublevel12"])
        self.assertEqual(result,{ "level2": s})

class MetaTest(TestCase):

    def test_load_portrait(self):
        with open(os.path.normpath('tests/fixtures/pairs/portrait.json'),) as f:
            photo = json.load(f)
        pair = (photo["master_record"], photo["asset_record"])
        result = icloudpd.meta.load(pair)
        # print(result)
        self.assertEqual(result,
            (
                'AV6CozgukSZTJL0LL7vbdONrUxPC', 
                1608662569220, 
                'IMG_1930.HEIC', 
                (
                    'public.jpeg', 
                    2011193, 
                    'resJPEGFullRes-MockUrl'
                ),
                None,
            ),
        )

    @given(s=st.text(min_size=1, max_size=5))
    def test_get_filename_missing(self, s):
        pair = (defaultdict(dict), defaultdict(dict))
        pair[0]["recordName"] = s
        result = icloudpd.meta._get_filename(pair)
        self.assertIsNone(result)

    @given(s=st.text(min_size=1, max_size=5))
    def test_get_id_valid(self, s):
        pair = (defaultdict(dict), defaultdict(dict))
        pair[0]["recordName"] = s
        result = icloudpd.meta._get_id(pair)
        self.assertEqual(result,s)

    def test_get_asset_timestamp_missing(self):
        pair = (defaultdict(dict), defaultdict(dict))
        result = icloudpd.meta._get_asset_timestamp(pair)
        self.assertIsNone(result)

    @given(s=st.integers())
    def test_get_asset_timestamp(self, s):
        pair = (defaultdict(dict), defaultdict(dict))
        pair[1]["fields"] = defaultdict(dict)
        pair[1]["fields"]["assetDate"] = defaultdict(dict)
        pair[1]["fields"]["assetDate"]["value"] = s
        result = icloudpd.meta._get_asset_timestamp(pair)
        self.assertEqual(result,s)

    @given(s=st.text(min_size=1))
    def test_get_id(self, s):
        pair = (defaultdict(dict), defaultdict(dict))
        pair[0]["recordName"] = s
        result = icloudpd.meta._get_id(pair)
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
        result = icloudpd.meta._get_url_adjustment(pair)
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
        result = icloudpd.meta._get_url_adjustment(pair)
        self.assertIsNone(result)

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
        result = icloudpd.meta._get_url_original(pair)
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
        result = icloudpd.meta._get_url_original(pair)
        self.assertIsNone(result)

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
        result = icloudpd.meta._get_url_complimentary(pair)
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
        result = icloudpd.meta._get_url_complimentary(pair)
        self.assertIsNone(result)

    def test_load_live_photo(self):
        with open(os.path.normpath('tests/fixtures/pairs/livephoto.json'),) as f:
            photo = json.load(f)
        pair = (photo["master_record"], photo["asset_record"])
        result = icloudpd.meta.load(pair)
        # print(result)
        self.assertEqual(result,
            (
                'AdEGM+k3qUpNtCqmkkiooAFpZyxJ', 
                1604492664396, 
                'IMG_0512.HEIC', 
                (
                    'public.heic', 
                    1274777, 
                    'resOriginalRes-MockURL'
                ),
                (
                    'com.apple.quicktime-movie',
                    4138524,
                    'resOriginalVidComplRes-MockURL'
                )
            ),
        )
