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

from typing import Any, Iterable

import requests

from .exceptions import DtrLookupError
from .models import (
    MaterialLookup,
    SEMANTIC_ID_CMP,
    SEMANTIC_ID_PART_TYPE_INFORMATION,
    SEMANTIC_ID_SMC_CALCULATED,
    SEMANTIC_ID_SMC_VERIFIABLE,
)


class DtrClient:
    """
    Provide helper methods for searching shells and retrieving submodel payloads from a Digital Twin Registry session.

    Class-Level Constants:
        None.

    Attributes:
        dataplane_url (str): Stores the dataplane url value.
        headers (Any): Stores the headers value.
        asset_link_search_path (str): Stores the asset link search path value.
        timeout (int): Stores the timeout value.

    Methods:
        __init__(): Initialize the object with the provided dependencies, default values, and internal state.
        search_shell_ids_by_asset_link(): Search the DTR for shell identifiers that match the provided asset-link filters.
        get_shell_descriptor(): Fetch one shell descriptor from the DTR.
        extract_semantic_id(): Extract the semantic identifier from a submodel descriptor.
        find_submodel_descriptor(): Find the submodel descriptor matching a requested semantic identifier.
        fetch_submodel_value(): Fetch the JSON value payload for one submodel descriptor.
        iter_shell_descriptors(): Iterate over shell descriptors for the provided shell identifiers.
        get_submodel_value_from_shells(): Return the first matching submodel value from a list of shells.
        get_planned_part_shell_ids(): Resolve shell identifiers for a planned part lookup.
        get_built_part_shell_ids(): Resolve shell identifiers for a built-part lookup.
        get_part_type_information(): Fetch the PartTypeInformation payload for a supplier material number.
        get_smc(): Fetch the appropriate secondary material content payload for the current lookup.
        get_cmp_by_aas_id(): Fetch the Chemical Material Passport payload for a fixed shell identifier.
    """
    def __init__(self, dataplane_url: str, access_token: str, asset_link_search_path: str, timeout: int = 30) -> None:
        """
        Initialize the object with the provided dependencies, default values, and internal state.

        Args:
                dataplane_url (str): The dataplane url used by this method.
                access_token (str): The access token used by this method.
                asset_link_search_path (str): The asset link search path used by this method.
                timeout (int): The timeout used by this method.

        Steps:
            1. Read the provided dependencies and configuration values.
            2. Store them on the instance for later use.
            3. Prepare any internal state required by later method calls.

        Returns:
                None: This initializer configures the instance state in place.
        """
        self.dataplane_url = dataplane_url.rstrip("/")
        self.headers = {"Authorization": f"Bearer {access_token}"}
        self.asset_link_search_path = asset_link_search_path
        self.timeout = timeout

    def search_shell_ids_by_asset_link(self, specific_asset_ids: list[dict[str, str]]) -> list[str]:
        """
        Search the DTR for shell identifiers that match the provided asset-link filters.

        Args:
                specific_asset_ids (list[dict[str, str]]): The specific asset ids used by this method.

        Steps:
            1. Build the DTR search request from the provided asset-link filters.
            2. Send the search request to the DTR session.
            3. Return the matching shell identifiers.

        Returns:
                list[str]: The shell identifiers returned by the DTR search.
        """
        body = {"assetIds": specific_asset_ids}
        try:
            response = requests.post(
                f"{self.dataplane_url}{self.asset_link_search_path}",
                json=body,
                headers={**self.headers, "Content-Type": "application/json"},
                timeout=self.timeout,
            )
            response.raise_for_status()
            data = response.json()
        except Exception as exc:
            raise DtrLookupError(f"Asset-link search failed: {exc}") from exc

        if isinstance(data, list):
            return [str(x) for x in data]
        if isinstance(data, dict):
            for key in ("result", "items", "shellIds"):
                value = data.get(key)
                if isinstance(value, list):
                    return [str(x) for x in value]
        return []

    def get_shell_descriptor(self, aas_id: str) -> dict[str, Any]:
        """
        Fetch one shell descriptor from the DTR.

        Args:
                aas_id (str): The shell identifier whose descriptor or submodel should be read.

        Steps:
            1. Read the inputs required to get shell descriptor.
            2. Perform the operations needed to get shell descriptor.
            3. Return the resulting value or update the relevant application state.

        Returns:
                dict: The shell descriptor payload.
        """
        try:
            response = requests.get(
                f"{self.dataplane_url}/shell-descriptors/{aas_id}",
                headers=self.headers,
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response.json()
        except Exception as exc:
            raise DtrLookupError(f"Failed to fetch shell descriptor {aas_id}: {exc}") from exc

    @staticmethod
    def extract_semantic_id(submodel_descriptor: dict[str, Any]) -> str | None:
        """
        Extract the semantic identifier from a submodel descriptor.

        Args:
                submodel_descriptor (dict[str, Any]): The submodel descriptor whose value payload should be fetched.

        Steps:
            1. Read the inputs required to extract semantic id.
            2. Perform the operations needed to extract semantic id.
            3. Return the resulting value or update the relevant application state.

        Returns:
                str | None: The semantic identifier extracted from the submodel descriptor.
        """
        try:
            return submodel_descriptor["semanticId"]["keys"][0]["value"]
        except Exception:
            return None

    def find_submodel_descriptor(self, shell_descriptor: dict[str, Any], semantic_id: str) -> dict[str, Any] | None:
        """
        Find the submodel descriptor matching a requested semantic identifier.

        Args:
                shell_descriptor (dict[str, Any]): The shell descriptor that contains the submodel metadata.
                semantic_id (str): The semantic identifier of the submodel to retrieve.

        Steps:
            1. Read the inputs required to find submodel descriptor.
            2. Perform the operations needed to find submodel descriptor.
            3. Return the resulting value or update the relevant application state.

        Returns:
                dict | None: The matching submodel descriptor, if one is found.
        """
        for submodel in shell_descriptor.get("submodelDescriptors", []):
            if self.extract_semantic_id(submodel) == semantic_id:
                return submodel
        return None

    def fetch_submodel_value(self, submodel_descriptor: dict[str, Any]) -> dict[str, Any]:
        """
        Fetch the JSON value payload for one submodel descriptor.

        Args:
                submodel_descriptor (dict[str, Any]): The submodel descriptor whose value payload should be fetched.

        Steps:
            1. Read the endpoint metadata from the submodel descriptor.
            2. Build the correct value URL for the requested interface type.
            3. Fetch and return the JSON value payload.

        Returns:
                dict: The fetched submodel value payload.
        """
        endpoint = submodel_descriptor["endpoints"][0]
        href = endpoint["protocolInformation"]["href"]
        interface = endpoint.get("interface")

        if interface != "SUBMODEL-VALUE-3.1":
            href = href.rstrip("/") + "/$value"

        try:
            response = requests.get(href, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except Exception as exc:
            raise DtrLookupError(f"Failed to fetch submodel value from {href}: {exc}") from exc

    def iter_shell_descriptors(self, shell_ids: Iterable[str]) -> Iterable[tuple[str, dict[str, Any]]]:
        """
        Iterate over shell descriptors for the provided shell identifiers.

        Args:
                shell_ids (Iterable[str]): The shell identifiers to inspect.

        Steps:
            1. Read the inputs required to iter shell descriptors.
            2. Perform the operations needed to iter shell descriptors.
            3. Return the resulting value or update the relevant application state.

        Returns:
                Iterator[dict]: An iterator over the resolved shell descriptor payloads.
        """
        for aas_id in shell_ids:
            yield aas_id, self.get_shell_descriptor(aas_id)

    def get_submodel_value_from_shells(self, shell_ids: list[str], semantic_id: str) -> dict[str, Any]:
        """
        Return the first matching submodel value from a list of shells.

        Args:
                shell_ids (list[str]): The shell identifiers to inspect.
                semantic_id (str): The semantic identifier of the submodel to retrieve.

        Steps:
            1. Read the inputs required to get submodel value from shells.
            2. Perform the operations needed to get submodel value from shells.
            3. Return the resulting value or update the relevant application state.

        Returns:
                dict: The first matching submodel value payload.
        """
        for _, descriptor in self.iter_shell_descriptors(shell_ids):
            submodel = self.find_submodel_descriptor(descriptor, semantic_id)
            if submodel:
                return self.fetch_submodel_value(submodel)
        raise DtrLookupError(f"No submodel found for semantic ID {semantic_id}")

    def get_planned_part_shell_ids(self, manufacturer_part_id: str) -> list[str]:
        """
        Resolve shell identifiers for a planned part lookup.

        Args:
                manufacturer_part_id (str): The manufacturer part id used by this method.

        Steps:
            1. Read the inputs required to get planned part shell ids.
            2. Perform the operations needed to get planned part shell ids.
            3. Return the resulting value or update the relevant application state.

        Returns:
                list[str]: The shell identifiers for the planned-part lookup.
        """
        return self.search_shell_ids_by_asset_link(
            [
                {"key": "manufacturerPartId", "value": manufacturer_part_id},
                {"key": "assetLifecyclePhase", "value": "AsPlanned"},
            ]
        )

    def get_built_part_shell_ids(self, part_instance_id: str) -> list[str]:
        """
        Resolve shell identifiers for a built-part lookup.

        Args:
                part_instance_id (str): The part instance id used by this method.

        Steps:
            1. Read the inputs required to get built part shell ids.
            2. Perform the operations needed to get built part shell ids.
            3. Return the resulting value or update the relevant application state.

        Returns:
                list[str]: The shell identifiers for the built-part lookup.
        """
        return self.search_shell_ids_by_asset_link(
            [
                {"key": "partInstanceId", "value": part_instance_id},
                {"key": "assetLifecyclePhase", "value": "AsBuilt"},
            ]
        )

    def get_part_type_information(self, manufacturer_part_id: str) -> dict[str, Any]:
        """
        Fetch the PartTypeInformation payload for a supplier material number.

        Args:
                manufacturer_part_id (str): The manufacturer part id used by this method.

        Steps:
            1. Read the inputs required to get part type information.
            2. Perform the operations needed to get part type information.
            3. Return the resulting value or update the relevant application state.

        Returns:
                dict: The resolved PartTypeInformation payload.
        """
        shell_ids = self.get_planned_part_shell_ids(manufacturer_part_id)
        if not shell_ids:
            raise DtrLookupError("No shell found for Part Type lookup")
        return self.get_submodel_value_from_shells(shell_ids, SEMANTIC_ID_PART_TYPE_INFORMATION)

    def get_smc(self, lookup: MaterialLookup) -> tuple[str, dict[str, Any]]:
        """
        Fetch the appropriate secondary material content payload for the current lookup.

        Args:
                lookup (MaterialLookup): The lookup model describing the identifiers and lifecycle to resolve.

        Steps:
            1. Read the inputs required to get smc.
            2. Perform the operations needed to get smc.
            3. Return the resulting value or update the relevant application state.

        Returns:
                dict: The resolved secondary material content payload.
        """
        lookup.validate()
        if lookup.lifecycle == "AsPlanned":
            shell_ids = self.get_planned_part_shell_ids(lookup.manufacturer_part_id or "")
            wanted_semantic_id = SEMANTIC_ID_SMC_CALCULATED
        else:
            shell_ids = self.get_built_part_shell_ids(lookup.part_instance_id or "")
            wanted_semantic_id = SEMANTIC_ID_SMC_VERIFIABLE

        if not shell_ids:
            raise DtrLookupError("No shell found for SMC lookup")

        try:
            return wanted_semantic_id, self.get_submodel_value_from_shells(shell_ids, wanted_semantic_id)
        except DtrLookupError as exc:
            raise DtrLookupError(f"No SMC submodel found for semantic ID {wanted_semantic_id}") from exc

    def get_cmp_by_aas_id(self, aas_id: str) -> dict[str, Any]:
        """
        Fetch the Chemical Material Passport payload for a fixed shell identifier.

        Args:
                aas_id (str): The shell identifier whose descriptor or submodel should be read.

        Steps:
            1. Read the inputs required to get cmp by aas id.
            2. Perform the operations needed to get cmp by aas id.
            3. Return the resulting value or update the relevant application state.

        Returns:
                dict: The resolved Chemical Material Passport payload.
        """
        descriptor = self.get_shell_descriptor(aas_id)
        submodel = self.find_submodel_descriptor(descriptor, SEMANTIC_ID_CMP)
        if not submodel:
            raise DtrLookupError(f"CMP submodel not found on shell {aas_id}")
        return self.fetch_submodel_value(submodel)
