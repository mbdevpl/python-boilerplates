"""Boilerplate for integrating Sentry into the project."""

import logging
import os
import typing as t

import sentry_sdk
import sentry_sdk.integrations.logging

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

    @classmethod
    def _get_param(cls, param_name: str) -> t.Optional[str]:
        """Get a parameter value by checking envvar first."""
        return os.environ.get(f'SENTRY_{param_name.upper()}', getattr(cls, param_name, None))

    @classmethod
    def init(cls, *args, **kwargs):
        """Initialise Sentry SDK."""
        dsn = cls._get_param('dsn')
        if dsn is None or not dsn:
            _LOG.info('Sentry DSN is not set, skipping Sentry SDK initialisation')
            return
        sentry_sdk.init(
            *args, dsn=dsn,
            release=cls._get_param('release'), environment=cls._get_param('environment'),
            integrations=[
                sentry_sdk.integrations.logging.LoggingIntegration(
                    level=logging.INFO, event_level=logging.ERROR)],
            traces_sample_rate=1.0, profiles_sample_rate=1.0, enable_tracing=True,
            **kwargs)
