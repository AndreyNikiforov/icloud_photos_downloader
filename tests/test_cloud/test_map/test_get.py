from unittest import TestCase
from hypothesis import given, settings, HealthCheck
import hypothesis.strategies as st
from collections import defaultdict
import os, math, datetime

import icloudpd.cloud.map as getters
import icloudpd.util

class GetTest(TestCase):

    @given(s=st.text() | st.integers() | st.booleans() | st.floats(allow_nan=False) | st.decimals(allow_nan=False))
    def test_get_valid_leaf(self, s):
        source = defaultdict(dict)
        source["level1"]["level2"] = s
        result = getters._get(source, ["level1", "level2"])
        self.assertEqual(result, s)

    @given(s=st.text() | st.integers() | st.booleans() | st.floats())
    def test_get_long_path_returns_empty(self, s):
        source = defaultdict(dict)
        source["level1"] = defaultdict(dict)
        source["level1"]["sublevel11"] = defaultdict(dict)
        source["level1"]["sublevel11"]["sublevel12"] = defaultdict(dict)
        source["level1"]["sublevel11"]["sublevel12"]["level2"] = s
        result = getters._get(source, ["level1", "level2", "level3"])
        self.assertIsNone(result)

    @given(s=st.text() | st.integers() | st.booleans() | st.floats())
    def test_get_short_path_returns_dict_node(self, s):
        source = defaultdict(dict)
        source["level1"] = defaultdict(dict)
        source["level1"]["sublevel11"] = defaultdict(dict)
        source["level1"]["sublevel11"]["sublevel12"] = defaultdict(dict)
        source["level1"]["sublevel11"]["sublevel12"]["level2"] = s
        result = getters._get(source, ["level1", "sublevel11", "sublevel12"])
        self.assertEqual(result,{ "level2": s})
