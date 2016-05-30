# The idea here is to test that __init__ was called.
# 'validate_as_int' has to be a global variable since Field.__init__() doesn't
# take any arguments.
# The logic of InitField.validate() changes based on the value of its
# 'validate_as_int' attribute.

import unittest

from formscribe import Field
from formscribe import Form
from formscribe import ValidationError

validate_as_int = True
submitted_value = None


class TestForm(Form):
    class TestField(Field):
        key = 'test-key'

        def __init__(self):
            global validate_as_int
            self.validate_as_int = validate_as_int

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
            global submitted_value
            submitted_value = value


class TestInitField(unittest.TestCase):
    def setUp(self):
        global submitted_value
        submitted_value = None

    def test_init(self):
        global validate_as_int
        validate_as_int = True

        TestForm({'test-key': 3})
        self.assertEqual(submitted_value, 3)

        validate_as_int = False
        TestForm({'test-key': ' 3 '})
        self.assertEqual(submitted_value, '3')
