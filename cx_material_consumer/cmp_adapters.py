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

from dataclasses import dataclass
from typing import Protocol

from .dtr import DtrClient
from .exceptions import DtrLookupError
from .models import MaterialLookup, SEMANTIC_ID_CMP


class CmpLookupAdapter(Protocol):
    """
    Define the interface used to resolve Chemical Material Passport payloads for a material lookup.

    Class-Level Constants:
        None.

    Attributes:
        None.

    Methods:
        get_cmp(): Resolve and return a Chemical Material Passport payload.
    """
    def get_cmp(self, dtr: DtrClient, lookup: MaterialLookup) -> dict:
        """
        Resolve and return a Chemical Material Passport payload.

        Args:
                dtr (DtrClient): The dtr used by this method.
                lookup (MaterialLookup): The lookup model describing the identifiers and lifecycle to resolve.

        Steps:
            1. Read the inputs required to get cmp.
            2. Perform the operations needed to get cmp.
            3. Return the resulting value or update the relevant application state.

        Returns:
                dict: The resolved Chemical Material Passport payload.
        """
        ...


@dataclass(frozen=True)
class PlannedPartTwinCmpAdapter:
    """
    Resolve Chemical Material Passport data from the planned-part twin associated with a supplier material number.

    Class-Level Constants:
        None.

    Attributes:
        None.

    Methods:
        get_cmp(): Resolve and return a Chemical Material Passport payload.
    """

    def get_cmp(self, dtr: DtrClient, lookup: MaterialLookup) -> dict:
        """
        Resolve and return a Chemical Material Passport payload.

        Args:
                dtr (DtrClient): The dtr used by this method.
                lookup (MaterialLookup): The lookup model describing the identifiers and lifecycle to resolve.

        Steps:
            1. Read the inputs required to get cmp.
            2. Perform the operations needed to get cmp.
            3. Return the resulting value or update the relevant application state.

        Returns:
                dict: The resolved Chemical Material Passport payload.
        """
        if not lookup.manufacturer_part_id:
            raise DtrLookupError("manufacturerPartId is required for planned-part CMP lookup")

        shell_ids = dtr.search_shell_ids_by_asset_link(
            [
                {"key": "manufacturerPartId", "value": lookup.manufacturer_part_id},
                {"key": "assetLifecyclePhase", "value": "AsPlanned"},
            ]
        )
        if not shell_ids:
            raise DtrLookupError("No candidate shells found for CMP planned-part lookup")

        for aas_id in shell_ids:
            descriptor = dtr.get_shell_descriptor(aas_id)
            submodel = dtr.find_submodel_descriptor(descriptor, SEMANTIC_ID_CMP)
            if submodel:
                return dtr.fetch_submodel_value(submodel)

        raise DtrLookupError("CMP submodel not found on planned-part candidate shells")


@dataclass(frozen=True)
class FixedAasIdCmpAdapter:
    """
    Resolve Chemical Material Passport data from a fixed shell identifier when the provider requires a custom lookup path.

    Class-Level Constants:
        None.

    Attributes:
        aas_id (str): Stores the aas id value.

    Methods:
        get_cmp(): Resolve and return a Chemical Material Passport payload.
    """
    aas_id: str

    def get_cmp(self, dtr: DtrClient, lookup: MaterialLookup) -> dict:
        """
        Resolve and return a Chemical Material Passport payload.

        Args:
                dtr (DtrClient): The dtr used by this method.
                lookup (MaterialLookup): The lookup model describing the identifiers and lifecycle to resolve.

        Steps:
            1. Read the inputs required to get cmp.
            2. Perform the operations needed to get cmp.
            3. Return the resulting value or update the relevant application state.

        Returns:
                dict: The resolved Chemical Material Passport payload.
        """
        return dtr.get_cmp_by_aas_id(self.aas_id)


def build_cmp_adapter(mode: str, fixed_aas_id: str | None = None) -> CmpLookupAdapter:
    """
    Create the CMP lookup adapter configured for the current settings.

    Args:
            mode (str): The mode used by this method.
            fixed_aas_id (str | None): The fixed aas id used by this method.

    Steps:
        1. Read the inputs required to build cmp adapter.
        2. Perform the operations needed to build cmp adapter.
        3. Return the resulting value or update the relevant application state.

    Returns:
            CmpLookupAdapter: The configured CMP lookup adapter.
    """
    if mode == "planned-part-twin":
        return PlannedPartTwinCmpAdapter()
    if mode == "fixed-aas-id":
        if not fixed_aas_id:
            raise ValueError("CMP fixed AAS ID is required for cmp lookup mode 'fixed-aas-id'")
        return FixedAasIdCmpAdapter(aas_id=fixed_aas_id)
    raise ValueError(f"Unsupported CMP lookup mode: {mode}")
