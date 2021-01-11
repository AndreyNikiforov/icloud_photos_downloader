from unittest import TestCase
from hypothesis import given, settings
import hypothesis.strategies as st
import json
from collections import defaultdict
import os
import inspect

import icloudpd.file as fs

class FileSystemTest(TestCase):

    @given(chunks=st.lists(st.binary(max_size=20), max_size=5)) 
    @settings(deadline=500) # sensitive to disk io speed
    def test_stream_to_file(self, chunks):
        base_dir = os.path.normpath(f"tests/fixtures/Photos/{inspect.stack()[0][3]}")
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

        size = sum(map(lambda x: len(x), chunks))

        import random

        # generate temp file
        path_like = None
        while path_like == None or os.path.exists(path_like):
            path_like = os.path.join(base_dir, f"{size}_{random.randint(0, 1000000)}")
        # print(f"path_like: {path_like}")

        result = fs.stream_to_file(
            path_like,
            chunks
        )
        self.assertEqual(result, size, "Returned Result")
        self.assertTrue(os.path.exists(path_like), "File exists")
        self.assertEqual(os.stat(path_like).st_size, size, "File size")

    def test_ensure_folder_to_create(self):
        base_dir = os.path.normpath(f"tests/fixtures/Photos/{inspect.stack()[0][3]}")
        if os.path.exists(base_dir):
            import shutil
            shutil.rmtree(base_dir)

        import random

        # generate temp file
        path_like = os.path.join(base_dir, f"{random.randint(0, 1000000)}")

        # print(f"path_like: {path_like}")

        result = fs.ensure_folder(
            path_like
        )
        self.assertTrue(result, "Was created")

    def test_ensure_folder_exists(self):
        base_dir = os.path.normpath(f"tests/fixtures/Photos/{inspect.stack()[0][3]}")
        if os.path.exists(base_dir):
            import shutil
            shutil.rmtree(base_dir)

        os.makedirs(base_dir)

        import random

        # generate temp file
        path_like = os.path.join(base_dir, f"{random.randint(0, 1000000)}")

        # print(f"path_like: {path_like}")

        result = fs.ensure_folder(
            path_like
        )
        self.assertFalse(result, "Was NOT created")
