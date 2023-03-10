# -*- coding: utf-8 -*-
"""API for performing initial signup."""
from ...constants.logs import LOG_LEVEL_API
from ...exceptions import ApiError
from ...http import Http
from ...logs import get_obj_log
from ...tools import token_parse
from .. import json_api
from ..api_endpoints import ApiEndpoints


class Signup:
    """API for performing initial signup.

    Examples:
        * Check if initial signup has been done: :meth:`is_signed_up`
        * Perform initial signup: :meth:`signup`

    """

    @property
    def is_signed_up(self) -> bool:
        """Check if initial signup has been done.

        Examples:
            >>> signup = axonius_api_client.Signup(url="10.20.0.61")
            >>> signup.is_signed_up
            True
        """
        return self._get().value

    @property
    def system_status(self) -> json_api.signup.SystemStatus:
        """Pass."""
        return self._status()

    def signup(self, password: str, company_name: str, contact_email: str) -> dict:
        """Perform the initial signup and get the API key and API secret of admin user.

        Examples:
            >>> signup = axonius_api_client.Signup(url="10.20.0.61")
            >>> data = signup.signup(
            ...     password="demo", company_name="Axonius", contact_email="jim@axonius.com"
            ... )
            >>> data
            {'api_key': 'xxxx', 'api_secret': 'xxxx'}

        Args:
            password: password for admin user
            company_name: name of company
            contact_email: email address of company contact
        """
        return self._perform(
            password=password, company_name=company_name, contact_email=contact_email
        ).to_dict()

    def validate_password_reset_token(self, token: str) -> bool:
        """Pass."""
        token = token_parse(token)
        data = self._token_validate(token=token)
        return data.value

    def use_password_reset_token(
        self, token: str, password: str
    ) -> json_api.password_reset.UseResponse:
        """Use a password token reset link to change a users password.

        Args:
            token: password reset token
            password: password to set

        Notes:
            token can be generated by
            :meth:`axonius_api_client.api.system.system_users.SystemUsers.get_password_reset_link`
            or
            :meth:`axonius_api_client.api.system.system_users.SystemUsers.email_password_reset_link`

        Returns:
            name of user whose password was reset
        """
        token = token_parse(token)
        if not self.validate_password_reset_token(token=token):
            raise ApiError(f"Password reset token is not valid: {token}")

        data = self._token_use(token=token, password=password)
        return data

    def _status(self) -> json_api.signup.SystemStatus:
        """Direct API method to get the status of the overall system."""
        api_endpoint = ApiEndpoints.signup.status
        return api_endpoint.perform_request(http=self.http)

    def _get(self) -> json_api.generic.BoolValue:
        """Direct API method to get the status of initial signup."""
        api_endpoint = ApiEndpoints.signup.get
        return api_endpoint.perform_request(http=self.http)

    def _token_validate(self, token: str) -> json_api.password_reset.ValidateResponse:
        """Pass."""
        api_endpoint = ApiEndpoints.password_reset.validate
        request_obj = api_endpoint.load_request(token=token)
        return api_endpoint.perform_request(http=self.http, request_obj=request_obj)

    def _token_use(self, token: str, password: str) -> json_api.password_reset.UseResponse:
        """Direct API method to use a reset token to change a password.

        Args:
            token: password reset token
            password: password to set
        """
        api_endpoint = ApiEndpoints.password_reset.use
        request_obj = api_endpoint.load_request(token=token, password=password)
        return api_endpoint.perform_request(http=self.http, request_obj=request_obj)

    def _perform(
        self, password: str, company_name: str, contact_email: str
    ) -> json_api.signup.SignupResponse:
        """Direct API method to do the initial signup.

        Args:
            password: password to set to admin user
            company_name: company name
            contact_email: contact email
        """
        api_endpoint = ApiEndpoints.signup.perform
        request_obj = api_endpoint.load_request(
            company_name=company_name,
            new_password=password,
            confirm_new_password=password,
            contact_email=contact_email,
            user_name="admin",
            api_keys=True,
        )
        return api_endpoint.perform_request(http=self.http, request_obj=request_obj)

    def __init__(self, url, **kwargs):
        """Provide an API for performing initial signup.

        Args:
            url: url of instance to perform signup against
            **kwargs: passed thru to :obj:`axonius_api_client.http.Http`
        """
        log_level = kwargs.get("log_level", LOG_LEVEL_API)
        self.LOG = get_obj_log(obj=self, level=log_level)
        kwargs.setdefault("certwarn", False)
        self.HTTP = self.http = Http(url=url, **kwargs)
