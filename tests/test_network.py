from unittest import TestCase
from hypothesis import given, settings
import hypothesis.strategies as st
import json
from collections import defaultdict
import rx
from rx import operators as ops
import os
import inspect
import requests

import icloudpd.network

class NetworkTest(TestCase):

    @given(size=st.integers(min_value=1, max_value=5))
    def test_get_file_stream(self, size):
        # TODO start local server instead

        class _Context(object):
            session = requests.Session()

        context = _Context()

        result = icloudpd.network.get_file_stream(
            context,
            "https://www.python.org/"
        ).pipe(
            ops.take(size),
            ops.to_iterable()
        ).run()
        self.assertEqual(len(result), size, "chunk count")
        self.assertEqual(sum(map(len, result)), 1024 * size, "downloaded size")
