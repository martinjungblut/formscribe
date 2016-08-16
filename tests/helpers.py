"""Formscribe testing helpers."""

import unittest


class StatefulTest(unittest.TestCase):
    """
    Base class for stateful Formscribe tests.

    Attributes:
        world (dict): dictionary representing the stateful environment in which
                      Field and Form objects may perform their submit and
                      validate operations.
                      This attribute is reset automatically by
                      setUp() and tearDown().
    """

    world = {}

    def setUp(self):
        StatefulTest.world = {}

    def tearDown(self):
        StatefulTest.world = {}
