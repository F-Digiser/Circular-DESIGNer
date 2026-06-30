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

from .exceptions import DiscoveryError
from .http_client import JsonHttpClient


class BpnDiscoveryClient:
    """
    Resolve supplier business partner numbers from external identifiers such as a supplier material number.

    Class-Level Constants:
        None.

    Attributes:
        http (Any): Stores the http value.
        api_path (str): Stores the api path value.
        key_type (str): Stores the key type value.

    Methods:
        __init__(): Initialize the object with the provided dependencies, default values, and internal state.
        resolve_bpnls_by_material_number(): Resolve candidate supplier BPNLs for a supplier material number.
        _extract_bpnls(): Extract BPNL values from a BPN discovery response payload.
    """

    def __init__(
        self,
        base_url: str,
        api_path: str,
        headers: dict[str, str] | None = None,
        timeout: int = 30,
        key_type: str = "materialNumber",
    ) -> None:
        """
        Initialize the object with the provided dependencies, default values, and internal state.

        Args:
                base_url (str): The base url used by this method.
                api_path (str): The api path used by this method.
                headers (dict[str, str] | None): The headers used by this method.
                timeout (int): The timeout used by this method.
                key_type (str): The key type used by this method.

        Steps:
            1. Read the provided dependencies and configuration values.
            2. Store them on the instance for later use.
            3. Prepare any internal state required by later method calls.

        Returns:
                None: This initializer configures the instance state in place.
        """
        if not base_url:
            raise DiscoveryError("BPN Discovery base URL is not configured")
        self.http = JsonHttpClient(base_url=base_url.rstrip("/"), headers=headers or {}, timeout=timeout)
        self.api_path = api_path
        self.key_type = key_type

    def resolve_bpnls_by_material_number(self, material_number: str) -> list[str]:
        """
        Resolve candidate supplier BPNLs for a supplier material number.

        Args:
                material_number (str): The supplier material number used for BPN discovery.

        Steps:
            1. Read the inputs required to resolve bpnls by material number.
            2. Perform the operations needed to resolve bpnls by material number.
            3. Return the resulting value or update the relevant application state.

        Returns:
                list[str]: The resolved supplier BPNLs for the provided material number.
        """
        body = {
            "type": self.key_type,
            "keys": [material_number],
        }
        try:
            data = self.http.post(self.api_path, body)
        except Exception as exc:
            raise DiscoveryError(f"BPN Discovery lookup failed for material number {material_number}: {exc}") from exc

        candidates = self._extract_bpnls(data)
        if not candidates:
            raise DiscoveryError(f"No BPNL found via BPN Discovery for material number {material_number}")
        return candidates

    @classmethod
    def _extract_bpnls(cls, data: Any) -> list[str]:
        """
        Extract BPNL values from a BPN discovery response payload.

        Args:
                data (Any): The data used by this method.

        Steps:
            1. Read the inputs required to  extract bpnls.
            2. Perform the operations needed to  extract bpnls.
            3. Return the resulting value or update the relevant application state.

        Returns:
                list[str]: The BPNL values extracted from the discovery response.
        """
        found: list[str] = []
        seen: set[str] = set()

        def add(value: Any) -> None:
            if isinstance(value, str) and value.startswith("BPNL") and value not in seen:
                found.append(value)
                seen.add(value)

        def walk(obj: Any) -> None:
            if isinstance(obj, dict):
                for key, value in obj.items():
                    normalized = str(key).lower()
                    if normalized in {"bpnl", "bpnlvalue", "bpnlvalue", "bpn", "businesspartnernumber"}:
                        add(value)
                    else:
                        walk(value)
            elif isinstance(obj, list):
                for item in obj:
                    walk(item)
            else:
                add(obj)

        walk(data)
        return found
