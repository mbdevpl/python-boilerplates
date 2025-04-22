"""Unit tests for Sentry boilerplate."""

import logging
import sys
import unittest
import unittest.mock

import boilerplates.sentry


class SentryTests(unittest.TestCase):

    def test_init(self):
        with self.assertLogs('boilerplates.sentry', logging.INFO) as context:
            boilerplates.sentry.Sentry.init()
        self.assertEqual(len(context.output), 1, msg=context.output)
        self.assertIn('skipping Sentry SDK initialisation', context.output[0])

    def test_init_without_dsn(self):
        class Sentry(boilerplates.sentry.Sentry):
            dsn = ''
        with self.assertLogs('boilerplates.sentry', logging.INFO) as context, \
                unittest.mock.patch('sentry_sdk.init') as sentry_sdk_init_mock:
            Sentry.init()
        sentry_sdk_init_mock.assert_not_called()
        self.assertEqual(len(context.output), 1, msg=context.output)
        self.assertIn('skipping Sentry SDK initialisation', context.output[0])

    @unittest.skipUnless(sys.version_info >= (3, 10), 'this test requires Python 3.10')
    def test_init_with_dsn(self):
        class Sentry(boilerplates.sentry.Sentry):
            dsn = 'https://spam@ham.ingest.sentry.io/eggs'
        with self.assertNoLogs('boilerplates.sentry', logging.INFO), \
                unittest.mock.patch('sentry_sdk.init') as sentry_sdk_init_mock:
            Sentry.init()
        sentry_sdk_init_mock.assert_called_once()

    @unittest.skipUnless(sys.version_info >= (3, 10), 'this test requires Python 3.10')
    def test_init_with_envvar(self):
        class Sentry(boilerplates.sentry.Sentry):
            pass
        environ_override = {'SENTRY_DSN': 'https://spam@ham.ingest.sentry.io/eggs'}
        with unittest.mock.patch.dict('os.environ', environ_override), \
                self.assertNoLogs('boilerplates.sentry', logging.INFO), \
                unittest.mock.patch('sentry_sdk.init') as sentry_sdk_init_mock:
            Sentry.init()
        sentry_sdk_init_mock.assert_called_once()

    @unittest.skipUnless(sys.version_info >= (3, 10), 'this test requires Python 3.10')
    def test_configure_with_envvars(self):
        class Sentry(boilerplates.sentry.Sentry):
            dsn = 'https://spam@ham.ingest.sentry.io/eggs'
        environ_override = {'SENTRY_PROFILES_SAMPLE_RATE': '0.42', 'SENTRY_DEBUG': 'True'}
        with unittest.mock.patch.dict('os.environ', environ_override), \
                self.assertNoLogs('boilerplates.sentry', logging.INFO), \
                unittest.mock.patch('sentry_sdk.init') as sentry_sdk_init_mock:
            Sentry.init()
        sentry_sdk_init_mock.assert_called_once()
        self.assertIn('profiles_sample_rate', sentry_sdk_init_mock.call_args.kwargs)
        self.assertEqual(sentry_sdk_init_mock.call_args.kwargs['profiles_sample_rate'], 0.42)
        self.assertIn('debug', sentry_sdk_init_mock.call_args.kwargs)
        self.assertTrue(sentry_sdk_init_mock.call_args.kwargs['debug'], 0.42)
