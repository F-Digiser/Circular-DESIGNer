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

from typing import Callable, Any

from .bpdm_pool import BpdmPoolClient
from .bpn_discovery import BpnDiscoveryClient
from .cmp_adapters import build_cmp_adapter
from .connector import ConnectorRuntime
from .dtr import DtrClient
from .exceptions import DiscoveryError
from .models import (
    MaterialLookup,
    MaterialProfile,
    SupplierRef,
    SupplierSelectionCandidate,
    SupplierSelectionRequired,
)


class MaterialConsumerService:
    """
    Coordinate supplier resolution, connector access, DTR lookups, BPDM enrichment, and profile construction for material imports.

    Class-Level Constants:
        None.

    Attributes:
        connector_runtime (ConnectorRuntime): Stores the connector runtime value.
        bpdm_pool_client (BpdmPoolClient): Stores the bpdm pool client value.
        dtr_asset_link_search_path (str): Stores the dtr asset link search path value.
        dtr_timeout_seconds (int): Stores the dtr timeout seconds value.
        cmp_lookup_adapter (Any): Stores the cmp lookup adapter value.
        bpn_discovery_client (BpnDiscoveryClient | None): Stores the bpn discovery client value.
        dtr_client_factory (Callable[[str, str, str, int], Any]): Stores the dtr client factory value.

    Methods:
        __init__(): Initialize the object with the provided dependencies, default values, and internal state.
        _build_supplier_selection(): Build the supplier-selection response shown when a material number matches multiple BPNLs.
        resolve_supplier_bpnl(): Resolve the supplier BPNL from the user input or from BPN discovery.
        _extract_material_name(): Extract the material name from a PartTypeInformation payload.
        _extract_candidate_site_bpnss(): Extract candidate planned site BPNS values from a PartTypeInformation payload.
        get_material_profile(): Resolve the complete material profile for a supplier and lookup model.
        get_profile_for_supplier_material_number(): Resolve a material profile starting from a supplier material number and optional supplier information.
    """
    def __init__(
        self,
        connector_runtime: ConnectorRuntime,
        bpdm_pool_client: BpdmPoolClient,
        dtr_asset_link_search_path: str,
        dtr_timeout_seconds: int,
        cmp_lookup_mode: str,
        cmp_fixed_aas_id: str | None,
        bpn_discovery_client: BpnDiscoveryClient | None = None,
        dtr_client_factory: Callable[[str, str, str, int], Any] = DtrClient,
    ) -> None:
        """
        Initialize the object with the provided dependencies, default values, and internal state.

        Args:
                connector_runtime (ConnectorRuntime): The connector runtime used by this method.
                bpdm_pool_client (BpdmPoolClient): The bpdm pool client used by this method.
                dtr_asset_link_search_path (str): The dtr asset link search path used by this method.
                dtr_timeout_seconds (int): The dtr timeout seconds used by this method.
                cmp_lookup_mode (str): The cmp lookup mode used by this method.
                cmp_fixed_aas_id (str | None): The cmp fixed aas id used by this method.
                bpn_discovery_client (BpnDiscoveryClient | None): The bpn discovery client used by this method.
                dtr_client_factory (Callable[[str, str, str, int], Any]): The dtr client factory used by this method.

        Steps:
            1. Read the provided dependencies and configuration values.
            2. Store them on the instance for later use.
            3. Prepare any internal state required by later method calls.

        Returns:
                None: This initializer configures the instance state in place.
        """
        self.connector_runtime = connector_runtime
        self.bpdm_pool_client = bpdm_pool_client
        self.dtr_asset_link_search_path = dtr_asset_link_search_path
        self.dtr_timeout_seconds = dtr_timeout_seconds
        self.cmp_lookup_adapter = build_cmp_adapter(cmp_lookup_mode, cmp_fixed_aas_id)
        self.bpn_discovery_client = bpn_discovery_client
        self.dtr_client_factory = dtr_client_factory

    def _build_supplier_selection(
        self,
        supplier_material_number: str,
        candidates: list[str],
        provided_supplier_bpnl: str | None = None,
        mismatch: bool = False,
    ) -> SupplierSelectionRequired:
        """
        Build the supplier-selection response shown when a material number matches multiple BPNLs.

        Args:
                supplier_material_number (str): The supplier material number entered by the user for the lookup.
                candidates (list[str]): The supplier candidates to display or process.
                provided_supplier_bpnl (str | None): The provided supplier bpnl used by this method.
                mismatch (bool): The mismatch used by this method.

        Steps:
            1. Read the inputs required to  build supplier selection.
            2. Perform the operations needed to  build supplier selection.
            3. Return the resulting value or update the relevant application state.

        Returns:
                SupplierSelectionRequired: The selection state returned to the user interface.
        """
        enriched: list[SupplierSelectionCandidate] = []
        for bpnl in candidates:
            try:
                details = self.bpdm_pool_client.describe_supplier_candidate(bpnl)
            except Exception:
                details = {"bpnl": bpnl}
            enriched.append(
                SupplierSelectionCandidate(
                    bpnl=details.get("bpnl", bpnl),
                    supplier_name=details.get("supplier_name"),
                    city_name=details.get("city_name"),
                    country_alpha2=details.get("country_alpha2"),
                    address_bpna=details.get("address_bpna"),
                )
            )

        message = (
            "Multiple supplier companies were found for the provided material number. "
            "Please choose one supplier and resubmit its BPNL."
        )
        if mismatch and provided_supplier_bpnl:
            message = (
                "The provided supplier BPNL did not match the supplier companies returned by BPN Discovery. "
                "Please choose one of the listed suppliers and resubmit its BPNL."
            )

        return SupplierSelectionRequired(
            supplier_material_number=supplier_material_number,
            message=message,
            candidates=enriched,
            provided_supplier_bpnl=provided_supplier_bpnl,
        )

    def resolve_supplier_bpnl(
        self,
        supplier_material_number: str,
        supplier_bpnl: str | None = None,
    ) -> tuple[str, str] | SupplierSelectionRequired:
        """
        Resolve the supplier BPNL from the user input or from BPN discovery.

        Args:
                supplier_material_number (str): The supplier material number entered by the user for the lookup.
                supplier_bpnl (str | None): The optional supplier BPNL used to skip supplier discovery or disambiguate results.

        Steps:
            1. Check whether the caller already provided a supplier BPNL.
            2. Use BPN discovery when the supplier still needs to be resolved.
            3. Return either one resolved supplier or a selection state for the user interface.

        Returns:
                tuple[str, str, SupplierSelectionRequired | None]: The resolved BPNL, its source label, and an optional selection state.
        """
        if self.bpn_discovery_client is not None:
            try:
                candidates = self.bpn_discovery_client.resolve_bpnls_by_material_number(supplier_material_number)
            except DiscoveryError:
                if supplier_bpnl:
                    return supplier_bpnl, "provided"
                raise

            if supplier_bpnl:
                if supplier_bpnl in candidates:
                    return supplier_bpnl, "provided+verified-by-bpn-discovery"
                if len(candidates) > 1:
                    return self._build_supplier_selection(
                        supplier_material_number=supplier_material_number,
                        candidates=candidates,
                        provided_supplier_bpnl=supplier_bpnl,
                        mismatch=True,
                    )
                raise DiscoveryError(
                    "Provided supplier BPNL does not match the single BPN Discovery candidate for material number "
                    f"{supplier_material_number}: {', '.join(candidates)}"
                )
            if len(candidates) == 1:
                return candidates[0], "bpn-discovery"
            return self._build_supplier_selection(
                supplier_material_number=supplier_material_number,
                candidates=candidates,
                provided_supplier_bpnl=supplier_bpnl,
            )

        if supplier_bpnl:
            return supplier_bpnl, "provided"

        raise DiscoveryError("No supplier BPNL provided and no BPN Discovery client configured.")

    @staticmethod
    def _extract_material_name(part_type_information_payload: dict | None) -> str | None:
        """
        Extract the material name from a PartTypeInformation payload.

        Args:
                part_type_information_payload (dict | None): The part type information payload used by this method.

        Steps:
            1. Read the inputs required to  extract material name.
            2. Perform the operations needed to  extract material name.
            3. Return the resulting value or update the relevant application state.

        Returns:
                str | None: The extracted material name.
        """
        if not isinstance(part_type_information_payload, dict):
            return None
        info = part_type_information_payload.get("partTypeInformation")
        if isinstance(info, dict):
            value = info.get("nameAtManufacturer")
            if isinstance(value, str) and value:
                return value
        return None

    @staticmethod
    def _extract_candidate_site_bpnss(part_type_information_payload: dict | None) -> list[str]:
        """
        Extract candidate planned site BPNS values from a PartTypeInformation payload.

        Args:
                part_type_information_payload (dict | None): The part type information payload used by this method.

        Steps:
            1. Read the inputs required to  extract candidate site bpnss.
            2. Perform the operations needed to  extract candidate site bpnss.
            3. Return the resulting value or update the relevant application state.

        Returns:
                list[str]: The candidate planned site BPNS values.
        """
        if not isinstance(part_type_information_payload, dict):
            return []
        entries = part_type_information_payload.get("partSitesInformationAsPlanned")
        if not isinstance(entries, list):
            return []

        def rank(entry: dict) -> int:
            function = str(entry.get("function", "")).strip().lower()
            if function == "production":
                return 0
            if function == "warehouse":
                return 1
            if function == "spare part warehouse":
                return 2
            return 9

        result: list[str] = []
        seen: set[str] = set()
        for entry in sorted([e for e in entries if isinstance(e, dict)], key=rank):
            bpns = entry.get("catenaXsiteId")
            if isinstance(bpns, str) and bpns and bpns not in seen:
                result.append(bpns)
                seen.add(bpns)
        return result

    def get_material_profile(self, supplier: SupplierRef, lookup: MaterialLookup) -> MaterialProfile:
        """
        Resolve the complete material profile for a supplier and lookup model.

        Args:
                supplier (SupplierRef): The supplier context used for connector and BPDM lookups.
                lookup (MaterialLookup): The lookup model describing the identifiers and lifecycle to resolve.

        Steps:
            1. Validate the lookup model and resolve the supplier connector.
            2. Read DTR submodels and optional BPDM enrichment data.
            3. Assemble and return the final material profile object.

        Returns:
                MaterialProfile: The fully resolved material profile.
        """
        lookup.validate()

        supplier_dsp = self.connector_runtime.find_connector_by_bpn(supplier.bpnl)
        dataplane_url, access_token = self.connector_runtime.open_dtr_session(supplier.bpnl, supplier_dsp)
        dtr = self.dtr_client_factory(
            dataplane_url,
            access_token,
            self.dtr_asset_link_search_path,
            self.dtr_timeout_seconds,
        )

        part_type_information_payload = None
        material_name = None
        candidate_site_bpnss: list[str] = []

        if lookup.lifecycle == "AsPlanned" and lookup.manufacturer_part_id:
            try:
                part_type_information_payload = dtr.get_part_type_information(lookup.manufacturer_part_id)
                material_name = self._extract_material_name(part_type_information_payload)
                candidate_site_bpnss = self._extract_candidate_site_bpnss(part_type_information_payload)
            except Exception:
                part_type_information_payload = None
                material_name = None
                candidate_site_bpnss = []

        smc_semantic_id, smc_payload = dtr.get_smc(lookup)

        try:
            cmp_payload = self.cmp_lookup_adapter.get_cmp(dtr, lookup)
        except Exception:
            cmp_payload = None

        site_dict = None
        address_dict = None
        resolved_site_bpns = lookup.site_bpns or (candidate_site_bpnss[0] if candidate_site_bpnss else None)
        address_bpna = None

        if resolved_site_bpns:
            site, address = self.bpdm_pool_client.resolve_site_and_main_address(resolved_site_bpns)
            site_dict = site.raw if site else None
            address_dict = address.raw if address else None
            address_bpna = address.bpna if address else None
        else:
            address = self.bpdm_pool_client.resolve_address_by_legal_entity(supplier.bpnl)
            address_dict = address.raw if address else None
            address_bpna = address.bpna if address else None

        return MaterialProfile(
            supplier_bpnl=supplier.bpnl,
            supplier_bpnl_source="provided",
            supplier_site_bpns=resolved_site_bpns,
            supplier_address_bpna=address_bpna,
            manufacturer_part_id=lookup.manufacturer_part_id,
            part_instance_id=lookup.part_instance_id,
            lifecycle=lookup.lifecycle,
            material_name=material_name,
            part_type_information_payload=part_type_information_payload,
            candidate_site_bpnss=candidate_site_bpnss,
            smc_semantic_id=smc_semantic_id,
            smc_payload=smc_payload,
            cmp_payload=cmp_payload,
            bpdm_site=site_dict,
            bpdm_address=address_dict,
        )

    def get_profile_for_supplier_material_number(
        self,
        supplier_material_number: str,
        supplier_bpnl: str | None = None,
        site_bpns: str | None = None,
    ) -> MaterialProfile | SupplierSelectionRequired:
        """
        Resolve a material profile starting from a supplier material number and optional supplier information.

        Args:
                supplier_material_number (str): The supplier material number entered by the user for the lookup.
                supplier_bpnl (str | None): The optional supplier BPNL used to skip supplier discovery or disambiguate results.
                site_bpns (str | None): The optional supplier site BPNS used for address enrichment.

        Steps:
            1. Translate the supplier material number into a planned-part lookup model.
            2. Resolve the supplier BPNL when necessary.
            3. Return the resulting material profile or a supplier-selection request.

        Returns:
                MaterialProfile | SupplierSelectionRequired: The resolved profile or a supplier-selection request.
        """
        resolved = self.resolve_supplier_bpnl(
            supplier_material_number=supplier_material_number,
            supplier_bpnl=supplier_bpnl,
        )
        if isinstance(resolved, SupplierSelectionRequired):
            return resolved
        resolved_bpnl, bpnl_source = resolved
        supplier = SupplierRef(bpnl=resolved_bpnl)
        lookup = MaterialLookup(
            lifecycle="AsPlanned",
            manufacturer_part_id=supplier_material_number,
            site_bpns=site_bpns,
        )
        profile = self.get_material_profile(supplier=supplier, lookup=lookup)
        profile.supplier_bpnl_source = bpnl_source
        return profile
