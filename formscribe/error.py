class InvalidFieldError(Exception):
    """
    Raised whenever a field has an invalid set of attributes.

    Args:
        message (str): the message describing the error.
    """

    def __init__(self, message):
        super().__init__()
        self.message = message


class ValidationError(Exception):
    """
    Raised whenever a validation fails.
    Should be raised from the Form.validate() method.

    Args:
        message (str): the message describing the error.
    """

    def __init__(self, message):
        super().__init__()
        self.message = message


class SubmitError(Exception):
    """
    Raised whenever a given value can't be submitted.
    Should be raised from the Form.submit() method.

    Args:
        message (str): the message describing the error.
    """

    def __init__(self, message):
        super().__init__()
        self.message = message
