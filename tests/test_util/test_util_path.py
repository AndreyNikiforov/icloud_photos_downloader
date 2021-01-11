
from unittest import TestCase
# from hypothesis import given
# import hypothesis.strategies as st

import icloudpd.util.path as ut

class UtilPathTest(TestCase):

    def test_set_ext_add(self):
        path = 'abc'
        ext = '.def'
        result = str(ut.set_ext(path, ext))
        self.assertEqual(result, 'abc.def')

    def test_set_ext_empty(self):
        path = 'abc'
        ext = ''
        result = str(ut.set_ext(path, ext))
        self.assertEqual(result, 'abc')

    def test_set_ext_replace_last(self):
        path = 'abc.tar.gz'
        ext = '.def'
        result = str(ut.set_ext(path, ext))
        self.assertEqual(result, 'abc.tar.def')
