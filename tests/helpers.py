"""FormScribe testing helpers."""

import unittest


class FormScribeTest(unittest.TestCase):
    """
    Base class for all FormScribe tests.

    Attributes:
        world (dict): dictionary representing the stateful environment in which
                      Field and Form objects may perform their submit
                      operations.
                      This attribute is reset automatically by
                      setUp() and tearDown().
    """

    world = {}

    def setUp(self):
        FormScribeTest.world = {}

    def tearDown(self):
        FormScribeTest.world = {}
