import unittest

from formscribe import Form


class KwargsSettersForm(Form):
    def submit(self):
        self.session['value'] = 1


class TestForm(unittest.TestCase):
    def test_no_errors(self):
        form = Form({})
        self.assertEqual(len(form.errors), 0)

        form = Form(data={})
        self.assertEqual(len(form.errors), 0)

    def test_kwargs_setters(self):
        """
        Ensure that a predefined value is set to the 'session' attribute
        that was passed as a keyword argument to the Form.
        """

        session = {}
        form = KwargsSettersForm(data={}, session=session)

        self.assertEqual(id(form.session), id(session))
        self.assertEqual(session['value'], 1)
