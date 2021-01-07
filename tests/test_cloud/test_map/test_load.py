from unittest import TestCase
from hypothesis import given, settings, HealthCheck
import hypothesis.strategies as st
import json
from collections import defaultdict
import os, math, datetime

import icloudpd.cloud.map as getters
import icloudpd.util

class ToPhotoSourceTest(TestCase):
    
    def test_to_photo_source_portrait(self):
        with open(os.path.normpath('tests/fixtures/pairs/portrait.json'),) as f:
            photo = json.load(f)
        pair = (photo["master_record"], photo["asset_record"])
        result = getters.to_photo_source(pair)
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
                (
                        'public.heic', 
                    1497485, 
                    'resOriginalRes-MockUrl'
                ),
                (None, None, None),
            ),
        )

    def test_to_photo_source_live_photo(self):
        with open(os.path.normpath('tests/fixtures/pairs/livephoto.json'),) as f:
            photo = json.load(f)
        pair = (photo["master_record"], photo["asset_record"])
        result = getters.to_photo_source(pair)
        # print(result)
        self.assertEqual(result,
            (
                'AdEGM+k3qUpNtCqmkkiooAFpZyxJ', 
                1604492664396, 
                'IMG_0512.HEIC', 
                (None, None, None),
                (
                    'public.heic',
                    1274777,
                    'resOriginalRes-MockURL'
                ),
                (
                    'com.apple.quicktime-movie',
                    4138524,
                    'resOriginalVidComplRes-MockURL'
                ),
            ),
        )

