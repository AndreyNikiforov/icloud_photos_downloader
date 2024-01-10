""" Basic non-streaming http transport abstractions """

from returns_ext.interfaces.monoid import Monoid1

class Request(Monoid1):
    """ For client Need this object to be composable (semigroup) and with predefined typed schema """
    pass

class Response(Monoid1):
    """ For Server Need this object to be composable (semigroup) and with predefined typed schema """
    pass

