from unittest import TestCase
from hypothesis import given
import hypothesis.strategies as st

import icloudpd.util.operators as ut

class OperatorTest(TestCase):

    @given(s=st.integers() | st.decimals(allow_nan=False) | st.booleans() | st.floats(allow_nan=False) | st.none())
    def test_compose_empty(self, s):
        result = ut.compose()(s)
        self.assertEqual(result, s)


    @given(s=st.integers() | st.decimals(allow_nan=False) | st.booleans() | st.floats(allow_nan=False) | st.none())
    def test_compose_lambdas(self, s):
        
        results = ut.compose(
            lambda x: ('a', x),
            lambda x: ('b', x),
            lambda x: ('c', x),
        )(s)
        self.assertEqual(results, ('c', ('b', ('a', s))))

    @given(s=st.integers() | st.decimals(allow_nan=False) | st.booleans() | st.floats(allow_nan=False) | st.none())
    def test_compose_one_lambda(self, s):
        
        results = ut.compose(
            lambda x: ('a', x),
        )(s)
        self.assertEqual(results, ('a', s))

    @given(
        s=st.integers() | st.decimals(allow_nan=False) | st.booleans() | st.floats(allow_nan=False),
        d=st.integers() | st.decimals(allow_nan=False) | st.booleans() | st.floats(allow_nan=False)
    )
    def test_default_if_none_value(self, s, d):
        self.assertEqual(ut.default_if_none(d)(s), s)

    @given(d=st.integers() | st.decimals(allow_nan=False) | st.booleans() | st.floats(allow_nan=False))
    def test_default_if_none_default(self, d):
        self.assertEqual(ut.default_if_none(d)(None), d)

    @given(t=st.tuples(
        st.integers() | st.decimals(allow_nan=False) | st.booleans() | st.floats(allow_nan=False),
        st.integers() | st.decimals(allow_nan=False) | st.booleans() | st.floats(allow_nan=False),
        )
    )
    def test_all_or_none_valid(self, t):
        self.assertEqual(ut.all_or_none()(t), t)

    @given(t=st.tuples(
        st.integers() | st.decimals(allow_nan=False) | st.booleans() | st.floats(allow_nan=False),
        st.none(),
        )
    )
    def test_all_or_none_with_none(self, t):
        self.assertIsNone(ut.all_or_none()(t))

    @given(t=st.tuples(
        st.none(),
        )
    )
    def test_all_or_none_single_tuple_none(self, t):
        self.assertIsNone(ut.all_or_none()(t))

    @given(t=st.none())
    def test_all_or_none_single_none(self, t):
        with self.assertRaises(TypeError):
            ut.all_or_none()(t)
