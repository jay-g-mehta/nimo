import testtools


def mask_decorator(*args, **kwargs):
    """patches any decorator method with do-nothing decorator"""
    def do_nothing(f):
        return f
    return do_nothing


class TestCase(testtools.TestCase):
    """Test case base class for all unit tests."""

    def setUp(self):
        """Run before each test method to initialize test environment."""
        super(TestCase, self).setUp()
