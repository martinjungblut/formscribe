from formscribe import Field
from formscribe import Form
from formscribe.decorators import boolean
from tests.helpers import StatefulTest


class BooleanForm(Form):
    @boolean
    class Enabled(Field):
        key = 'enabled'

        def validate(self, value):
            StatefulTest.world['enabled'] = int(value)


class TestBoolean(StatefulTest):
    def test_true_values(self):
        for value in ('1', 1, True):
            form = BooleanForm(data={'enabled': value})
            self.assertFalse(form.errors)
            self.assertEqual(StatefulTest.world['enabled'], 1)

    def test_false_values(self):
        for value in ('', None, False, 0):
            form = BooleanForm(data={'enabled': value})
            self.assertFalse(form.errors)
            self.assertEqual(StatefulTest.world['enabled'], 0)

    def test_not_posted(self):
        form = BooleanForm(data={})
        self.assertFalse(form.errors)
        self.assertEqual(StatefulTest.world['enabled'], 0)
