"""Helper file to extend on pytest functionality."""
from contextlib import contextmanager

from pytest import fail


@contextmanager
def not_raises(exception):
    """Open format and save the locations.

    Parameters
    ----------
    exception
        A exception that must not be raised to pass and fails if it does.
    """
    try:
        yield
    except exception:
        raise fail("DID RAISE {0}".format(exception))
