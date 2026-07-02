# Changelog

## Unreleased

### Security

- **`GuestBackend` must not be used for guest login.** `GuestBackend.authenticate()`
  no longer returns a user (it ignored passwords, which allowed re-login to guest
  accounts via the normal login form when the guest identifier is public).
- **`maybe_create_guest_user`** now logs guests in with
  `django.contrib.auth.backends.ModelBackend` (configurable via
  `GUEST_USER_LOGIN_BACKEND`) instead of authenticating through `GuestBackend`.
  Guests get a one-time session at creation and cannot re-authenticate afterwards.

### Changed

- System check **`guest_user.W001`** now **warns when `GuestBackend` is
  registered** (previously errored when it was missing).
- **`create_guest_user`**: on username collision (`IntegrityError`), email and
  password are regenerated together with the new username.
- **`create_guest_user(username=...)`**: always binds `guest+{username}@liqd.net`
  email and a generated password.

### Migration for downstream projects

1. Remove `guest_user.backends.GuestBackend` from `AUTHENTICATION_BACKENDS`.
2. Remove `SILENCED_SYSTEM_CHECKS = ["guest_user.W001"]` if added only for the
   old check.
3. `GuestCreateView` can call `maybe_create_guest_user(request)` again (or keep
   explicit `create_guest_user` + `login` — equivalent with this release).
