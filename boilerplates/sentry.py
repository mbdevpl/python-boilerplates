"""Boilerplate for integrating Sentry into the project."""

import logging
import os
import typing as t

import sentry_sdk
import sentry_sdk.integrations
import sentry_sdk.integrations.argv
import sentry_sdk.integrations.excepthook
import sentry_sdk.integrations.logging
import sentry_sdk.integrations.modules
import sentry_sdk.integrations.pure_eval
import sentry_sdk.integrations.stdlib
import sentry_sdk.integrations.threading

_LOG = logging.getLogger(__name__)


class Sentry:
    """Sentry configuration.

    For each parameter, the value is taken from the environment variable if it is set, otherwise
    from the class attribute if it is set.

    For each parameter, the name of the environment variable name is 'SENTRY_'
    followed by the parameter name in upper case.
    """

    dsn: str
    release: str
    environment: str
    integrations: t.List[sentry_sdk.integrations.Integration] = [
        sentry_sdk.integrations.argv.ArgvIntegration(),
        sentry_sdk.integrations.excepthook.ExcepthookIntegration(always_run=False),
        sentry_sdk.integrations.logging.LoggingIntegration(
            level=logging.INFO, event_level=logging.ERROR),
        sentry_sdk.integrations.modules.ModulesIntegration(),
        sentry_sdk.integrations.pure_eval.PureEvalIntegration(),
        sentry_sdk.integrations.stdlib.StdlibIntegration(),
        sentry_sdk.integrations.threading.ThreadingIntegration()
    ]

    traces_sample_rate: float = 1.0
    profiles_sample_rate: float = 1.0

    @classmethod
    def _get_str_param(cls, param_name: str) -> t.Optional[str]:
        """Get a string parameter value by checking envvar first.

        Works only for 'dsn', 'release' or 'environment' parameters.
        """
        assert param_name in ('dsn', 'release', 'environment'), param_name
        return os.environ.get(f'SENTRY_{param_name.upper()}', getattr(cls, param_name, None))

    @classmethod
    def is_dsn_set(cls) -> bool:
        """Check if Sentry DSN parameter is set, thus if Sentry SDK should be initialised or not."""
        dsn = cls._get_str_param('dsn')
        return dsn is not None and len(dsn) > 0

    @classmethod
    def init(cls, *args, **kwargs):
        """Initialise Sentry SDK."""
        if not cls.is_dsn_set():
            _LOG.info('Sentry DSN is not set, skipping Sentry SDK initialisation')
            return
        sentry_sdk.init(
            *args, dsn=cls._get_str_param('dsn'),
            release=cls._get_str_param('release'), environment=cls._get_str_param('environment'),
            integrations=cls.integrations,
            traces_sample_rate=cls.traces_sample_rate,
            profiles_sample_rate=cls.profiles_sample_rate,
            enable_tracing=cls.profiles_sample_rate > 0,
            **kwargs)
