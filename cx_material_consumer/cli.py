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

import argparse
import json
import sys

from .bpdm_pool import BpdmPoolClient
from .bpn_discovery import BpnDiscoveryClient
from .config import Settings
from .material_service import MaterialConsumerService
from .mappers import to_custom_output
from .models import MaterialLookup, SupplierRef, SupplierSelectionRequired
from .mock_clients import MockBpdmPoolClient, MockBpnDiscoveryClient, MockConnectorRuntime, MockDtrClient


def build_parser() -> argparse.ArgumentParser:
    """
    Build the command-line argument parser for the material consumer CLI.

    Args:
            None: This method does not accept additional arguments beyond the instance context.

    Steps:
        1. Read the inputs required to build parser.
        2. Perform the operations needed to build parser.
        3. Return the resulting value or update the relevant application state.

    Returns:
            ArgumentParser: The configured CLI parser.
    """
    parser = argparse.ArgumentParser(description="Consume Catena-X material aspects and BPDM data")
    parser.add_argument("--supplier-bpnl", required=False, help="Optional supplier legal-entity BPNL. If omitted for the supplier material number flow, the app tries BPN Discovery first.")
    parser.add_argument(
        "--supplier-material-number",
        help="Preferred user-facing input for a supplier catalog/material number. Internally mapped to manufacturerPartId.",
    )
    parser.add_argument("--manufacturer-part-id", help="Low-level Catena-X input. Same meaning as supplier material number.")
    parser.add_argument("--part-instance-id", help="Part instance ID for AsBuilt lookups")
    parser.add_argument(
        "--lifecycle",
        choices=["AsPlanned", "AsBuilt"],
        help="Optional. Inferred to AsPlanned for supplier material number / manufacturer part ID, or AsBuilt for part instance ID.",
    )
    parser.add_argument(
        "--site-bpns",
        help="Optional supplier site BPNS. If omitted for AsPlanned, the app tries to infer it from PartTypeInformation and otherwise falls back to legal-entity addresses.",
    )
    parser.add_argument("--material-key", help="Output key in the custom JSON", default=None)
    return parser


def resolve_lookup_args(args: argparse.Namespace) -> tuple[MaterialLookup, str]:
    """
    Convert parsed CLI arguments into a lookup object and supplier context.

    Args:
            args (argparse.Namespace): The args used by this method.

    Steps:
        1. Read the inputs required to resolve lookup args.
        2. Perform the operations needed to resolve lookup args.
        3. Return the resulting value or update the relevant application state.

    Returns:
            tuple[SupplierRef, MaterialLookup]: The supplier and lookup models derived from the CLI arguments.
    """
    manufacturer_part_id = args.supplier_material_number or args.manufacturer_part_id
    lifecycle = args.lifecycle

    if lifecycle is None:
        if args.part_instance_id:
            lifecycle = "AsBuilt"
        elif manufacturer_part_id:
            lifecycle = "AsPlanned"
        else:
            raise ValueError("Provide either --supplier-material-number / --manufacturer-part-id or --part-instance-id.")

    lookup = MaterialLookup(
        lifecycle=lifecycle,
        manufacturer_part_id=manufacturer_part_id,
        part_instance_id=args.part_instance_id,
        site_bpns=args.site_bpns,
    )
    lookup.validate()

    material_key = (
        args.material_key
        or manufacturer_part_id
        or args.part_instance_id
        or args.supplier_bpnl
        or "material"
    )
    return lookup, material_key


def _selection_to_dict(selection: SupplierSelectionRequired) -> dict:
    """
    Convert a supplier-selection object into a plain dictionary.

    Args:
            selection (SupplierSelectionRequired): The supplier-selection object presented to the user.

    Steps:
        1. Read the inputs required to  selection to dict.
        2. Perform the operations needed to  selection to dict.
        3. Return the resulting value or update the relevant application state.

    Returns:
            dict: The supplier-selection payload represented as plain data.
    """
    return {
        "status": "selection_required",
        "message": selection.message,
        "supplier_material_number": selection.supplier_material_number,
        "provided_supplier_bpnl": selection.provided_supplier_bpnl,
        "candidates": [
            {
                "bpnl": item.bpnl,
                "supplier_name": item.supplier_name,
                "city_name": item.city_name,
                "country_alpha2": item.country_alpha2,
                "address_bpna": item.address_bpna,
            }
            for item in selection.candidates
        ],
    }


