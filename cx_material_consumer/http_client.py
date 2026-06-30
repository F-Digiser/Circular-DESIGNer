""""    
    Copyright (C) 2026  Digiser

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from __future__ import annotations

from typing import Any
import requests


class JsonHttpClient:
    """
    Wrap JSON-based HTTP GET and POST requests with a shared base URL, headers, and timeout configuration.

    Class-Level Constants:
        None.

    Attributes:
        base_url (str): Stores the base url value.
        headers (dict[str, str] | None): Stores the headers value.
        timeout (int): Stores the timeout value.

    Methods:
        __init__(): Initialize the object with the provided dependencies, default values, and internal state.
        _url(): Build the absolute request URL for one relative API path.
        get(): Send an HTTP GET request and return the JSON response body.
        post(): Send an HTTP POST request and return the JSON response body.
    """
    def __init__(self, base_url: str, headers: dict[str, str] | None = None, timeout: int = 30) -> None:
        """
        Initialize the object with the provided dependencies, default values, and internal state.

        Args:
                base_url (str): The base url used by this method.
                headers (dict[str, str] | None): The headers used by this method.
                timeout (int): The timeout used by this method.

        Steps:
            1. Read the provided dependencies and configuration values.
            2. Store them on the instance for later use.
            3. Prepare any internal state required by later method calls.

        Returns:
                None: This initializer configures the instance state in place.
        """
        self.base_url = base_url.rstrip("/")
        self.headers = headers or {}
        self.timeout = timeout

    def _url(self, path: str) -> str:
        """
        Build the absolute request URL for one relative API path.

        Args:
                path (str): The relative API path to call.

        Steps:
            1. Read the inputs required to  url.
            2. Perform the operations needed to  url.
            3. Return the resulting value or update the relevant application state.

        Returns:
                str: The value returned by this method.
        """
        if path.startswith("http://") or path.startswith("https://"):
            return path
        return f"{self.base_url}{path if path.startswith('/') else '/' + path}"

    def get(self, path: str, params: dict[str, Any] | None = None, headers: dict[str, str] | None = None) -> Any:
        """
        Send an HTTP GET request and return the JSON response body.

        Args:
                path (str): The relative API path to call.
                params (dict[str, Any] | None): The optional query parameters for the HTTP request.
                headers (dict[str, str] | None): The headers used by this method.

        Steps:
            1. Read the inputs required to get.
            2. Perform the operations needed to get.
            3. Return the resulting value or update the relevant application state.

        Returns:
                dict: The JSON response payload returned by the server.
        """
        response = requests.get(
            self._url(path),
            params=params,
            headers={**self.headers, **(headers or {})},
            timeout=self.timeout,
        )
        response.raise_for_status()
        if response.content:
            return response.json()
        return None

    def post(self, path: str, body: dict[str, Any], headers: dict[str, str] | None = None) -> Any:
        """
        Send an HTTP POST request and return the JSON response body.

        Args:
                path (str): The relative API path to call.
                body (dict[str, Any]): The JSON body sent with the POST request.
                headers (dict[str, str] | None): The headers used by this method.

        Steps:
            1. Read the inputs required to post.
            2. Perform the operations needed to post.
            3. Return the resulting value or update the relevant application state.

        Returns:
                dict: The JSON response payload returned by the server.
        """
        response = requests.post(
            self._url(path),
            json=body,
            headers={**self.headers, **(headers or {})},
            timeout=self.timeout,
        )
        response.raise_for_status()
        if response.content:
            return response.json()
        return None
