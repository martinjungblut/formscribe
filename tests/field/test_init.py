from formscribe import Field
from formscribe import Form
from formscribe.error import ValidationError
from tests.helpers import StatefulTest


class TestFieldInitForm(Form):
    class TestFieldInitField(Field):
        key = 'test-key'

        def __init__(self):
            self.validate_as_int = StatefulTest.world['validate_as_int']

        def validate(self, value):
            if self.validate_as_int:
                try:
                    return int(value)
                except Exception:
                    raise ValidationError(0)
            else:
                try:
                    return value.strip()
                except Exception:
                    raise ValidationError(1)

        def submit(self, value):
            StatefulTest.world['submitted_value'] = value


class TestFieldInit(StatefulTest):
    def setUp(self):
        self.world['submitted_value'] = None

    def test_init(self):
        self.world['validate_as_int'] = True
        TestFieldInitForm({'test-key': 3})
        self.assertEqual(self.world['submitted_value'], 3)

        self.world['validate_as_int'] = False
        TestFieldInitForm({'test-key': ' 3 '})
        self.assertEqual(self.world['submitted_value'], '3')
