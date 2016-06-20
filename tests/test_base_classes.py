"""Tests for base Form and Field classes."""

import unittest

from formscribe import Field
from formscribe import Form
from formscribe.error import InvalidFieldError


class KwargsSettersForm(Form):
    def submit(self):
        self.session['value'] = 3


class TestForm(unittest.TestCase):
    def test_no_errors(self):
        form = Form({})
        self.assertEqual(len(form.errors), 0)

    def test_kwargs_setters(self):
        session = {}
        form = KwargsSettersForm({}, session=session)

        self.assertEqual(len(form.errors), 0)
        self.assertEqual(form.session, session)
        self.assertEqual(session['value'], 3)


class TestField(unittest.TestCase):
    def test_validate(self):
        field = Field()
        self.assertRaises(NotImplementedError, field.validate, None)

    def test_submit(self):
        field = Field()
        self.assertRaises(NotImplementedError, field.submit, None)


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
        self.assertRaises(InvalidFieldError, NoRegexGroupForm, {})

    def test_no_regex_group_key(self):
        self.assertRaises(InvalidFieldError, NoRegexGroupKeyForm, {})
