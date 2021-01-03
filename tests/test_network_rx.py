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

import icloudpd.network_rx

class NetworkTest_Rx(TestCase):

    @given(size=st.integers(min_value=1, max_value=5))
    def test_get_file_stream(self, size):
        # TODO start local server instead

        class _Context(object):
            session = requests.Session()

        context = _Context()

        result = icloudpd.network_rx.get_file_stream(
            context,
            "https://www.python.org/"
        ).pipe(
            ops.take(size),
            ops.to_iterable()
        ).run()
        self.assertEqual(len(result), size, "chunk count")
        self.assertEqual(sum(map(len, result)), 1024 * size, "downloaded size")

    def test_fetch_meta(self):
        import pyicloud
        import vcr
        with vcr.use_cassette("tests/vcr_cassettes/listing_photos.yml") as cass:
            self.assertEqual(len(cass), 6, "Cassette Content")
            context = pyicloud.PyiCloudService(
                "jdoe@gmail.com", "password1",
                client_id="DE309E26-942E-11E8-92F5-14109FE0B321")
            results = rx.just(context).pipe(
                icloudpd.network_rx.fetch_meta("All Photos"),
                ops.take(100),
                ops.to_iterable()
            ).run()
            self.assertEqual(cass.play_count, 4, "Cassette Content Played") # there are two more requests in cassette, don;t know what they are
        self.assertEqual(len(results), 100, "Result")

    def test_meta_len(self):
        import pyicloud
        import vcr
        with vcr.use_cassette("tests/vcr_cassettes/listing_photos.yml") as cass:
            self.assertEqual(len(cass), 6, "Cassette Content")
            context = pyicloud.PyiCloudService(
                "jdoe@gmail.com", "password1",
                client_id="DE309E26-942E-11E8-92F5-14109FE0B321")
            results = rx.just(context).pipe(
                icloudpd.network_rx.meta_len("All Photos"),
                ops.to_iterable()
            ).run()
            self.assertEqual(cass.play_count, 4, "Cassette Content Played") # there are two more requests in cassette, don;t know what they are
        self.assertEqual(len(results), 1, "Result")
        self.assertEqual(results[0], 33161, "Len")
