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

    For parameters 'dsn', 'release' and 'environment', the value is taken
    from the environment variable if it is set, otherwise from the class
    attribute if it is set.

    For each parameter, the name of the environment variable name is 'SENTRY_'
    followed by the parameter name in upper case.

    The class attribute tags, if set, will be added to the global scope of the
    current Sentry SDK.

    :cvar dsn: sentry DSN (Data Source Name) used to identify the project in sentry
    :cvar release: release version of your application
    :cvar environment: environment name (e.g., 'production', 'staging', 'development')
    :cvar integrations: list of sentry SDK integrations to enable (default: argv, excepthook,
        logging, modules, pure_eval, stdlib, threading)
    :cvar debug: enable debug mode for the sentry SDK (default: False)
    :cvar attach_stacktrace: attach stacktraces to messages (default: False)
    :cvar shutdown_timeout: time in seconds to wait for pending events to be sent before
        shutdown (default: 2.0)
    :cvar send_default_pii: send personally identifiable information by default (default: None)
    :cvar default_integrations: enable sentry's default integrations (default: True)
    :cvar traces_sample_rate: percentage of transactions to sample (0.0 to 1.0) (default: 1.0)
    :cvar profiles_sample_rate: percentage of transactions to profile (0.0 to 1.0) (default: 1.0)
    :cvar tags: dictionary of tags to apply to all events (default: {})
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

    debug: bool = False
    attach_stacktrace: bool = False
    shutdown_timeout: float = 2.0
    send_default_pii: bool | None = None
    default_integrations: bool = True

    traces_sample_rate: float = 1.0
    profiles_sample_rate: float = 1.0

    tags: t.Dict[str, str] = {}

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
            release=cls._get_str_param('release'),
            environment=cls._get_str_param('environment'),
            integrations=cls.integrations,
            traces_sample_rate=cls.traces_sample_rate,
            profiles_sample_rate=cls.profiles_sample_rate,
            enable_tracing=cls.profiles_sample_rate > 0,
            debug=cls.debug,
            attach_stacktrace=cls.attach_stacktrace,
            shutdown_timeout=cls.shutdown_timeout,
            send_default_pii=cls.send_default_pii,
            default_integrations=cls.default_integrations,
            **kwargs)

        sentry_sdk.set_tags(cls.tags)
