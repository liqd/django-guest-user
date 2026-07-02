from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from .functions import is_guest_user


class GuestBackend(ModelBackend):
    """Deprecated authentication backend.

    Earlier versions authenticated guests by identifier alone (ignoring the
    password), which allowed anyone who knew a guest's public username or email
    to log into that account via the normal login form.

    **Do not add this backend to** ``AUTHENTICATION_BACKENDS``. Guest sessions
    are started by :func:`guest_user.functions.maybe_create_guest_user` using
    ``GUEST_USER_LOGIN_BACKEND`` (``ModelBackend`` by default).
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            user = UserModel._default_manager.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
        if is_guest_user(user):
            return user
        return None
