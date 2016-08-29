from formscribe import Field
from formscribe import Form
from formscribe.decorators import oneof
from tests.helpers import StatefulTest


class OneOfForm(Form):
    @oneof(['elf', 'orc', 'human'], 'Invalid race.')
    class Race(Field):
        key = 'race'

        def validate(self, value):
            StatefulTest.world['race'] = value.upper()


class TestOneOf(StatefulTest):
    def test_success(self):
        form = OneOfForm(data={'race': 'human'})
        self.assertFalse(form.errors)
        self.assertEqual(StatefulTest.world['race'], 'HUMAN')

    def test_error(self):
        form = OneOfForm(data={'race': 'goblin'})
        self.assertEqual(len(form.errors), 1)
        self.assertEqual(form.errors[0].message, 'Invalid race.')
