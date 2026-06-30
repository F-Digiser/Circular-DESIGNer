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

from dataclasses import dataclass, field
from typing import Any, Literal

Lifecycle = Literal["AsPlanned", "AsBuilt"]


SEMANTIC_ID_SMC_CALCULATED = (
    "urn:samm:io.catenax.secondary_material_content_calculated:1.0.0"
    "#SecondaryMaterialContentCalculated"
)
SEMANTIC_ID_SMC_VERIFIABLE = (
    "urn:samm:io.catenax.secondary_material_content_verifiable:1.0.0"
    "#SecondaryMaterialContentVerifiable"
)
SEMANTIC_ID_CMP = (
    "urn:samm:io.catenax.material.chemical_material_passport:1.0.0"
    "#ChemicalMaterialPassport"
)
SEMANTIC_ID_PART_TYPE_INFORMATION = (
    "urn:samm:io.catenax.part_type_information:1.0.0#PartTypeInformation"
)
DIGITAL_TWIN_REGISTRY_TYPE = "https://w3id.org/catenax/taxonomy#DigitalTwinRegistry"


@dataclass(frozen=True)
class SupplierRef:
    """
    Represent the supplier context used during a lookup.

    Class-Level Constants:
        None.

    Attributes:
        bpnl (str): Stores the bpnl value.

    Methods:
        None.
    """
    bpnl: str


@dataclass(frozen=True)
class MaterialLookup:
    """
    Represent the lookup keys and lifecycle information required to resolve material-related twins and submodels.

    Class-Level Constants:
        None.

    Attributes:
        lifecycle (Lifecycle): Stores the lifecycle value.
        manufacturer_part_id (str | None): Stores the manufacturer part id value.
        part_instance_id (str | None): Stores the part instance id value.
        site_bpns (str | None): Stores the site bpns value.

    Methods:
        validate(): Validate the lookup model and raise an error when the provided identifiers are inconsistent.
    """
    lifecycle: Lifecycle
    manufacturer_part_id: str | None = None
    part_instance_id: str | None = None
    site_bpns: str | None = None

    def validate(self) -> None:
        """
        Validate the lookup model and raise an error when the provided identifiers are inconsistent.

        Args:
                None: This method does not accept additional arguments beyond the instance context.

        Steps:
            1. Read the inputs required to validate.
            2. Perform the operations needed to validate.
            3. Return the resulting value or update the relevant application state.

        Returns:
                None: The value returned by this method.
        """
        if self.lifecycle == "AsPlanned" and not self.manufacturer_part_id:
            raise ValueError("manufacturer_part_id is required for AsPlanned")
        if self.lifecycle == "AsBuilt" and not self.part_instance_id:
            raise ValueError("part_instance_id is required for AsBuilt")


@dataclass
class BpdmAddress:
    """
    Represent a normalized BPDM address record.

    Class-Level Constants:
        None.

    Attributes:
        bpna (str | None): Stores the bpna value.
        name (str | None): Stores the name value.
        street_name (str | None): Stores the street name value.
        house_number (str | None): Stores the house number value.
        postal_code (str | None): Stores the postal code value.
        city_name (str | None): Stores the city name value.
        country_alpha2 (str | None): Stores the country alpha2 value.
        raw (dict[str, Any]): Stores the raw value.

    Methods:
        None.
    """
    bpna: str | None = None
    name: str | None = None
    street_name: str | None = None
    house_number: str | None = None
    postal_code: str | None = None
    city_name: str | None = None
    country_alpha2: str | None = None
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass
class BpdmSite:
    """
    Represent a normalized BPDM site record.

    Class-Level Constants:
        None.

    Attributes:
        bpns (str | None): Stores the bpns value.
        name (str | None): Stores the name value.
        main_address_bpna (str | None): Stores the main address bpna value.
        legal_entity_bpnl (str | None): Stores the legal entity bpnl value.
        raw (dict[str, Any]): Stores the raw value.

    Methods:
        None.
    """
    bpns: str | None = None
    name: str | None = None
    main_address_bpna: str | None = None
    legal_entity_bpnl: str | None = None
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass
class MaterialProfile:
    """
    Store the resolved material profile data that is later converted into the target materials JSON structure.

    Class-Level Constants:
        None.

    Attributes:
        supplier_bpnl (str): Stores the supplier bpnl value.
        supplier_bpnl_source (str): Stores the supplier bpnl source value.
        supplier_site_bpns (str | None): Stores the supplier site bpns value.
        supplier_address_bpna (str | None): Stores the supplier address bpna value.
        manufacturer_part_id (str | None): Stores the manufacturer part id value.
        part_instance_id (str | None): Stores the part instance id value.
        lifecycle (Lifecycle): Stores the lifecycle value.
        material_name (str | None): Stores the material name value.
        part_type_information_payload (dict[str, Any] | None): Stores the part type information payload value.
        candidate_site_bpnss (list[str]): Stores the candidate site bpnss value.
        smc_semantic_id (str | None): Stores the smc semantic id value.
        smc_payload (dict[str, Any] | None): Stores the smc payload value.
        cmp_payload (dict[str, Any] | None): Stores the cmp payload value.
        bpdm_site (dict[str, Any] | None): Stores the bpdm site value.
        bpdm_address (dict[str, Any] | None): Stores the bpdm address value.

    Methods:
        None.
    """
    supplier_bpnl: str
    supplier_bpnl_source: str
    supplier_site_bpns: str | None
    supplier_address_bpna: str | None
    manufacturer_part_id: str | None
    part_instance_id: str | None
    lifecycle: Lifecycle
    material_name: str | None
    part_type_information_payload: dict[str, Any] | None
    candidate_site_bpnss: list[str]
    smc_semantic_id: str | None
    smc_payload: dict[str, Any] | None
    cmp_payload: dict[str, Any] | None
    bpdm_site: dict[str, Any] | None
    bpdm_address: dict[str, Any] | None


@dataclass
class SupplierSelectionCandidate:
    """
    Represent a user-facing supplier option when a material number resolves to multiple BPNLs.

    Class-Level Constants:
        None.

    Attributes:
        bpnl (str): Stores the bpnl value.
        supplier_name (str | None): Stores the supplier name value.
        city_name (str | None): Stores the city name value.
        country_alpha2 (str | None): Stores the country alpha2 value.
        address_bpna (str | None): Stores the address bpna value.

    Methods:
        None.
    """
    bpnl: str
    supplier_name: str | None = None
    city_name: str | None = None
    country_alpha2: str | None = None
    address_bpna: str | None = None


@dataclass
class SupplierSelectionRequired:
    """
    Represent the intermediate selection state that requests the user to choose one supplier candidate before continuing.

    Class-Level Constants:
        None.

    Attributes:
        supplier_material_number (str): Stores the supplier material number value.
        message (str): Stores the message value.
        candidates (list[SupplierSelectionCandidate]): Stores the candidates value.
        provided_supplier_bpnl (str | None): Stores the provided supplier bpnl value.

    Methods:
        None.
    """
    supplier_material_number: str
    message: str
    candidates: list[SupplierSelectionCandidate]
    provided_supplier_bpnl: str | None = None
