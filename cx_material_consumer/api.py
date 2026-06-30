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

from functools import lru_cache
from typing import Literal, Any, Union

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from .bpdm_pool import BpdmPoolClient
from .bpn_discovery import BpnDiscoveryClient
from .config import Settings
from .exceptions import CxMaterialConsumerError
from .material_service import MaterialConsumerService
from .mappers import to_custom_output
from .models import MaterialLookup, MaterialProfile, SupplierRef, SupplierSelectionRequired
from .mock_clients import MockBpdmPoolClient, MockBpnDiscoveryClient, MockConnectorRuntime, MockDtrClient


class SupplierMaterialNumberRequest(BaseModel):
    """
    Define the request body used by the API endpoint that resolves materials from a supplier material number.

    Class-Level Constants:
        None.

    Attributes:
        supplier_material_number (str): Stores the supplier material number value.
        supplier_bpnl (str | None): Stores the supplier bpnl value.
        site_bpns (str | None): Stores the site bpns value.
        material_key (str | None): Stores the material key value.

    Methods:
        None.
    """
    supplier_material_number: str = Field(..., description="Supplier material number; used as manufacturerPartId")
    supplier_bpnl: str | None = Field(default=None, description="Optional supplier BPNL to disambiguate or skip discovery")
    site_bpns: str | None = Field(default=None, description="Optional supplier site BPNS")
    material_key: str | None = Field(default=None, description="Optional output key in the custom JSON")


class DirectLookupRequest(BaseModel):
    """
    Define the request body used by the API endpoint that performs a direct lookup with explicit supplier information.

    Class-Level Constants:
        None.

    Attributes:
        supplier_bpnl (str): Stores the supplier bpnl value.
        lifecycle (Literal['AsPlanned', 'AsBuilt']): Stores the lifecycle value.
        manufacturer_part_id (str | None): Stores the manufacturer part id value.
        part_instance_id (str | None): Stores the part instance id value.
        site_bpns (str | None): Stores the site bpns value.
        material_key (str | None): Stores the material key value.

    Methods:
        None.
    """
    supplier_bpnl: str
    lifecycle: Literal["AsPlanned", "AsBuilt"]
    manufacturer_part_id: str | None = None
    part_instance_id: str | None = None
    site_bpns: str | None = None
    material_key: str | None = None


class ApiSuccessResponse(BaseModel):
    """
    Define the API response model used for successful material profile lookups.

    Class-Level Constants:
        None.

    Attributes:
        status (Literal['ok']): Stores the status value.
        profile (dict[str, Any]): Stores the profile value.
        output (dict[str, Any]): Stores the output value.

    Methods:
        None.
    """
    status: Literal["ok"] = "ok"
    profile: dict[str, Any]
    output: dict[str, Any]


