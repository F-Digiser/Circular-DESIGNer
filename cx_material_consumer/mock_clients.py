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

from .exceptions import BpdmLookupError, DiscoveryError, DtrLookupError
from .mock_data import MOCK_BPN_DISCOVERY, MOCK_SUPPLIERS
from .models import (
    BpdmAddress,
    BpdmSite,
    MaterialLookup,
    SEMANTIC_ID_CMP,
    SEMANTIC_ID_PART_TYPE_INFORMATION,
    SEMANTIC_ID_SMC_CALCULATED,
    SEMANTIC_ID_SMC_VERIFIABLE,
)


class MockConnectorRuntime:
    """
    Provide mock connector-discovery and DTR-session behavior for local demonstrations.

    Class-Level Constants:
        None.

    Attributes:
        None.

    Methods:
        find_connector_by_bpn(): Resolve the connector endpoint for a supplier BPNL.
        open_dtr_session(): Open a connector-backed session to the supplier Digital Twin Registry.
    """
    def find_connector_by_bpn(self, bpnl: str) -> str:
        """
        Resolve the connector endpoint for a supplier BPNL.

        Args:
                bpnl (str): The business partner number of the supplier legal entity.

        Steps:
            1. Read the inputs required to find connector by bpn.
            2. Perform the operations needed to find connector by bpn.
            3. Return the resulting value or update the relevant application state.

        Returns:
                str: The connector endpoint associated with the supplier BPNL.
        """
        if bpnl not in MOCK_SUPPLIERS:
            raise DiscoveryError(f"No mock connector found for {bpnl}")
        return f"mock://connector/{bpnl}"

    def open_dtr_session(self, supplier_bpnl: str, supplier_dsp_endpoint: str) -> tuple[str, str]:
        """
        Open a connector-backed session to the supplier Digital Twin Registry.

        Args:
                supplier_bpnl (str): The optional supplier BPNL used to skip supplier discovery or disambiguate results.
                supplier_dsp_endpoint (str): The supplier dsp endpoint used by this method.

        Steps:
            1. Read the inputs required to open dtr session.
            2. Perform the operations needed to open dtr session.
            3. Return the resulting value or update the relevant application state.

        Returns:
                tuple[str, str]: The DTR dataplane URL and access token for the opened session.
        """
        if supplier_bpnl not in MOCK_SUPPLIERS:
            raise DiscoveryError(f"No mock DTR session available for {supplier_bpnl}")
        return f"mock://dtr/{supplier_bpnl}", "mock-access-token"


class MockBpnDiscoveryClient:
    """
    Provide mock supplier resolution results for local demonstrations.

    Class-Level Constants:
        None.

    Attributes:
        None.

    Methods:
        resolve_bpnls_by_material_number(): Resolve candidate supplier BPNLs for a supplier material number.
    """
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
        candidates = MOCK_BPN_DISCOVERY.get(material_number)
        if not candidates:
            raise DiscoveryError(f"No BPNL found via mock BPN Discovery for material number {material_number}")
        return list(candidates)


