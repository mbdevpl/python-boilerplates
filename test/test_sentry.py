"""Unit tests for Sentry boilerplate."""

import logging
import unittest

import boilerplates.sentry


class SentryTests(unittest.TestCase):

    def test_init(self):
        with self.assertLogs('boilerplates.sentry', logging.INFO) as context:
            boilerplates.sentry.Sentry.init()
        self.assertEqual(len(context.output), 1, msg=context.output)
        self.assertIn('skipping Sentry SDK initialisation', context.output[0])
