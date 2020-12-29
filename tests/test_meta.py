from unittest import TestCase
from hypothesis import given
import hypothesis.strategies as st
import json
from collections import defaultdict
import rx
from rx import operators as ops
import os

import icloudpd.meta

class MetaGetTest(TestCase):

    @given(s=st.text() | st.integers() | st.booleans() | st.floats())
    def test_get_valid_leaf(self, s):
        source = defaultdict(dict)
        source["level1"]["level2"] = s
        result = icloudpd.meta._get(source, "level1", "level2").pipe(ops.to_iterable()).run()
        self.assertEqual(result, [s])

    @given(s=st.text() | st.integers() | st.booleans() | st.floats())
    def test_get_long_path_returns_empty(self, s):
        source = defaultdict(dict)
        source["level1"]["level2"] = s
        result = icloudpd.meta._get(source, "level1", "level2", "level3").pipe(ops.to_iterable()).run()
        self.assertEqual(result,[])

    @given(s=st.text() | st.integers() | st.booleans() | st.floats())
    def test_get_short_path_returns_dict_node(self, s):
        source = defaultdict(dict)
        source["level1"] = defaultdict(dict)
        source["level1"]["sublevel11"] = defaultdict(dict)
        source["level1"]["sublevel11"]["sublevel12"] = defaultdict(dict)
        source["level1"]["sublevel11"]["sublevel12"]["level2"] = s
        result = icloudpd.meta._get(source, "level1", "sublevel11", "sublevel12").pipe(ops.to_iterable()).run()
        self.assertEqual(result,[{ "level2": s}])

class MetaTest(TestCase):

    def test_load_portrait(self):
        with open(os.path.normpath('tests/fixtures/pairs/portrait.json'),) as f:
            photo = json.load(f)
        pair = (photo["master_record"], photo["asset_record"])
        result = icloudpd.meta.load(rx.of(pair)).pipe(ops.to_iterable()).run()
        
        self.assertEqual(result,[
            [
                'AV6CozgukSZTJL0LL7vbdONrUxPC', 
                1608662569220, 
                'IMG_1930.HEIC', 
                [
                    'public.jpeg', 
                    2011193, 
                    'resJPEGFullRes-MockUrl'
                ],
            ],
        ])

    @given(s=st.text())
    def test_get_filename_missing(self, s):
        pair = (defaultdict(dict), defaultdict(dict))
        pair[0]["recordName"] = s
        result = icloudpd.meta._get_filename(pair).pipe(ops.to_iterable()).run()
        self.assertEqual(len(result),1)

    def test_get_asset_date_missing(self):
        pair = (defaultdict(dict), defaultdict(dict))
        result = icloudpd.meta._get_asset_date(pair).pipe(ops.to_iterable()).run()
        self.assertEqual(result,[0])

    @given(s=st.integers())
    def test_get_assetDate(self, s):
        pair = (defaultdict(dict), defaultdict(dict))
        pair[1]["fields"] = defaultdict(dict)
        pair[1]["fields"]["assetDate"] = defaultdict(dict)
        pair[1]["fields"]["assetDate"]["value"] = s
        result = icloudpd.meta._get_asset_date(pair).pipe(ops.to_iterable()).run()
        self.assertEqual(result,[s])

    @given(s=st.text())
    def test_get_id(self, s):
        pair = (defaultdict(dict), defaultdict(dict))
        pair[0]["recordName"] = s
        result = icloudpd.meta._get_id(pair).pipe(ops.to_iterable()).run()
        self.assertEqual(result,[s])

    @given(t=st.text(), s=st.integers(), l=st.text())
    def test_get_url(self, t, s, l):
        pair = (defaultdict(dict), defaultdict(dict))
        pair[1]["fields"] = defaultdict(dict)
        pair[1]["fields"]["resJPEGFullFileType"] = defaultdict(dict)
        pair[1]["fields"]["resJPEGFullRes"] = defaultdict(dict)
        pair[1]["fields"]["resJPEGFullRes"]["value"] = defaultdict(dict)
        pair[1]["fields"]["resJPEGFullFileType"]["value"] = t
        pair[1]["fields"]["resJPEGFullRes"]["value"]["size"] = s
        pair[1]["fields"]["resJPEGFullRes"]["value"]["downloadURL"] = l
        result = icloudpd.meta._get_url(pair).pipe(ops.to_iterable()).run()
        self.assertEqual(result,[[t,s,l]])

    def test_load_live_photo(self):
        with open(os.path.normpath('tests/fixtures/pairs/livephoto.json'),) as f:
            photo = json.load(f)
        pair = (photo["master_record"], photo["asset_record"])
        result = icloudpd.meta.load(rx.of(pair)).pipe(ops.to_iterable()).run()
        print(result)
        self.assertEqual(result,[
            [
                'AdEGM+k3qUpNtCqmkkiooAFpZyxJ', 
                1604492664396, 
                'IMG_0512.HEIC', 
                [
                    'public.heic', 
                    1274777, 
                    'resOriginalRes-MockURL'
                ],
                [
                    'com.apple.quicktime-movie',
                    4138524,
                    'resOriginalVidComplRes-MockURL'
                ]
            ],
        ])
