"""Tests for base Form and Field classes."""

import unittest

from formscribe import Field
from formscribe import Form
from formscribe.error import InvalidFieldError


class TestForm(unittest.TestCase):
    def test(self):
        form = Form({})
        self.assertEqual(len(form.errors), 0)


class TestField(unittest.TestCase):
    def test_validate(self):
        with self.assertRaises(NotImplementedError):
            Field().validate(None)

    def test_submit(self):
        with self.assertRaises(NotImplementedError):
            Field().submit(None)


class NoRegexGroupForm(Form):
    class NoRegexGroup(Field):
        regex_key = 'some-key'
        regex_group_key = 'some-group-key'

        def validate(self, value):
            return value


class NoRegexGroupKeyForm(Form):
    class NoRegexGroupKey(Field):
        regex_key = 'some-key'
        regex_group = 'some-group'

        def validate(self, value):
            return value


class TestRegexFields(unittest.TestCase):
    def test_no_regex_group(self):
        with self.assertRaises(InvalidFieldError):
            NoRegexGroupForm({})

    def test_no_regex_group_key(self):
        with self.assertRaises(InvalidFieldError):
            NoRegexGroupKeyForm({})
