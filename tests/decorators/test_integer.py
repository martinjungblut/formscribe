from formscribe import Field
from formscribe import Form
from formscribe.decorators import integer
from tests.helpers import StatefulTest


class IntegerForm(Form):
    @integer('Age must be an integer.')
    class Age(Field):
        key = 'age'

        def validate(self, value):
            value = value + 1
            StatefulTest.world['age'] = value


class TestInteger(StatefulTest):
    def test_success(self):
        form = IntegerForm(data={'age': '25'})
        self.assertFalse(form.errors)
        self.assertEqual(StatefulTest.world['age'], 26)

    def test_error(self):
        form = IntegerForm(data={'age': 'invalid'})
        self.assertEqual(len(form.errors), 1)
        self.assertEqual(form.errors[0].message, 'Age must be an integer.')