class MockBpdmPoolClient:
    """
    Provide mock BPDM records for local demonstrations.

    Class-Level Constants:
        None.

    Attributes:
        None.

    Methods:
        _supplier(): Return the mock supplier record for a BPNL.
        get_site(): Fetch one site record from BPDM.
        get_address(): Fetch one address record from BPDM.
        get_legal_entity(): Fetch one legal-entity record from BPDM.
        describe_supplier_candidate(): Build a user-facing supplier candidate description from BPDM data.
        get_legal_entity_addresses(): Fetch the addresses associated with one legal entity.
        search_sites(): Search BPDM sites with the provided filter values.
        search_addresses(): Search BPDM addresses with the provided filter values.
        resolve_site_and_main_address(): Resolve a site and its main address from a BPNS value.
        resolve_address_by_legal_entity(): Resolve one representative address for a legal entity.
    """
    def _supplier(self, bpnl: str) -> dict[str, Any]:
        """
        Return the mock supplier record for a BPNL.

        Args:
                bpnl (str): The business partner number of the supplier legal entity.

        Steps:
            1. Read the inputs required to  supplier.
            2. Perform the operations needed to  supplier.
            3. Return the resulting value or update the relevant application state.

        Returns:
                dict: The mock supplier record for the provided BPNL.
        """
        supplier = MOCK_SUPPLIERS.get(bpnl)
        if not supplier:
            raise BpdmLookupError(f"Unknown mock supplier {bpnl}")
        return supplier

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
        for supplier in MOCK_SUPPLIERS.values():
            if bpns in supplier["sites"]:
                return supplier["sites"][bpns]
        raise BpdmLookupError(f"Unknown mock site {bpns}")

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
        for supplier in MOCK_SUPPLIERS.values():
            if bpna in supplier["addresses"]:
                return supplier["addresses"][bpna]
        raise BpdmLookupError(f"Unknown mock address {bpna}")

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
        return self._supplier(bpnl)["legal_entity"]

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
        supplier = self._supplier(bpnl)
        return {
            "bpnl": bpnl,
            "supplier_name": supplier.get("supplier_name"),
            "city_name": supplier.get("city_name"),
            "country_alpha2": supplier.get("country_alpha2"),
            "address_bpna": supplier.get("address_bpna"),
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
        supplier = self._supplier(bpnl)
        return list(supplier["addresses"].values())

    def search_sites(self, bpnls: list[str] | None = None, bpnss: list[str] | None = None, participants_only: bool = False) -> list[dict[str, Any]]:
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
        results: list[dict[str, Any]] = []
        for bpnl, supplier in MOCK_SUPPLIERS.items():
            if bpnls and bpnl not in bpnls:
                continue
            for key, site in supplier["sites"].items():
                if bpnss and key not in bpnss:
                    continue
                results.append(site)
        return results

    def search_addresses(self, bpnas: list[str] | None = None, bpnss: list[str] | None = None, bpnls: list[str] | None = None, participants_only: bool = False) -> list[dict[str, Any]]:
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
        results: list[dict[str, Any]] = []
        for bpnl, supplier in MOCK_SUPPLIERS.items():
            if bpnls and bpnl not in bpnls:
                continue
            sites = supplier["sites"]
            addresses = supplier["addresses"]
            allowed_bpnas = set(bpnas or []) if bpnas else None
            if bpnss:
                allowed_bpnas = set(allowed_bpnas or set())
                for bpns in bpnss:
                    site = sites.get(bpns)
                    if site:
                        main = ((site.get("mainAddress") or {}).get("bpna"))
                        if main:
                            allowed_bpnas.add(main)
            for addr_id, address in addresses.items():
                if allowed_bpnas is not None and addr_id not in allowed_bpnas:
                    continue
                results.append(address)
        return results

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
        address_bpna = ((site_raw.get("mainAddress") or {}).get("bpna"))
        address_raw = self.get_address(address_bpna) if address_bpna else None
        site = BpdmSite(
            bpns=site_raw.get("bpns"),
            name=site_raw.get("name"),
            main_address_bpna=address_bpna,
            legal_entity_bpnl=site_raw.get("legalEntity"),
            raw=site_raw,
        )
        address = None
        if address_raw:
            physical = address_raw.get("physicalPostalAddress") or {}
            address = BpdmAddress(
                bpna=address_raw.get("bpna"),
                name=address_raw.get("name"),
                street_name=physical.get("streetName"),
                house_number=physical.get("houseNumber"),
                postal_code=physical.get("zipCode"),
                city_name=physical.get("cityName"),
                country_alpha2=physical.get("countryAlpha2"),
                raw=address_raw,
            )
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
        address_raw = addresses[0]
        physical = address_raw.get("physicalPostalAddress") or {}
        return BpdmAddress(
            bpna=address_raw.get("bpna"),
            name=address_raw.get("name"),
            street_name=physical.get("streetName"),
            house_number=physical.get("houseNumber"),
            postal_code=physical.get("zipCode"),
            city_name=physical.get("cityName"),
            country_alpha2=physical.get("countryAlpha2"),
            raw=address_raw,
        )


class MockDtrClient:
    """
    Provide mock DTR shell and submodel responses for local demonstrations.

    Class-Level Constants:
        None.

    Attributes:
        supplier (Any): Stores the supplier value.
        bpnl (Any): Stores the bpnl value.

    Methods:
        __init__(): Initialize the object with the provided dependencies, default values, and internal state.
        _material_by_shell(): Return the mock material record that belongs to one shell identifier.
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
        try:
            self.bpnl = dataplane_url.rstrip("/").split("/")[-1]
        except Exception as exc:
            raise DtrLookupError(f"Invalid mock dataplane URL: {dataplane_url}") from exc
        self.supplier = MOCK_SUPPLIERS.get(self.bpnl)
        if not self.supplier:
            raise DtrLookupError(f"Unknown mock supplier for dataplane URL {dataplane_url}")

    def _material_by_shell(self, aas_id: str) -> dict[str, Any]:
        """
        Return the mock material record that belongs to one shell identifier.

        Args:
                aas_id (str): The shell identifier whose descriptor or submodel should be read.

        Steps:
            1. Read the inputs required to  material by shell.
            2. Perform the operations needed to  material by shell.
            3. Return the resulting value or update the relevant application state.

        Returns:
                dict: The mock material record associated with the shell identifier.
        """
        for material in self.supplier["materials"].values():
            if material.get("shell_id") == aas_id:
                return material
        raise DtrLookupError(f"Unknown mock shell descriptor {aas_id}")

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
        kv = {item.get("key"): item.get("value") for item in specific_asset_ids}
        lifecycle = kv.get("assetLifecyclePhase")
        if lifecycle == "AsPlanned":
            mpid = kv.get("manufacturerPartId")
            material = self.supplier["materials"].get(mpid or "")
            return [material["shell_id"]] if material else []
        if lifecycle == "AsBuilt":
            pid = kv.get("partInstanceId")
            if pid:
                return [f"aas-built-{pid}"]
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
        material = self._material_by_shell(aas_id)
        endpoints = []
        endpoints.append({
            "idShort": "partTypeInformation",
            "interface": "SUBMODEL-VALUE-3.1",
            "semanticId": {"keys": [{"value": SEMANTIC_ID_PART_TYPE_INFORMATION}]},
            "endpoints": [{"protocolInformation": {"href": f"mock://submodel/{self.bpnl}/{material['part_type_information']['manufacturerPartId']}/part-type-information"}}],
        })
        endpoints.append({
            "idShort": "smc",
            "interface": "SUBMODEL-VALUE-3.1",
            "semanticId": {"keys": [{"value": SEMANTIC_ID_SMC_CALCULATED}]},
            "endpoints": [{"protocolInformation": {"href": f"mock://submodel/{self.bpnl}/{material['part_type_information']['manufacturerPartId']}/smc"}}],
        })
        if material.get("cmp") is not None:
            endpoints.append({
                "idShort": "cmp",
                "interface": "SUBMODEL-VALUE-3.1",
                "semanticId": {"keys": [{"value": SEMANTIC_ID_CMP}]},
                "endpoints": [{"protocolInformation": {"href": f"mock://submodel/{self.bpnl}/{material['part_type_information']['manufacturerPartId']}/cmp"}}],
            })
        return {"id": aas_id, "submodelDescriptors": endpoints}

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
        href = submodel_descriptor["endpoints"][0]["protocolInformation"]["href"]
        try:
            _, _, bpnl, material_number, artifact = href.split("/")[-5:]
        except Exception as exc:
            raise DtrLookupError(f"Invalid mock submodel href {href}") from exc
        supplier = MOCK_SUPPLIERS.get(bpnl)
        if not supplier:
            raise DtrLookupError(f"Unknown mock supplier {bpnl}")
        material = supplier["materials"].get(material_number)
        if not material:
            raise DtrLookupError(f"Unknown mock material {material_number} for {bpnl}")
        if artifact == "part-type-information":
            return material["part_type_information"]
        if artifact == "smc":
            return material["smc"]
        if artifact == "cmp":
            if material.get("cmp") is None:
                raise DtrLookupError("CMP submodel not available in mock data")
            return material["cmp"]
        raise DtrLookupError(f"Unknown mock artifact {artifact}")

    def iter_shell_descriptors(self, shell_ids: list[str]):
        """
        Iterate over shell descriptors for the provided shell identifiers.

        Args:
                shell_ids (list[str]): The shell identifiers to inspect.

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
        return self.search_shell_ids_by_asset_link([
            {"key": "manufacturerPartId", "value": manufacturer_part_id},
            {"key": "assetLifecyclePhase", "value": "AsPlanned"},
        ])

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
        return self.search_shell_ids_by_asset_link([
            {"key": "partInstanceId", "value": part_instance_id},
            {"key": "assetLifecyclePhase", "value": "AsBuilt"},
        ])

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
            semantic_id = SEMANTIC_ID_SMC_CALCULATED
        else:
            shell_ids = self.get_built_part_shell_ids(lookup.part_instance_id or "")
            semantic_id = SEMANTIC_ID_SMC_VERIFIABLE
            # Mock AsBuilt reuses planned SMC shape for simplicity.
        if not shell_ids:
            raise DtrLookupError("No shell found for SMC lookup")
        try:
            payload = self.get_submodel_value_from_shells(shell_ids, semantic_id if lookup.lifecycle == "AsBuilt" else semantic_id)
        except DtrLookupError:
            if lookup.lifecycle == "AsBuilt":
                # fallback for the mock built flow
                payload = {"secondaryMaterialContent": [{"secondaryMaterialContentPercentage": 22.0}]}
            else:
                raise
        return semantic_id, payload

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
