import unittest

from formscribe import Field
from formscribe.error import InvalidFieldError


class NoRegexKey(Field):
    """Missing the 'regex_key' attribute."""

    regex_group = 'some-group'
    regex_group_key = 'some-group-key'

    def validate(self, value):
        return value


class NoRegexGroup(Field):
    """Missing the 'regex_group' attribute."""

    regex_key = 'some-key'
    regex_group_key = 'some-group-key'

    def validate(self, value):
        return value


class NoRegexGroupKey(Field):
    """Missing the 'regex_group_key' attribute."""

    regex_key = 'some-key'
    regex_group = 'some-group'

    def validate(self, value):
        return value


class Empty(Field):
    """Missing all attributes which specify how this field works."""

    def validate(self, value):
        return value


class RegexAndKeyBased(Field):
    """Field is both a normal field and a regular expression based one."""

    key = 'some-key'
    regex_key = 'some-regex-key'

    def validate(self, value):
        return value


class TestInvalidFields(unittest.TestCase):
    """All fields being created here must raise an InvalidFieldError."""

    def test_no_regex_key(self):
        self.assertRaises(InvalidFieldError, NoRegexKey, {})

    def test_no_regex_group(self):
        self.assertRaises(InvalidFieldError, NoRegexGroup, {})

    def test_no_regex_group_key(self):
        self.assertRaises(InvalidFieldError, NoRegexGroupKey, {})

    def test_empty(self):
        self.assertRaises(InvalidFieldError, Empty, {})

    def test_regex_and_key_based(self):
        self.assertRaises(InvalidFieldError, RegexAndKeyBased, {})
