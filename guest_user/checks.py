from django.conf import settings as django_settings
from django.core.checks import Warning, register

from . import settings


@register()
def check_settings(app_configs, **kwargs):
    checks = []

    guest_backend = "guest_user.backends.GuestBackend"

    if settings.ENABLED and guest_backend in django_settings.AUTHENTICATION_BACKENDS:
        checks.append(
            Warning(
                "GuestBackend is in AUTHENTICATION_BACKENDS. This backend "
                "allowed guest re-login by identifier alone in older versions "
                "and is deprecated. Remove it; guest sessions are created via "
                "maybe_create_guest_user() and GUEST_USER_LOGIN_BACKEND.",
                hint=(
                    'Remove "guest_user.backends.GuestBackend" from '
                    "AUTHENTICATION_BACKENDS."
                ),
                obj="settings",
                id="guest_user.W001",
            )
        )

    return checks
