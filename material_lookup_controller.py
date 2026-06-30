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

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from cx_material_consumer.config import Settings
from cx_material_consumer.json_db import (
    load_materials_database,
    merge_material_output,
    save_materials_database,
)
from cx_material_consumer.mappers import to_custom_output
from cx_material_consumer.models import MaterialProfile, SupplierSelectionRequired
from cx_material_consumer.service_factory import build_service

try:
    from PyQt5.QtWidgets import QInputDialog, QMessageBox
except ImportError:  # pragma: no cover
    QInputDialog = None
    QMessageBox = None


@dataclass
class LookupControllerResult:
    """
    Store the normalized lookup result together with the generated output payload and the resolved material key.

    Class-Level Constants:
        None.

    Attributes:
        profile (MaterialProfile): Stores the profile value.
        output (dict): Stores the output value.
        material_key (str): Stores the material key value.

    Methods:
        None.
    """
    profile: MaterialProfile
    output: dict
    material_key: str


class MaterialLookupController:
    """
    Coordinate user prompting, service construction, supplier disambiguation, output generation, and database merging for the desktop application.

    Class-Level Constants:
        None.

    Attributes:
        mock_mode_getter (Callable[[], bool] | None): Stores the mock mode getter value.
        status_callback (Callable[[str], None] | None): Stores the status callback value.
        last_result (LookupControllerResult | None): Stores the last result value.

    Methods:
        __init__(): Initialize the object with the provided dependencies, default values, and internal state.
        build_settings(): Create a Settings instance from the current UI or runtime state.
        missing_real_mode_fields(): Return the list of required real-mode configuration keys that are currently missing.
        format_real_mode_configuration_error(): Build a user-friendly message that explains which real-mode configuration values still need to be provided.
        prompt_inputs(): Prompt the user for lookup input values and return the collected values.
        run_prompted_lookup(): Prompt the user for missing lookup inputs, execute the lookup flow, and return the normalized result.
        run_lookup(): Run the demonstration lookup flow from the integration example window.
        merge_last_result_into_db(): Merge the most recent lookup output into the target materials database file.
        merge_output_into_db(): Merge a provided output payload into the target materials database file.
        dump_last_result_json(): Serialize the last lookup output as formatted JSON text.
        save_last_result_json(): Write the last lookup output to a JSON file.
        _prompt_for_supplier_choice(): Prompt the user to choose one supplier candidate when a material number resolves to multiple BPNLs.
        _message(): Show a message box or return silently depending on the requested message level.
    """

    def __init__(
        self,
        mock_mode_getter: Callable[[], bool] | None = None,
        status_callback: Callable[[str], None] | None = None,
    ) -> None:
        """
        Initialize the object with the provided dependencies, default values, and internal state.

        Args:
                mock_mode_getter (Callable[[], bool] | None): The mock mode getter used by this method.
                status_callback (Callable[[str], None] | None): The status callback used by this method.

        Steps:
            1. Read the provided dependencies and configuration values.
            2. Store them on the instance for later use.
            3. Prepare any internal state required by later method calls.

        Returns:
                None: This initializer configures the instance state in place.
        """
        self.mock_mode_getter = mock_mode_getter or (lambda: False)
        self.status_callback = status_callback or (lambda _message: None)
        self.last_result: LookupControllerResult | None = None

    def build_settings(self) -> Settings:
        """
        Create a Settings instance from the current UI or runtime state.

        Args:
                None: This method does not accept additional arguments beyond the instance context.

        Steps:
            1. Read the inputs required to build settings.
            2. Perform the operations needed to build settings.
            3. Return the resulting value or update the relevant application state.

        Returns:
                Settings: The settings object built from the current runtime state.
        """
        base = Settings()
        return Settings(
            mock_mode=bool(self.mock_mode_getter()),
            dataspace_version=base.dataspace_version,
            connector_base_url=base.connector_base_url,
            connector_management_path=base.connector_management_path,
            connector_api_key=base.connector_api_key,
            discovery_auth_url=base.discovery_auth_url,
            discovery_realm=base.discovery_realm,
            discovery_client_id=base.discovery_client_id,
            discovery_client_secret=base.discovery_client_secret,
            discovery_finder_url=base.discovery_finder_url,
            bpn_discovery_base_url=base.bpn_discovery_base_url,
            bpn_discovery_api_path=base.bpn_discovery_api_path,
            bpn_discovery_timeout_seconds=base.bpn_discovery_timeout_seconds,
            bpn_discovery_api_key=base.bpn_discovery_api_key,
            bpn_discovery_material_number_type=base.bpn_discovery_material_number_type,
            bpdm_pool_base_url=base.bpdm_pool_base_url,
            bpdm_pool_api_path=base.bpdm_pool_api_path,
            bpdm_timeout_seconds=base.bpdm_timeout_seconds,
            bpdm_api_key=base.bpdm_api_key,
            dtr_asset_link_search_path=base.dtr_asset_link_search_path,
            dtr_timeout_seconds=base.dtr_timeout_seconds,
            cmp_lookup_mode=base.cmp_lookup_mode,
            cmp_fixed_aas_id=base.cmp_fixed_aas_id,
        )

    def missing_real_mode_fields(self) -> list[str]:
        """
        Return the list of required real-mode configuration keys that are currently missing.

        Args:
                None: This method does not accept additional arguments beyond the instance context.

        Steps:
            1. Read the inputs required to missing real mode fields.
            2. Perform the operations needed to missing real mode fields.
            3. Return the resulting value or update the relevant application state.

        Returns:
                list[str]: The required configuration keys that are still missing.
        """
        settings = self.build_settings()
        if settings.mock_mode:
            return []
        return settings.missing_real_mode_fields()

    def format_real_mode_configuration_error(self) -> str:
        """
        Build a user-friendly message that explains which real-mode configuration values still need to be provided.

        Args:
                None: This method does not accept additional arguments beyond the instance context.

        Steps:
            1. Read the inputs required to format real mode configuration error.
            2. Perform the operations needed to format real mode configuration error.
            3. Return the resulting value or update the relevant application state.

        Returns:
                str: A user-facing explanation of the missing configuration.
        """
        missing = self.missing_real_mode_fields()
        if not missing:
            return ""
        items = "\n".join(f"- {Settings.label_for_env_key(key)}" for key in missing)
        return (
            "Real Catena-X mode is not configured yet.\n\n"
            "Please click on 'Configuration' in the Import Supplier Material window and fill in "
            "at least the required settings before trying a lookup again.\n\n"
            f"Missing required settings:\n{items}"
        )

    def prompt_inputs(self, parent) -> tuple[str | None, str | None, str | None, str | None]:
        """
        Prompt the user for lookup input values and return the collected values.

        Args:
                parent (Any): The parent widget or object used to own dialogs and message boxes.

        Steps:
            1. Read the inputs required to prompt inputs.
            2. Perform the operations needed to prompt inputs.
            3. Return the resulting value or update the relevant application state.

        Returns:
                tuple | None: The collected input values, or None when the user cancels the prompt flow.
        """
        if QInputDialog is None:
            raise RuntimeError("PyQt5 is not installed.")

        supplier_material_number, ok = QInputDialog.getText(
            parent,
            "Supplier material number",
            "Enter supplier material number:",
        )
        if not ok or not supplier_material_number.strip():
            return None, None, None, None

        supplier_bpnl, _ = QInputDialog.getText(
            parent,
            "Supplier BPNL (optional)",
            "Enter supplier BPNL:",
        )
        site_bpns, _ = QInputDialog.getText(
            parent,
            "Site BPNS (optional)",
            "Enter site BPNS:",
        )
        material_key, _ = QInputDialog.getText(
            parent,
            "Material key (optional)",
            "Enter output material key. Leave empty to use the resolved material name:",
        )
        return (
            supplier_material_number.strip(),
            supplier_bpnl.strip() or None,
            site_bpns.strip() or None,
            material_key.strip() or None,
        )

    def run_prompted_lookup(self, parent) -> LookupControllerResult | None:
        """
        Prompt the user for missing lookup inputs, execute the lookup flow, and return the normalized result.

        Args:
                parent (Any): The parent widget or object used to own dialogs and message boxes.

        Steps:
            1. Prompt the user for the required lookup values.
            2. Run the lookup flow with the collected values.
            3. Return the normalized result to the caller.

        Returns:
                LookupControllerResult | None: The resolved lookup result, or None when the user cancels.
        """
        supplier_material_number, supplier_bpnl, site_bpns, material_key = self.prompt_inputs(parent)
        if not supplier_material_number:
            return None
        return self.run_lookup(
            parent=parent,
            supplier_material_number=supplier_material_number,
            supplier_bpnl=supplier_bpnl,
            site_bpns=site_bpns,
            material_key=material_key,
        )

    def run_lookup(
        self,
        parent,
        supplier_material_number: str,
        supplier_bpnl: str | None = None,
        site_bpns: str | None = None,
        material_key: str | None = None,
    ) -> LookupControllerResult | None:
        """
        Run the demonstration lookup flow from the integration example window.

        Args:
                parent (Any): The parent widget or object used to own dialogs and message boxes.
                supplier_material_number (str): The supplier material number entered by the user for the lookup.
                supplier_bpnl (str | None): The optional supplier BPNL used to skip supplier discovery or disambiguate results.
                site_bpns (str | None): The optional supplier site BPNS used for address enrichment.
                material_key (str | None): The optional key to use as the top-level material entry name in the output JSON.

        Steps:
            1. Validate and normalize the provided lookup inputs.
            2. Run the required discovery and retrieval steps or prompt for disambiguation when needed.
            3. Return the normalized result or selection state to the caller.

        Returns:
                None: This method updates the example window with the lookup result.
        """
        if not supplier_material_number.strip():
            self._message(parent, "Missing input", "Please enter a supplier material number.")
            return None

        self.status_callback("Running material lookup…")
        settings = self.build_settings()
        if not settings.mock_mode:
            message = self.format_real_mode_configuration_error()
            if message:
                self._message(parent, "Real mode not configured", message)
                self.status_callback("Lookup stopped. Real mode configuration is incomplete.")
                return None
        service = build_service(settings)

        result = service.get_profile_for_supplier_material_number(
            supplier_material_number=supplier_material_number.strip(),
            supplier_bpnl=(supplier_bpnl or None),
            site_bpns=(site_bpns or None),
        )

        if isinstance(result, SupplierSelectionRequired):
            chosen_bpnl = self._prompt_for_supplier_choice(parent, result)
            if not chosen_bpnl:
                self.status_callback("Lookup paused. No supplier selected.")
                return None
            result = service.get_profile_for_supplier_material_number(
                supplier_material_number=supplier_material_number.strip(),
                supplier_bpnl=chosen_bpnl,
                site_bpns=(site_bpns or None),
            )

        resolved_key = material_key or result.material_name or supplier_material_number.strip()
        output = to_custom_output(result, material_key=resolved_key)
        controller_result = LookupControllerResult(
            profile=result,
            output=output,
            material_key=resolved_key,
        )
        self.last_result = controller_result
        self.status_callback(
            f"Lookup finished. Material key: {resolved_key}; "
            f"Supplier BPNL: {result.supplier_bpnl}; lifecycle: {result.lifecycle}; "
            f"mock mode: {settings.mock_mode}."
        )
        return controller_result

    def merge_last_result_into_db(self, database_path: str | Path) -> dict:
        """
        Merge the most recent lookup output into the target materials database file.

        Args:
                database_path (str | Path): The path of the materials database JSON file.

        Steps:
            1. Load the target materials database file.
            2. Merge the last lookup output into the database structure.
            3. Persist the updated database to disk.

        Returns:
                dict: The value returned by this method.
        """
        if not self.last_result:
            raise ValueError("No lookup result available. Run a lookup first.")
        return self.merge_output_into_db(database_path, self.last_result.output)

    def merge_output_into_db(self, database_path: str | Path, output: dict) -> dict:
        """
        Merge a provided output payload into the target materials database file.

        Args:
                database_path (str | Path): The path of the materials database JSON file.
                output (dict): The generated output payload to merge or serialize.

        Steps:
            1. Load the target materials database file.
            2. Merge the provided output payload into the database structure.
            3. Persist the updated database to disk.

        Returns:
                dict: The value returned by this method.
        """
        database = load_materials_database(database_path)
        merged = merge_material_output(database, output)
        save_materials_database(database_path, merged)
        material_keys = ", ".join(output.get("materials", {}).keys()) or "material"
        self.status_callback(f"Merged {material_keys} into {database_path}")
        return merged

    def dump_last_result_json(self) -> str:
        """
        Serialize the last lookup output as formatted JSON text.

        Args:
                None: This method does not accept additional arguments beyond the instance context.

        Steps:
            1. Read the inputs required to dump last result json.
            2. Perform the operations needed to dump last result json.
            3. Return the resulting value or update the relevant application state.

        Returns:
                str: The formatted JSON text representing the last lookup output.
        """
        if not self.last_result:
            return ""
        return json.dumps(self.last_result.output, indent=2, ensure_ascii=False)

    def save_last_result_json(self, path: str | Path) -> None:
        """
        Write the last lookup output to a JSON file.

        Args:
                path (str | Path): The relative API path to call.

        Steps:
            1. Read the inputs required to save last result json.
            2. Perform the operations needed to save last result json.
            3. Return the resulting value or update the relevant application state.

        Returns:
                Path: The path of the written JSON file.
        """
        if not self.last_result:
            raise ValueError("No lookup result available. Run a lookup first.")
        Path(path).write_text(self.dump_last_result_json(), encoding="utf-8")

    def _prompt_for_supplier_choice(self, parent, selection: SupplierSelectionRequired) -> str | None:
        """
        Prompt the user to choose one supplier candidate when a material number resolves to multiple BPNLs.

        Args:
                parent (Any): The parent widget or object used to own dialogs and message boxes.
                selection (SupplierSelectionRequired): The supplier-selection object presented to the user.

        Steps:
            1. Read the inputs required to  prompt for supplier choice.
            2. Perform the operations needed to  prompt for supplier choice.
            3. Return the resulting value or update the relevant application state.

        Returns:
                str | None: The chosen supplier BPNL, or None when the user cancels.
        """
        if QInputDialog is None:
            raise RuntimeError("PyQt5 is not installed.")

        options: list[str] = []
        labels_to_bpnl: dict[str, str] = {}
        for candidate in selection.candidates:
            label = candidate.supplier_name or "Unknown supplier"
            city = candidate.city_name or "Unknown city"
            country = candidate.country_alpha2 or "--"
            bpna = candidate.address_bpna or "no BPNA"
            text = f"{label} | {candidate.bpnl} | {city}, {country} | {bpna}"
            options.append(text)
            labels_to_bpnl[text] = candidate.bpnl

        if not options:
            self._message(parent, "No suppliers found", selection.message)
            return None

        choice, ok = QInputDialog.getItem(
            parent,
            "Choose supplier",
            selection.message,
            options,
            0,
            False,
        )
        if not ok or not choice:
            return None
        return labels_to_bpnl.get(choice)

    @staticmethod
    def _message(parent, title: str, text: str) -> None:
        """
        Show a message box or return silently depending on the requested message level.

        Args:
                parent (Any): The parent widget or object used to own dialogs and message boxes.
                title (str): The title used by this method.
                text (str): The text used by this method.

        Steps:
            1. Read the inputs required to  message.
            2. Perform the operations needed to  message.
            3. Return the resulting value or update the relevant application state.

        Returns:
                None: This helper displays a message or returns without a value.
        """
        if QMessageBox is None:
            raise RuntimeError(text)
        QMessageBox.warning(parent, title, text)
