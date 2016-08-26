import unittest

from formscribe import Field


class TestFieldNotImplemented(unittest.TestCase):
    def test_validate_not_implemented(self):
        field = Field()
        self.assertRaises(NotImplementedError, field.validate, None)

    def test_submit_not_implemented(self):
        field = Field()
        self.assertRaises(NotImplementedError, field.submit, None)
