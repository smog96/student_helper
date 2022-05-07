import re

import requests
from loguru import logger
from requests.auth import HTTPBasicAuth


class BaseAPI:
    def __init__(
        self,
        base_url: str,
        api_login: str,
        api_password: str,
        ssl_secure: bool = True,
    ):
        self.base_url = self._initialize_host(base_url)
        self.response_200_regex = r"^2[0-9]{2}$"  # ^https?\:\/\/
        self.api_login = api_login
        self.api_password = api_password
        self.ssl_secure = ssl_secure

    def _initialize_host(self, base_url) -> str:
        if base_url[0:4] == "http":
            raise ValueError(
                "Base api url can't start with http/https. Change secure (ssl)."
            )

        prefix = "https://"  # if self.ssl_secure else "http://"
        host = f"{prefix}{base_url}"

        if host[-1] != "/":
            host += "/"

        return host

    def _make_safe_request(
        self,
        http_method,
        endpoint: str,
        params: dict = None,
        credentials: HTTPBasicAuth = None,
    ):
        if credentials is None:
            credentials = HTTPBasicAuth(self.api_login, self.api_password)

        if params is None:
            params = {}

        try:
            request_method = getattr(requests, http_method)
            response: requests.Response = request_method(
                self.base_url + endpoint, params=params, auth=credentials
            )
            if (
                re.match(self.response_200_regex, response.status_code)
                is False
            ):
                logger.error(f"Response status code {response.status_code}.")
                return response
            return response.json()
        except ConnectionError:
            logger.error("Connection error.")
        return None
