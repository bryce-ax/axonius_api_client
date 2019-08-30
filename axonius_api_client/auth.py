# -*- coding: utf-8 -*-
"""Axonius API authentication module."""
from __future__ import absolute_import, division, print_function, unicode_literals

import abc

import six

from . import api, constants, exceptions, tools


@six.add_metaclass(abc.ABCMeta)
class Model(object):
    """Abstract base class for all Authentication methods."""

    @abc.abstractmethod
    def login(self):
        """Login to API."""
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def logout(self):
        """Logout from API."""
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def check_login(self):
        """Throw exc if not login.

        Raises:
            :exc:`exceptions.NotLoggedIn`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractproperty
    def http(self):
        """Get HttpClient object.

        Returns:
            :obj:`axonius_api_client.http.Http`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractproperty
    def is_logged_in(self):
        """Check if login has been called.

        Returns:
            :obj:`bool`

        """
        raise NotImplementedError  # pragma: no cover


class Mixins(object):
    """Mixins for Model."""

    _logged_in = False
    """:obj:`bool`: Attribute checked by :meth:`is_logged_in`."""

    def __init__(self, http, creds, **kwargs):
        """Constructor.

        Args:
            http (:obj:`axonius_api_client.http.Http`):
                HTTP client to use to send requests.
            creds:
                Credentials used by this Auth method.

        """
        log_level = kwargs.get("log_level", constants.LOG_LEVEL_AUTH)
        self._log = tools.logs.get_obj_log(obj=self, level=log_level)

        self._http = http
        """:obj:`axonius_api_client.http.Http`: HTTP Client."""

        self._creds = creds
        """:obj:`dict`: Credential store."""

        self._check_http_lock()
        self._set_http_lock()

    def __str__(self):
        """Show object info.

        Returns:
            :obj:`str`

        """
        bits = [
            "url={!r}".format(self.http.url),
            "is_logged_in={}".format(self.is_logged_in),
        ]
        bits = "({})".format(", ".join(bits))
        return "{c.__module__}.{c.__name__}{bits}".format(c=self.__class__, bits=bits)

    def __repr__(self):
        """Show object info.

        Returns:
            :obj:`str`

        """
        return self.__str__()

    @property
    def http(self):
        """Get HttpClient object.

        Returns:
            :obj:`axonius_api_client.http.Http`

        """
        return self._http

    def _check_http_lock(self):
        """Check HTTP client not already used by another Auth.

        Raises:
            :exc:`exceptions.AuthError`

        """
        auth_lock = getattr(self.http, "_auth_lock", None)
        if auth_lock:
            msg = "{http} already being used by {auth}"
            msg = msg.format(http=self.http, auth=auth_lock)
            raise exceptions.AuthError(msg)

    def _set_http_lock(self):
        """Set HTTP Client auth lock."""
        self._http._auth_lock = self

    def _validate(self):
        """Validate credentials."""
        response = self.http(method="get", path=api.routers.ApiV1.devices.count)

        try:
            response.raise_for_status()
        except Exception as exc:
            self._logged_in = False
            raise exceptions.InvalidCredentials(auth=self, exc=exc)

        self._logged_in = True

    def logout(self):
        """Logout from API."""
        self.check_login()
        self._logged_in = False
        self._logout()

    def check_login(self):
        """Throw exc if not login.

        Raises:
            :exc:`exceptions.NotLoggedIn`

        """
        if not self.is_logged_in:
            raise exceptions.NotLoggedIn(auth=self)

    @property
    def is_logged_in(self):
        """Check if login has been called.

        Returns:
            :obj:`bool`

        """
        return self._logged_in


class ApiKey(Mixins, Model):
    """Authentication method using API key & API secret."""

    def __init__(self, http, key, secret, **kwargs):
        """Constructor.

        Args:
            http (:obj:`axonius_api_client.http.Http`):
                HTTP client to use to send requests.
            key (:obj:`str`):
                API key to use in credentials.
            secret (:obj:`str`):
                API secret to use in credentials.

        """
        creds = {"key": key, "secret": secret}
        super(ApiKey, self).__init__(http=http, creds=creds, **kwargs)

    @property
    def _cred_fields(self):
        return ["key", "secret"]

    def _logout(self):
        """Logout from API."""
        self._logged_in = False
        self.http.session.headers = {}

    def login(self):
        """Login to API."""
        if self.is_logged_in:
            raise exceptions.AlreadyLoggedIn(auth=self)

        self.http.session.headers["api-key"] = self._creds["key"]
        self.http.session.headers["api-secret"] = self._creds["secret"]

        self._validate()

        self._logged_in = True

        msg = "Successfully logged in using {}".format(self._cred_fields)
        self._log.debug(msg)


class Creds(Mixins, Model):
    """Authentication method using username & password."""

    def __init__(self, http, username, password, **kwargs):
        """Constructor.

        Args:
            http (:obj:`axonius_api_client.http.client.HttpClient`):
                HTTP client to use to send requests.
            username (:obj:`str`):
                Username to use in credentials.
            password (:obj:`str`):
                Password to use in credentials.

        """
        creds = {"username": username, "password": password}
        super(Creds, self).__init__(http=http, creds=creds, **kwargs)

    @property
    def _cred_fields(self):
        return ["username", "password"]

    def _logout(self):
        """Logout from API."""
        self._logged_in = False
        self.http.session.auth = None

    def login(self):
        """Login to API."""
        if self.is_logged_in:
            raise exceptions.AlreadyLoggedIn(auth=self)

        self.http.session.auth = (self._creds["username"], self._creds["password"])

        self._validate()

        self._logged_in = True
        msg = "Successfully logged in using {}".format(self._cred_fields)
        self._log.debug(msg)