class SupplierSelectionCandidateResponse(BaseModel):
    """
    Define the API response model for one supplier candidate returned during BPN disambiguation.

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


class SupplierSelectionResponse(BaseModel):
    """
    Define the API response model used when the client must choose one supplier before lookup can continue.

    Class-Level Constants:
        None.

    Attributes:
        status (Literal['selection_required']): Stores the status value.
        message (str): Stores the message value.
        supplier_material_number (str): Stores the supplier material number value.
        provided_supplier_bpnl (str | None): Stores the provided supplier bpnl value.
        candidates (list[SupplierSelectionCandidateResponse]): Stores the candidates value.

    Methods:
        None.
    """
    status: Literal["selection_required"] = "selection_required"
    message: str
    supplier_material_number: str
    provided_supplier_bpnl: str | None = None
    candidates: list[SupplierSelectionCandidateResponse]


ApiResponse = Union[ApiSuccessResponse, SupplierSelectionResponse]


@lru_cache(maxsize=1)
def build_service() -> MaterialConsumerService:
    """
    Build and return the configured material consumer service instance.

    Args:
            None: This method does not accept additional arguments beyond the instance context.

    Steps:
        1. Read the inputs required to build service.
        2. Perform the operations needed to build service.
        3. Return the resulting value or update the relevant application state.

    Returns:
            MaterialConsumerService: The configured material consumer service instance.
    """
    settings = Settings()

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


app = FastAPI(
    title="Catena-X Material Consumer Starter API",
    version="0.6.0",
    description=(
        "Local wrapper around the starter project so a desktop application can call a simple REST API "
        "instead of shelling out to the CLI. Supports MOCK_MODE=true for local testing without onboarding."
    ),
)


@app.get("/health")
def health() -> dict[str, str]:
    """
    Return a minimal health response for the API service.

    Args:
            None: This method does not accept additional arguments beyond the instance context.

    Steps:
        1. Read the inputs required to health.
        2. Perform the operations needed to health.
        3. Return the resulting value or update the relevant application state.

    Returns:
            dict: The API health payload.
    """
    settings = Settings()
    return {"status": "ok", "mode": "mock" if settings.mock_mode else "real"}


@app.get("/", response_class=HTMLResponse)
def root() -> str:
    """
    Return a small informational response for the API root endpoint.

    Args:
            None: This method does not accept additional arguments beyond the instance context.

    Steps:
        1. Read the inputs required to root.
        2. Perform the operations needed to root.
        3. Return the resulting value or update the relevant application state.

    Returns:
            dict: The informational API root payload.
    """
    settings = Settings()
    mode_hint = "MOCK MODE is enabled. Try MAT-4711, MAT-AMBIG, or MAT-NOCMP." if settings.mock_mode else "Use /docs for Swagger UI, or test the main endpoint below."
    return f"""
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Catena-X Material Consumer Starter API</title>
    <style>
      body {{ font-family: Arial, sans-serif; max-width: 960px; margin: 40px auto; padding: 0 16px; }}
      code, pre {{ background: #f4f4f4; padding: 2px 4px; }}
      pre {{ padding: 12px; overflow: auto; }}
      input {{ width: 100%; padding: 8px; margin: 6px 0 12px; }}
      button {{ padding: 10px 14px; }}
      .row {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
    </style>
  </head>
  <body>
    <h1>Catena-X Material Consumer Starter API</h1>
    <p>{mode_hint}</p>
    <div class="row">
      <div>
        <label>Supplier material number</label>
        <input id="supplier_material_number" placeholder="MAT-4711" />
        <label>Supplier BPNL (optional)</label>
        <input id="supplier_bpnl" placeholder="BPNL000000000001" />
        <label>Site BPNS (optional)</label>
        <input id="site_bpns" placeholder="BPNS000000000111" />
        <button onclick="runLookup()">Run lookup</button>
      </div>
      <div>
        <pre id="result">No request yet.</pre>
      </div>
    </div>
    <script>
      async function runLookup() {{
        const payload = {{
          supplier_material_number: document.getElementById('supplier_material_number').value,
          supplier_bpnl: document.getElementById('supplier_bpnl').value || null,
          site_bpns: document.getElementById('site_bpns').value || null
        }};
        const res = await fetch('/profiles/supplier-material-number', {{
          method: 'POST',
          headers: {{'Content-Type': 'application/json'}},
          body: JSON.stringify(payload)
        }});
        const data = await res.json();
        document.getElementById('result').textContent = JSON.stringify(data, null, 2);
      }}
    </script>
  </body>
</html>
"""


def _profile_to_dict(profile: MaterialProfile) -> dict[str, Any]:
    """
    Convert a material profile into a plain dictionary for API responses.

    Args:
            profile (MaterialProfile): The resolved material profile to convert or serialize.

    Steps:
        1. Read the inputs required to  profile to dict.
        2. Perform the operations needed to  profile to dict.
        3. Return the resulting value or update the relevant application state.

    Returns:
            dict: The material profile represented as plain data.
    """
    return {
        "supplier_bpnl": profile.supplier_bpnl,
        "supplier_bpnl_source": profile.supplier_bpnl_source,
        "supplier_site_bpns": profile.supplier_site_bpns,
        "supplier_address_bpna": profile.supplier_address_bpna,
        "manufacturer_part_id": profile.manufacturer_part_id,
        "part_instance_id": profile.part_instance_id,
        "lifecycle": profile.lifecycle,
        "material_name": profile.material_name,
        "candidate_site_bpnss": profile.candidate_site_bpnss,
        "smc_semantic_id": profile.smc_semantic_id,
        "part_type_information_payload": profile.part_type_information_payload,
        "smc_payload": profile.smc_payload,
        "cmp_payload": profile.cmp_payload,
        "bpdm_site": profile.bpdm_site,
        "bpdm_address": profile.bpdm_address,
    }


def _selection_to_dict(selection: SupplierSelectionRequired) -> dict[str, Any]:
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


@app.post("/profiles/supplier-material-number", response_model=ApiResponse)
def profile_for_supplier_material_number(request: SupplierMaterialNumberRequest) -> ApiResponse:
    """
    Handle the API endpoint that resolves a material profile from a supplier material number.

    Args:
            request (SupplierMaterialNumberRequest): The request used by this method.

    Steps:
        1. Read the inputs required to profile for supplier material number.
        2. Perform the operations needed to profile for supplier material number.
        3. Return the resulting value or update the relevant application state.

    Returns:
            dict | ApiSuccessResponse | SupplierSelectionResponse: The API response for the supplier-material-number lookup.
    """
    service = build_service()
    try:
        profile_or_selection = service.get_profile_for_supplier_material_number(
            supplier_material_number=request.supplier_material_number,
            supplier_bpnl=request.supplier_bpnl,
            site_bpns=request.site_bpns,
        )
        if isinstance(profile_or_selection, SupplierSelectionRequired):
            return SupplierSelectionResponse(**_selection_to_dict(profile_or_selection))
        material_key = request.material_key or request.supplier_material_number
        return ApiSuccessResponse(
            profile=_profile_to_dict(profile_or_selection),
            output=to_custom_output(profile_or_selection, material_key),
        )
    except CxMaterialConsumerError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/profiles/direct", response_model=ApiSuccessResponse)
def profile_direct(request: DirectLookupRequest) -> ApiSuccessResponse:
    """
    Handle the API endpoint that performs a direct supplier lookup.

    Args:
            request (DirectLookupRequest): The request used by this method.

    Steps:
        1. Read the inputs required to profile direct.
        2. Perform the operations needed to profile direct.
        3. Return the resulting value or update the relevant application state.

    Returns:
            ApiSuccessResponse: The API response for the direct lookup path.
    """
    service = build_service()
    try:
        lookup = MaterialLookup(
            lifecycle=request.lifecycle,
            manufacturer_part_id=request.manufacturer_part_id,
            part_instance_id=request.part_instance_id,
            site_bpns=request.site_bpns,
        )
        lookup.validate()
        supplier = SupplierRef(bpnl=request.supplier_bpnl)
        profile = service.get_material_profile(supplier=supplier, lookup=lookup)
        material_key = (
            request.material_key
            or request.manufacturer_part_id
            or request.part_instance_id
            or request.supplier_bpnl
        )
        return ApiSuccessResponse(
            profile=_profile_to_dict(profile),
            output=to_custom_output(profile, material_key),
        )
    except (CxMaterialConsumerError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
