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

    For parameters 'dsn', 'release', 'environment', 'default_integrations', 'debug',
    'attach_stacktrace', 'shutdown_timeout', 'traces_sample_rate' and 'profiles_sample_rate'
    the value is taken from the environment variable if it is set,
    otherwise from the class attribute if it is set.
    For those parameters, the expected name of the environment variable name is 'SENTRY_'
    followed by the parameter name in upper case.

    The class attribute tags, if set, will be added to the global scope of the
    current Sentry SDK.
    """

    dsn: str
    """Sentry DSN (Data Source Name) used to identify the project in Sentry."""

    release: str
    """Release version of your application."""

    environment: str
    """Environment name (e.g., 'production', 'staging', 'development')."""

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
    """Sentry SDK integrations to enable.

    To configure integrations that are enabled by default, also add them to this list.
    """

    default_integrations: bool = True
    """If True, enable Sentry's default integrations besides the ones set via 'integrations'."""

    debug: bool = False
    """If True, enable debug mode for the Sentry SDK."""

    attach_stacktrace: bool = False
    """If True, attach stacktraces to messages."""

    shutdown_timeout: float = 2.0
    """Time in seconds to wait for pending events to be sent before shutdown."""

    send_default_pii: t.Optional[bool] = False
    """If True, send personally identifiable information."""

    traces_sample_rate: float = 1.0
    """Ratio of transactions to sample (0.0 to 1.0)."""

    profiles_sample_rate: float = 1.0
    """Ratio of transactions to profile (0.0 to 1.0)."""

    tags: t.Dict[str, str] = {}
    """Tags to be added to all events."""

    @classmethod
    def _get_str_param(cls, param_name: str) -> t.Optional[str]:
        """Get a string parameter value by checking envvar first.

        Works only for 'dsn', 'release' or 'environment' parameters.

        :param param_name: name of the parameter to get
        :return: value of the parameter
        """
        assert param_name in ('dsn', 'release', 'environment'), param_name
        return os.environ.get(f'SENTRY_{param_name.upper()}', getattr(cls, param_name, None))

    @classmethod
    def _get_float_param(cls, param_name: str) -> float:
        assert param_name in (
            'shutdown_timeout', 'traces_sample_rate', 'profiles_sample_rate'), param_name
        if f'SENTRY_{param_name.upper()}' in os.environ:
            return float(os.environ[f'SENTRY_{param_name.upper()}'])
        return getattr(cls, param_name)

    @classmethod
    def _get_bool_param(cls, param_name: str) -> bool:
        assert param_name in ('default_integrations', 'debug', 'attach_stacktrace'), param_name
        if f'SENTRY_{param_name.upper()}' in os.environ:
            return os.environ[f'SENTRY_{param_name.upper()}'].lower() in {'true', 'yes', 'on', '1'}
        return getattr(cls, param_name)

    @classmethod
    def is_dsn_set(cls) -> bool:
        """Check if Sentry DSN parameter is set, thus if Sentry SDK should be initialised or not."""
        dsn = cls._get_str_param('dsn')
        return dsn is not None and len(dsn) > 0

    @classmethod
    def init(cls, *args, **kwargs) -> None:
        """Initialise Sentry SDK."""
        if not cls.is_dsn_set():
            _LOG.info('Sentry DSN is not set, skipping Sentry SDK initialisation')
            return
        sentry_sdk.init(
            *args, dsn=cls._get_str_param('dsn'),
            release=cls._get_str_param('release'),
            environment=cls._get_str_param('environment'),
            integrations=cls.integrations,
            traces_sample_rate=cls._get_float_param('traces_sample_rate'),
            profiles_sample_rate=cls._get_float_param('profiles_sample_rate'),
            enable_tracing=cls._get_float_param('profiles_sample_rate') > 0,
            debug=cls._get_bool_param('debug'),
            attach_stacktrace=cls._get_bool_param('attach_stacktrace'),
            shutdown_timeout=cls._get_float_param('shutdown_timeout'),
            send_default_pii=cls.send_default_pii,
            default_integrations=cls._get_bool_param('default_integrations'),
            **kwargs)

        sentry_sdk.set_tags(cls.tags)
