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

from .exceptions import BpdmLookupError
from .http_client import JsonHttpClient
from .models import BpdmAddress, BpdmSite


class BpdmPoolClient:
    """
    Provide helper methods for reading and normalizing business partner, site, and address data from the BPDM Pool API.

    Class-Level Constants:
        None.

    Attributes:
        http (Any): Stores the http value.

    Methods:
        __init__(): Initialize the object with the provided dependencies, default values, and internal state.
        get_site(): Fetch one site record from BPDM.
        get_address(): Fetch one address record from BPDM.
        get_legal_entity(): Fetch one legal-entity record from BPDM.
        describe_supplier_candidate(): Build a user-facing supplier candidate description from BPDM data.
        get_legal_entity_addresses(): Fetch the addresses associated with one legal entity.
        search_sites(): Search BPDM sites with the provided filter values.
        search_addresses(): Search BPDM addresses with the provided filter values.
        resolve_site_and_main_address(): Resolve a site and its main address from a BPNS value.
        resolve_address_by_legal_entity(): Resolve one representative address for a legal entity.
        _extract_list(): Extract a list-like payload section from a BPDM response.
        _find_first_string(): Return the first non-empty string found in the provided values.
        _normalize_site(): Normalize a raw BPDM site payload into a BpdmSite object.
        _normalize_address(): Normalize a raw BPDM address payload into a BpdmAddress object.
    """

    def __init__(self, base_url: str, api_path: str, headers: dict[str, str], timeout: int = 30) -> None:
        """
        Initialize the object with the provided dependencies, default values, and internal state.

        Args:
                base_url (str): The base url used by this method.
                api_path (str): The api path used by this method.
                headers (dict[str, str]): The headers used by this method.
                timeout (int): The timeout used by this method.

        Steps:
            1. Read the provided dependencies and configuration values.
            2. Store them on the instance for later use.
            3. Prepare any internal state required by later method calls.

        Returns:
                None: This initializer configures the instance state in place.
        """
        self.http = JsonHttpClient(
            base_url=f"{base_url.rstrip('/')}{api_path}",
            headers=headers,
            timeout=timeout,
        )

    def get_site(self, bpns: str) -> dict[str, Any]:
        """
        Fetch one site record from BPDM.

        Args:
                bpns (str): The business partner number of the supplier site.

        Steps:
            1. Read the inputs required to get site.
            2. Perform the operations needed to get site.
            3. Return the resulting value or update the relevant application state.

        Returns:
                dict: The raw BPDM site response payload.
        """
        try:
            return self.http.get(f"/sites/{bpns}")
        except Exception as exc:
            raise BpdmLookupError(f"Failed to fetch site {bpns}: {exc}") from exc

    def get_address(self, bpna: str) -> dict[str, Any]:
        """
        Fetch one address record from BPDM.

        Args:
                bpna (str): The business partner number of the supplier address.

        Steps:
            1. Read the inputs required to get address.
            2. Perform the operations needed to get address.
            3. Return the resulting value or update the relevant application state.

        Returns:
                dict: The raw BPDM address response payload.
        """
        try:
            return self.http.get(f"/addresses/{bpna}")
        except Exception as exc:
            raise BpdmLookupError(f"Failed to fetch address {bpna}: {exc}") from exc


    def get_legal_entity(self, bpnl: str) -> dict[str, Any]:
        """
        Fetch one legal-entity record from BPDM.

        Args:
                bpnl (str): The business partner number of the supplier legal entity.

        Steps:
            1. Read the inputs required to get legal entity.
            2. Perform the operations needed to get legal entity.
            3. Return the resulting value or update the relevant application state.

        Returns:
                dict: The raw BPDM legal-entity response payload.
        """
        try:
            return self.http.get(f"/legal-entities/{bpnl}")
        except Exception as exc:
            raise BpdmLookupError(f"Failed to fetch legal entity {bpnl}: {exc}") from exc

    def describe_supplier_candidate(self, bpnl: str) -> dict[str, Any]:
        """
        Build a user-facing supplier candidate description from BPDM data.

        Args:
                bpnl (str): The business partner number of the supplier legal entity.

        Steps:
            1. Read the inputs required to describe supplier candidate.
            2. Perform the operations needed to describe supplier candidate.
            3. Return the resulting value or update the relevant application state.

        Returns:
                SupplierSelectionCandidate: The supplier option enriched with BPDM details.
        """
        supplier_name = None
        city_name = None
        country_alpha2 = None
        address_bpna = None

        try:
            legal_entity = self.get_legal_entity(bpnl)
            supplier_name = self._find_first_string(legal_entity, "name", "legalName", "shortName", "tradingName")
        except BpdmLookupError:
            legal_entity = None

        try:
            address = self.resolve_address_by_legal_entity(bpnl)
            if address is not None:
                city_name = address.city_name
                country_alpha2 = address.country_alpha2
                address_bpna = address.bpna
                if not supplier_name:
                    supplier_name = address.name
        except BpdmLookupError:
            pass

        return {
            "bpnl": bpnl,
            "supplier_name": supplier_name,
            "city_name": city_name,
            "country_alpha2": country_alpha2,
            "address_bpna": address_bpna,
        }

    def get_legal_entity_addresses(self, bpnl: str) -> list[dict[str, Any]]:
        """
        Fetch the addresses associated with one legal entity.

        Args:
                bpnl (str): The business partner number of the supplier legal entity.

        Steps:
            1. Read the inputs required to get legal entity addresses.
            2. Perform the operations needed to get legal entity addresses.
            3. Return the resulting value or update the relevant application state.

        Returns:
                list[dict]: The raw addresses associated with the legal entity.
        """
        try:
            data = self.http.get(f"/legal-entities/{bpnl}/addresses")
            return self._extract_list(data)
        except Exception as exc:
            raise BpdmLookupError(f"Failed to fetch legal-entity addresses for {bpnl}: {exc}") from exc

    def search_sites(
        self,
        bpnls: list[str] | None = None,
        bpnss: list[str] | None = None,
        participants_only: bool = False,
    ) -> list[dict[str, Any]]:
        """
        Search BPDM sites with the provided filter values.

        Args:
                bpnls (list[str] | None): The bpnls used by this method.
                bpnss (list[str] | None): The bpnss used by this method.
                participants_only (bool): The participants only used by this method.

        Steps:
            1. Read the inputs required to search sites.
            2. Perform the operations needed to search sites.
            3. Return the resulting value or update the relevant application state.

        Returns:
                list[dict]: The raw BPDM site search results.
        """
        path = "/participants/sites/search" if participants_only else "/sites/search"
        body = {
            "bpns": bpnss or [],
            "legalEntities": bpnls or [],
        }
        try:
            data = self.http.post(path, body)
            return self._extract_list(data)
        except Exception as exc:
            raise BpdmLookupError(f"Failed to search sites: {exc}") from exc

    def search_addresses(
        self,
        bpnas: list[str] | None = None,
        bpnss: list[str] | None = None,
        bpnls: list[str] | None = None,
        participants_only: bool = False,
    ) -> list[dict[str, Any]]:
        """
        Search BPDM addresses with the provided filter values.

        Args:
                bpnas (list[str] | None): The bpnas used by this method.
                bpnss (list[str] | None): The bpnss used by this method.
                bpnls (list[str] | None): The bpnls used by this method.
                participants_only (bool): The participants only used by this method.

        Steps:
            1. Read the inputs required to search addresses.
            2. Perform the operations needed to search addresses.
            3. Return the resulting value or update the relevant application state.

        Returns:
                list[dict]: The raw BPDM address search results.
        """
        path = "/participants/addresses/search" if participants_only else "/addresses/search"
        body = {
            "bpna": bpnas or [],
            "bpns": bpnss or [],
            "bpnl": bpnls or [],
        }
        try:
            data = self.http.post(path, body)
            return self._extract_list(data)
        except Exception as exc:
            raise BpdmLookupError(f"Failed to search addresses: {exc}") from exc

    def resolve_site_and_main_address(self, bpns: str) -> tuple[BpdmSite | None, BpdmAddress | None]:
        """
        Resolve a site and its main address from a BPNS value.

        Args:
                bpns (str): The business partner number of the supplier site.

        Steps:
            1. Read the inputs required to resolve site and main address.
            2. Perform the operations needed to resolve site and main address.
            3. Return the resulting value or update the relevant application state.

        Returns:
                tuple[BpdmSite | None, BpdmAddress | None]: The resolved site and its main address.
        """
        site_raw = self.get_site(bpns)
        site = self._normalize_site(site_raw)

        if site.main_address_bpna:
            address_raw = self.get_address(site.main_address_bpna)
            return site, self._normalize_address(address_raw)

        # Fallback when the site payload does not expose a BPNA directly
        address_candidates = self.search_addresses(bpnss=[bpns])
        address = self._normalize_address(address_candidates[0]) if address_candidates else None
        return site, address

    def resolve_address_by_legal_entity(self, bpnl: str) -> BpdmAddress | None:
        """
        Resolve one representative address for a legal entity.

        Args:
                bpnl (str): The business partner number of the supplier legal entity.

        Steps:
            1. Read the inputs required to resolve address by legal entity.
            2. Perform the operations needed to resolve address by legal entity.
            3. Return the resulting value or update the relevant application state.

        Returns:
                BpdmAddress | None: One representative address for the supplier legal entity.
        """
        addresses = self.get_legal_entity_addresses(bpnl)
        if not addresses:
            return None
        return self._normalize_address(addresses[0])

    @staticmethod
    def _extract_list(data: Any) -> list[dict[str, Any]]:
        """
        Extract a list-like payload section from a BPDM response.

        Args:
                data (Any): The data used by this method.

        Steps:
            1. Read the inputs required to  extract list.
            2. Perform the operations needed to  extract list.
            3. Return the resulting value or update the relevant application state.

        Returns:
                list: The extracted list value, or an empty list when no list is available.
        """
        if data is None:
            return []
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            for key in ("content", "items", "addresses", "sites", "legalEntities"):
                value = data.get(key)
                if isinstance(value, list):
                    return value
        return []

    @staticmethod
    def _find_first_string(data: dict[str, Any], *candidates: str) -> str | None:
        """
        Return the first non-empty string found in the provided values.

        Args:
                data (dict[str, Any]): The data used by this method.
                *candidates (Any): Additional positional arguments accepted by this method.

        Steps:
            1. Read the inputs required to  find first string.
            2. Perform the operations needed to  find first string.
            3. Return the resulting value or update the relevant application state.

        Returns:
                str | None: The first non-empty string found in the provided values.
        """
        for key in candidates:
            value = data.get(key)
            if isinstance(value, str) and value:
                return value
        return None

    def _normalize_site(self, data: dict[str, Any]) -> BpdmSite:
        """
        Normalize a raw BPDM site payload into a BpdmSite object.

        Args:
                data (dict[str, Any]): The data used by this method.

        Steps:
            1. Read the inputs required to  normalize site.
            2. Perform the operations needed to  normalize site.
            3. Return the resulting value or update the relevant application state.

        Returns:
                BpdmSite: The normalized site object.
        """
        main_address = data.get("mainAddress") or {}
        return BpdmSite(
            bpns=self._find_first_string(data, "bpns", "bpnsValue", "bpnS"),
            name=self._find_first_string(data, "name"),
            main_address_bpna=self._find_first_string(main_address, "bpna", "bpnA")
            or self._find_first_string(data, "mainAddressBpna"),
            legal_entity_bpnl=self._find_first_string(data, "legalEntity", "legalEntityBpn", "bpnL"),
            raw=data,
        )

    def _normalize_address(self, data: dict[str, Any]) -> BpdmAddress:
        """
        Normalize a raw BPDM address payload into a BpdmAddress object.

        Args:
                data (dict[str, Any]): The data used by this method.

        Steps:
            1. Read the inputs required to  normalize address.
            2. Perform the operations needed to  normalize address.
            3. Return the resulting value or update the relevant application state.

        Returns:
                BpdmAddress: The normalized address object.
        """
        physical = data.get("physicalPostalAddress") or data.get("postalAddress") or {}
        return BpdmAddress(
            bpna=self._find_first_string(data, "bpna", "bpnA"),
            name=self._find_first_string(data, "name"),
            street_name=self._find_first_string(physical, "streetName", "street"),
            house_number=self._find_first_string(physical, "houseNumber"),
            postal_code=self._find_first_string(physical, "zipCode", "postalCode"),
            city_name=self._find_first_string(physical, "cityName", "city"),
            country_alpha2=self._find_first_string(physical, "countryAlpha2", "countryCode"),
            raw=data,
        )