def _build_service(settings: Settings) -> MaterialConsumerService:
    """
    Build the material consumer service using the current settings.

    Args:
            settings (Settings): The runtime settings used to configure the service or client.

    Steps:
        1. Read the inputs required to  build service.
        2. Perform the operations needed to  build service.
        3. Return the resulting value or update the relevant application state.

    Returns:
            MaterialConsumerService: The configured material consumer service.
    """
    if settings.mock_mode:
        return MaterialConsumerService(
            connector_runtime=MockConnectorRuntime(),
            bpdm_pool_client=MockBpdmPoolClient(),
            dtr_asset_link_search_path=settings.dtr_asset_link_search_path,
            dtr_timeout_seconds=settings.dtr_timeout_seconds,
            cmp_lookup_mode=settings.cmp_lookup_mode,
            cmp_fixed_aas_id=settings.cmp_fixed_aas_id or None,
            bpn_discovery_client=MockBpnDiscoveryClient(),
            dtr_client_factory=MockDtrClient,
        )

    from .connector import ConnectorRuntime

    connector_runtime = ConnectorRuntime(
        dataspace_version=settings.dataspace_version,
        connector_base_url=settings.connector_base_url,
        connector_management_path=settings.connector_management_path,
        connector_headers=settings.connector_headers(),
        discovery_auth_url=settings.discovery_auth_url,
        discovery_realm=settings.discovery_realm,
        discovery_client_id=settings.discovery_client_id,
        discovery_client_secret=settings.discovery_client_secret,
        discovery_finder_url=settings.discovery_finder_url,
    )

    bpdm_client = BpdmPoolClient(
        base_url=settings.bpdm_pool_base_url,
        api_path=settings.bpdm_pool_api_path,
        headers=settings.bpdm_headers(),
        timeout=settings.bpdm_timeout_seconds,
    )

    bpn_discovery_client = None
    if settings.bpn_discovery_base_url:
        bpn_discovery_client = BpnDiscoveryClient(
            base_url=settings.bpn_discovery_base_url,
            api_path=settings.bpn_discovery_api_path,
            headers=settings.bpn_discovery_headers(),
            timeout=settings.bpn_discovery_timeout_seconds,
            key_type=settings.bpn_discovery_material_number_type,
        )

    return MaterialConsumerService(
        connector_runtime=connector_runtime,
        bpdm_pool_client=bpdm_client,
        dtr_asset_link_search_path=settings.dtr_asset_link_search_path,
        dtr_timeout_seconds=settings.dtr_timeout_seconds,
        cmp_lookup_mode=settings.cmp_lookup_mode,
        cmp_fixed_aas_id=settings.cmp_fixed_aas_id or None,
        bpn_discovery_client=bpn_discovery_client,
    )


def main() -> None:
    """
    Run the module entry point.

    Args:
            None: This method does not accept additional arguments beyond the instance context.

    Steps:
        1. Read the inputs required to main.
        2. Perform the operations needed to main.
        3. Return the resulting value or update the relevant application state.

    Returns:
            int: The process exit code.
    """
    args = build_parser().parse_args()
    settings = Settings()
    service = _build_service(settings)

    try:
        lookup, material_key = resolve_lookup_args(args)
        if lookup.lifecycle == "AsPlanned" and lookup.manufacturer_part_id:
            profile_or_selection = service.get_profile_for_supplier_material_number(
                supplier_material_number=lookup.manufacturer_part_id,
                supplier_bpnl=args.supplier_bpnl,
                site_bpns=args.site_bpns,
            )
            if isinstance(profile_or_selection, SupplierSelectionRequired):
                print(json.dumps(_selection_to_dict(profile_or_selection), indent=2, ensure_ascii=False))
                return
            profile = profile_or_selection
        else:
            if not args.supplier_bpnl:
                raise ValueError("--supplier-bpnl is required for AsBuilt / part-instance lookups.")
            supplier = SupplierRef(bpnl=args.supplier_bpnl)
            profile = service.get_material_profile(supplier, lookup)
        print(json.dumps(to_custom_output(profile, material_key=material_key), indent=2, ensure_ascii=False))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, indent=2), file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
