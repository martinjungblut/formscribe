import hashlib
import unittest

from formscribe import Field
from formscribe import ValidationError


class Password(Field):
    key = 'password'

    def validate(self, value):
        try:
            value = value.strip()
        except AttributeError:
            raise ValidationError(0)

        return hashlib.md5(value.encode('utf-8')).hexdigest()


class TestFieldUsage(unittest.TestCase):
    def setUp(self):
        self.password_value= 'test'
        self.password_checksum = '098f6bcd4621d373cade4e832627b4f6'

    def test_validation_error(self):
        # kwargs only
        with self.assertRaises(ValidationError):
            Password(value=3, automatically_validate=True)

        # mix kwargs with args
        with self.assertRaises(ValidationError):
            Password(3, automatically_validate=True)

        # no kwargs
        with self.assertRaises(ValidationError):
            Password(3, True)

        # default args
        with self.assertRaises(ValidationError):
            Password(3)

        instance = Password()
        self.assertTrue(isinstance(instance, Password))

    def test_successful(self):
        # kwargs only
        self.assertEqual(Password(value=self.password_value, automatically_validate=True),
                         self.password_checksum)

        # mix kwargs with args
        self.assertEqual(Password(self.password_value, automatically_validate=True),
                         self.password_checksum)
        # no kwargs
        self.assertEqual(Password(self.password_value, True),
                         self.password_checksum)
