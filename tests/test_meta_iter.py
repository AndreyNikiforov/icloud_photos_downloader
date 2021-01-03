from unittest import TestCase
from hypothesis import given
import hypothesis.strategies as st
import json
from collections import defaultdict
import rx
from rx import operators as ops
import os

import icloudpd.meta_iter

class MetaGetTest_Iter(TestCase):

    @given(s=st.text() | st.integers() | st.booleans() | st.floats())
    def test_get_valid_leaf(self, s):
        source = defaultdict(dict)
        source["level1"]["level2"] = s
        result = list(icloudpd.meta_iter._get(source, ["level1", "level2"]))
        self.assertEqual(result, [s])

    @given(s=st.text() | st.integers() | st.booleans() | st.floats())
    def test_get_long_path_returns_empty(self, s):
        source = defaultdict(dict)
        source["level1"] = defaultdict(dict)
        source["level1"]["sublevel11"] = defaultdict(dict)
        source["level1"]["sublevel11"]["sublevel12"] = defaultdict(dict)
        source["level1"]["sublevel11"]["sublevel12"]["level2"] = s
        result = list(icloudpd.meta_iter._get(source, ["level1", "level2", "level3"]))
        self.assertEqual(result,[])

    @given(s=st.text() | st.integers() | st.booleans() | st.floats())
    def test_get_short_path_returns_dict_node(self, s):
        source = defaultdict(dict)
        source["level1"] = defaultdict(dict)
        source["level1"]["sublevel11"] = defaultdict(dict)
        source["level1"]["sublevel11"]["sublevel12"] = defaultdict(dict)
        source["level1"]["sublevel11"]["sublevel12"]["level2"] = s
        result = list(icloudpd.meta_iter._get(source, ["level1", "sublevel11", "sublevel12"]))
        self.assertEqual(result,[{ "level2": s}])

class MetaTest_Iter(TestCase):

    def test_load_portrait_iter(self):
        with open(os.path.normpath('tests/fixtures/pairs/portrait.json'),) as f:
            photo = json.load(f)
        pair = (photo["master_record"], photo["asset_record"])
        result = list(icloudpd.meta_iter.load(pair))
        
        self.assertEqual(result,[
            (
                'AV6CozgukSZTJL0LL7vbdONrUxPC', 
                1608662569220, 
                'IMG_1930.HEIC', 
                (
                    'public.jpeg', 
                    2011193, 
                    'resJPEGFullRes-MockUrl'
                ),
            ),
        ])

    @given(s=st.text(min_size=1, max_size=5))
    def test_get_filename_missing_iter(self, s):
        pair = (defaultdict(dict), defaultdict(dict))
        pair[0]["recordName"] = s
        result = list(icloudpd.meta_iter._get_filename(pair))
        self.assertEqual(result,[])

    @given(s=st.text(min_size=1, max_size=5))
    def test_get_fallback_filename_iter(self, s):
        pair = (defaultdict(dict), defaultdict(dict))
        pair[0]["recordName"] = s
        result = list(icloudpd.meta_iter._get_fallback_filename(pair))
        self.assertEqual(len(result),1)

    @given(s=st.text(min_size=1, max_size=5))
    def test_get_id_valid_iter(self, s):
        pair = (defaultdict(dict), defaultdict(dict))
        pair[0]["recordName"] = s
        result = list(icloudpd.meta_iter._get_id(pair))
        self.assertEqual(result,[s])

    def test_get_asset_timestamp_missing_iter(self):
        pair = (defaultdict(dict), defaultdict(dict))
        result = list(icloudpd.meta_iter._get_asset_timestamp(pair))
        self.assertEqual(result,[])

    @given(s=st.integers())
    def test_get_asset_timestamp_iter(self, s):
        pair = (defaultdict(dict), defaultdict(dict))
        pair[1]["fields"] = defaultdict(dict)
        pair[1]["fields"]["assetDate"] = defaultdict(dict)
        pair[1]["fields"]["assetDate"]["value"] = s
        result = list(icloudpd.meta_iter._get_asset_timestamp(pair))
        self.assertEqual(result,[s])

    @given(s=st.text(min_size=1))
    def test_get_id_iter(self, s):
        pair = (defaultdict(dict), defaultdict(dict))
        pair[0]["recordName"] = s
        result = list(icloudpd.meta_iter._get_id(pair))
        self.assertEqual(result,[s])

    @given(t=st.text(), s=st.integers(), l=st.text())
    def test_get_url_adjustment_iter(self, t, s, l):
        pair = (defaultdict(dict), defaultdict(dict))
        pair[1]["fields"] = defaultdict(dict)
        pair[1]["fields"]["resJPEGFullFileType"] = defaultdict(dict)
        pair[1]["fields"]["resJPEGFullRes"] = defaultdict(dict)
        pair[1]["fields"]["resJPEGFullRes"]["value"] = defaultdict(dict)
        pair[1]["fields"]["resJPEGFullFileType"]["value"] = t
        pair[1]["fields"]["resJPEGFullRes"]["value"]["size"] = s
        pair[1]["fields"]["resJPEGFullRes"]["value"]["downloadURL"] = l
        result = list(icloudpd.meta_iter._get_url_adjustment(pair))
        self.assertEqual(result,[(t,s,l)])

    @given(t=st.text(), s=st.integers(), l=st.text())
    def test_get_url_original_iter(self, t, s, l):
        pair = (defaultdict(dict), defaultdict(dict))
        pair[0]["fields"] = defaultdict(dict)
        pair[0]["fields"]["resOriginalFileType"] = defaultdict(dict)
        pair[0]["fields"]["resOriginalRes"] = defaultdict(dict)
        pair[0]["fields"]["resOriginalRes"]["value"] = defaultdict(dict)
        pair[0]["fields"]["resOriginalFileType"]["value"] = t
        pair[0]["fields"]["resOriginalRes"]["value"]["size"] = s
        pair[0]["fields"]["resOriginalRes"]["value"]["downloadURL"] = l
        result = list(icloudpd.meta_iter._get_url_original(pair))
        self.assertEqual(result,[(t,s,l)])

    @given(t=st.text(), s=st.integers(), l=st.text())
    def test_get_url_complimentary_iter(self, t, s, l):
        pair = (defaultdict(dict), defaultdict(dict))
        pair[0]["fields"] = defaultdict(dict)
        pair[0]["fields"]["resOriginalVidComplFileType"] = defaultdict(dict)
        pair[0]["fields"]["resOriginalVidComplRes"] = defaultdict(dict)
        pair[0]["fields"]["resOriginalVidComplRes"]["value"] = defaultdict(dict)
        pair[0]["fields"]["resOriginalVidComplFileType"]["value"] = t
        pair[0]["fields"]["resOriginalVidComplRes"]["value"]["size"] = s
        pair[0]["fields"]["resOriginalVidComplRes"]["value"]["downloadURL"] = l
        result = list(icloudpd.meta_iter._get_url_complimentary(pair))
        self.assertEqual(result,[(t,s,l)])


    def test_load_live_photo_iter(self):
        with open(os.path.normpath('tests/fixtures/pairs/livephoto.json'),) as f:
            photo = json.load(f)
        pair = (photo["master_record"], photo["asset_record"])
        result = list(icloudpd.meta_iter.load(pair))
        print(result)
        self.assertEqual(result,[
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
        ])
