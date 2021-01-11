from unittest import TestCase
from hypothesis import given, settings
import hypothesis.strategies as st
import json
from collections import defaultdict
import os
import inspect
import requests
import itertools as it

import icloudpd.cloud.network as network

class NetworkTest(TestCase):

    @given(size=st.integers(min_value=1, max_value=5))
    @settings(deadline=None) # sensitive to network speed
    def test_fetch_file_stream(self, size):
        # TODO start local server instead

        class _Context(object):
            session = requests.Session()

        context = _Context()

        result = list(
            it.islice(
                network.fetch_file_stream(
                    context,
                    "https://www.python.org/"
                ),
                size
            )
        )
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
            results = list(
                it.islice(
                    network.fetch_meta(
                        "All Photos",
                        context,
                    ),
                    100,
                )
            )
            self.assertEqual(cass.play_count, 4, "Cassette Content Played") # there are two more requests in cassette, don;t know what they are
        self.assertEqual(len(results), 100, "Result")

    def test_fetch_meta_len(self):
        import pyicloud
        import vcr
        with vcr.use_cassette("tests/vcr_cassettes/listing_photos.yml") as cass:
            self.assertEqual(len(cass), 6, "Cassette Content")
            context = pyicloud.PyiCloudService(
                "jdoe@gmail.com", "password1",
                client_id="DE309E26-942E-11E8-92F5-14109FE0B321")
            result = network.fetch_meta_len(
                "All Photos",
                context,
            )
            self.assertEqual(cass.play_count, 4, "Cassette Content Played") # there are two more requests in cassette, don;t know what they are
        self.assertEqual(result, 33161, "Len")
