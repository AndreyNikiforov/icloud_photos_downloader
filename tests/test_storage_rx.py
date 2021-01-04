from unittest import TestCase
from hypothesis import given, settings
import hypothesis.strategies as st
import json
from collections import defaultdict
import rx
from rx import operators as ops
import os
import inspect

import icloudpd.storage_rx

class SaveTest_Rx(TestCase):

    @given(chunks=st.lists(st.binary(max_size=20), max_size=5)) 
    @settings(deadline=500) # sensitive to disk io speed
    def test_save_file(self, chunks):
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

        result = icloudpd.storage_rx.save_file(
            path_like,
            lambda schedule: rx.from_iterable(chunks, schedule)
        ).pipe(ops.to_iterable()).run()
        self.assertEqual(result, [path_like], "Returned Result")
        self.assertTrue(os.path.exists(path_like), "File exists")
        self.assertEqual(os.stat(path_like).st_size, size, "File size")

    @given(size=st.integers(min_value=0, max_value=100))
    @settings(deadline=500) # sensitive to disk io speed
    def test_save_with_rename(self, size):
        base_dir = os.path.normpath(f"tests/fixtures/Photos/{inspect.stack()[0][3]}")
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

        import random

        # generate temp file
        path_like = None
        while path_like == None or os.path.exists(path_like):
            path_like = os.path.join(base_dir, f"{size}_{random.randint(0, 1000000)}")
        # print(f"path_like: {path_like}")

        def _save_file(size):
            def _internal(path):
                nonlocal size
                with open(path, "a") as f:
                    f.truncate(size)
                # print(f"Created {path} of size {size}")
            return _internal

        def _saver(orig_path, saver):
            def _internal(passed_path):
                nonlocal orig_path, saver
                return rx.return_value(passed_path).pipe(
                    ops.filter(lambda x: x != orig_path),
                    ops.do(rx.core.Observer(saver))
                )
            return _internal

        result = icloudpd.storage_rx.save_file_with_rename(
            path_like,
            _saver(path_like, _save_file(size)),
        ).pipe(ops.to_iterable()).run()
        self.assertEqual(result, [path_like], "Returned Result")
        self.assertTrue(os.path.exists(path_like), "File exists")
        self.assertEqual(os.stat(path_like).st_size, size, "File size")
