import unittest

from formscribe import Field


class KeyBasedField(Field):
    key = 'some-key'


class TestFieldNotImplemented(unittest.TestCase):
    def test_validate_not_implemented(self):
        field = KeyBasedField()
        self.assertRaises(NotImplementedError, field.validate, None)

    def test_submit_not_implemented(self):
        field = KeyBasedField()
        self.assertRaises(NotImplementedError, field.submit, None)
