from formscribe import Field
from formscribe import Form
from tests.helpers import StatefulTest


class CallableEnabledForm(Form):
    class CallableEnabledField(Field):
        key = 'test-key'

        def enabled(self):
            return StatefulTest.world['is_enabled']

        def validate(self, value):
            return bool(value)

        def submit(self, value):
            StatefulTest.world['has_submitted'] = True


class PropertyEnabledForm(Form):
    class PropertyEnabledField(Field):
        key = 'test-key'

        @property
        def enabled(self):
            return StatefulTest.world['is_enabled']

        def validate(self, value):
            return bool(value)

        def submit(self, value):
            StatefulTest.world['has_submitted'] = True


class ClassAttributeEnabledForm(Form):
    class ClassAttributeEnabledField(Field):
        key = 'test-key'
        enabled = False

        def validate(self, value):
            return bool(value)

        def submit(self, value):
            StatefulTest.world['has_submitted'] = True


class TestFieldEnabled(StatefulTest):
    def setUp(self):
        self.world['has_submitted'] = False
        self.world['is_enabled'] = True

    def test_callable_enabled(self):
        CallableEnabledForm({'test-key': True})
        self.assertTrue(self.world['has_submitted'])

        self.world['is_enabled'] = self.world['has_submitted'] = False

        CallableEnabledForm({'test-key': True})
        self.assertFalse(self.world['has_submitted'])

    def test_property_enabled(self):
        PropertyEnabledForm({'test-key': True})
        self.assertTrue(self.world['has_submitted'])

        self.world['is_enabled'] = self.world['has_submitted'] = False

        PropertyEnabledForm({'test-key': True})
        self.assertFalse(self.world['has_submitted'])

    def test_class_attribute_enabled(self):
        ClassAttributeEnabledForm({'test-key': True})
        self.assertFalse(self.world['has_submitted'])
