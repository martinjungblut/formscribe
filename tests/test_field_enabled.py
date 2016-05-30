import unittest

from formscribe import Field
from formscribe import Form

is_enabled = True
has_submitted = False


class CallableEnabledForm(Form):
    class CallableEnabledField(Field):
        key = 'test-key'

        def enabled(self):
            global is_enabled
            return is_enabled

        def validate(self, value):
            return bool(value)

        def submit(self, value):
            global has_submitted
            has_submitted = True


class PropertyEnabledForm(Form):
    class PropertyEnabledField(Field):
        key = 'test-key'

        @property
        def enabled(self):
            global is_enabled
            return is_enabled

        def validate(self, value):
            return bool(value)

        def submit(self, value):
            global has_submitted
            has_submitted = True


class StaticEnabledForm(Form):
    class StaticEnabledField(Field):
        key = 'test-key'
        enabled = False

        def validate(self, value):
            return bool(value)

        def submit(self, value):
            global has_submitted
            has_submitted = True


class TestFieldEnabled(unittest.TestCase):
    def setUp(self):
        global has_submitted
        global is_enabled
        has_submitted = False
        is_enabled = True

    def test_callable_enabled(self):
        CallableEnabledForm({'test-key': True})
        self.assertTrue(has_submitted)

        global has_submitted
        global is_enabled
        is_enabled = False
        has_submitted = False
        CallableEnabledForm({'test-key': True})
        self.assertFalse(has_submitted)

    def test_property_enabled(self):
        PropertyEnabledForm({'test-key': True})
        self.assertTrue(has_submitted)

        global has_submitted
        global is_enabled
        is_enabled = False
        has_submitted = False
        PropertyEnabledForm({'test-key': True})
        self.assertFalse(has_submitted)

    def test_static_enabled(self):
        StaticEnabledForm({'test-key': True})
        self.assertFalse(has_submitted)
