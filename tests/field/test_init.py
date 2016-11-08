from formscribe import Field
from formscribe import Form
from formscribe.error import ValidationError
from tests.helpers import StatefulTest


class MockedForm(Form):
    class MockedField(Field):
        key = 'test-key'

        def __init__(self):
            self.validate_as_int = StatefulTest.world['validate_as_int']

        def validate(self, value):
            if self.validate_as_int:
                return int(value)
            else:
                return value.strip()

        def submit(self, value):
            StatefulTest.world['submitted_value'] = value


class TestFieldInit(StatefulTest):
    """
    Make sure the Field's __init__ method is called and the attributes
    it sets are correctly defined.
    """

    def test_init_validate_as_int(self):
        self.world['validate_as_int'] = True
        MockedForm({'test-key': 3})
        self.assertEqual(self.world['submitted_value'], 3)

    def test_init_dont_validate_as_int(self):
        self.world['validate_as_int'] = False
        MockedForm({'test-key': ' 3 '})
        self.assertEqual(self.world['submitted_value'], '3')
