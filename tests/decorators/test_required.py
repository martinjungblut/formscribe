from formscribe import Field
from formscribe import Form
from formscribe.decorators import required
from tests.helpers import StatefulTest


class RequiredForm(Form):
    @required('Name is required.')
    class Name(Field):
        key = 'name'

        def validate(self, value):
            StatefulTest.world['name'] = value.upper()


class TestRequired(StatefulTest):
    def test_success(self):
        # the required decorator must never modify the values it takes
        form = RequiredForm(data={'name': ' john '})
        self.assertFalse(form.errors)
        self.assertEqual(StatefulTest.world['name'], ' JOHN ')

    def test_error_not_posted(self):
        form = RequiredForm(data={})
        self.assertEqual(len(form.errors), 1)
        self.assertEqual(form.errors[0].message, 'Name is required.')

    def test_error_false_value(self):
        for false_value in (None, '', ' ', '  '):
            form = RequiredForm(data={'name': false_value})
            self.assertEqual(len(form.errors), 1)
            self.assertEqual(form.errors[0].message, 'Name is required.')
