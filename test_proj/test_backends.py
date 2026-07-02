import pytest
from django.contrib.auth import authenticate, get_user_model
from guest_user.backends import GuestBackend
from guest_user.functions import get_guest_model, maybe_create_guest_user


@pytest.fixture
def backend():
    return GuestBackend()


@pytest.mark.django_db
def test_backend_without_user(backend):
    assert backend.authenticate(request=None, username="doesnotexist") is None


@pytest.mark.django_db
def test_backend_does_not_authenticate_normal_user(backend):
    UserModel = get_user_model()
    user = UserModel.objects.create_user(username="demo", password="hunter2")
    assert backend.authenticate(request=None, username=user.username) is None


@pytest.mark.django_db
def test_backend_does_not_authenticate_guest_user(backend):
    GuestModel = get_guest_model()
    guest = GuestModel.objects.create_guest_user()

    assert backend.authenticate(request=None, username=guest.username) is None


@pytest.mark.django_db
def test_maybe_create_guest_user_logs_in(client):
    assert client.session.get("_auth_user_id") is None

    from django.contrib.auth.models import AnonymousUser
    from django.test import RequestFactory

    request = RequestFactory().get("/")
    request.user = AnonymousUser()
    request.session = client.session
    maybe_create_guest_user(request)

    assert request.user.is_authenticated


@pytest.mark.django_db
def test_guest_cannot_relogin_via_authenticate(client):
    GuestModel = get_guest_model()
    guest = GuestModel.objects.create_guest_user()

    assert authenticate(username=guest.username, password="wrong") is None
