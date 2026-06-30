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
import sys
from pathlib import Path

from .cli import _build_service
from .config import Settings
from .json_db import load_materials_database, merge_material_output, save_materials_database
from .mappers import to_custom_output
from .models import SupplierSelectionRequired


try:
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import (
        QApplication,
        QCheckBox,
        QFileDialog,
        QFormLayout,
        QGridLayout,
        QHBoxLayout,
        QInputDialog,
        QLabel,
        QLineEdit,
        QMainWindow,
        QMessageBox,
        QPushButton,
        QTextEdit,
        QVBoxLayout,
        QWidget,
    )
except ImportError:  # pragma: no cover - friendly runtime message only
    QApplication = None


class MaterialLookupWindow(QMainWindow):
    """
    Provide the standalone demo window that performs lookups, shows output, and writes materials database updates.

    Class-Level Constants:
        None.

    Attributes:
        None.

    Methods:
        __init__(): Initialize the object with the provided dependencies, default values, and internal state.
        _build_ui(): Create and arrange the widgets used by the dialog or window.
        _load_defaults(): Load initial values into the standalone demo GUI.
        _build_settings(): Build a Settings instance from the standalone GUI state.
        _run_lookup(): Execute a lookup from the standalone GUI and display the result.
        _prompt_for_supplier_choice(): Prompt the user to choose one supplier candidate when a material number resolves to multiple BPNLs.
        _save_output_as_json(): Save the current standalone GUI output to a JSON file.
        _merge_into_database(): Merge the current standalone GUI output into a materials database file.
        _copy_output(): Copy the current standalone GUI output to the clipboard.
    """
    def __init__(self) -> None:
        """
        Initialize the object with the provided dependencies, default values, and internal state.

        Args:
                None: This method does not accept additional arguments beyond the instance context.

        Steps:
            1. Read the provided dependencies and configuration values.
            2. Store them on the instance for later use.
            3. Prepare any internal state required by later method calls.

        Returns:
                None: This initializer configures the instance state in place.
        """
        super().__init__()
        self.setWindowTitle("Catena-X Material Consumer")
        self.resize(980, 760)
        self._last_output: dict | None = None
        self._last_profile: dict | None = None
        self._last_selection: dict | None = None
        self._build_ui()
        self._load_defaults()

    def _build_ui(self) -> None:
        """
        Create and arrange the widgets used by the dialog or window.

        Args:
                None: This method does not accept additional arguments beyond the instance context.

        Steps:
            1. Read the inputs required to  build ui.
            2. Perform the operations needed to  build ui.
            3. Return the resulting value or update the relevant application state.

        Returns:
                None: The value returned by this method.
        """
        central = QWidget(self)
        self.setCentralWidget(central)
        root = QVBoxLayout(central)

        description = QLabel(
            "Enter a supplier material number and optional supplier/site identifiers. "
            "The output is generated in the materials.json structure and can be merged into your materials database."
        )
        description.setWordWrap(True)
        root.addWidget(description)

        form_widget = QWidget(self)
        form_layout = QFormLayout(form_widget)
        root.addWidget(form_widget)

        self.supplier_material_number_edit = QLineEdit(self)
        self.supplier_material_number_edit.setPlaceholderText("e.g. MAT-4711")
        form_layout.addRow("Supplier material number*", self.supplier_material_number_edit)

        self.supplier_bpnl_edit = QLineEdit(self)
        self.supplier_bpnl_edit.setPlaceholderText("optional, e.g. BPNL000000000001")
        form_layout.addRow("Supplier BPNL", self.supplier_bpnl_edit)

        self.site_bpns_edit = QLineEdit(self)
        self.site_bpns_edit.setPlaceholderText("optional, e.g. BPNS000000000111")
        form_layout.addRow("Site BPNS", self.site_bpns_edit)

        self.material_key_edit = QLineEdit(self)
        self.material_key_edit.setPlaceholderText("optional; defaults to the resolved material name")
        form_layout.addRow("Material key", self.material_key_edit)

        self.database_path_edit = QLineEdit(self)
        self.database_path_edit.setPlaceholderText("optional path to your large materials JSON file")
        form_layout.addRow("Materials DB path", self.database_path_edit)

        options_layout = QHBoxLayout()
        self.mock_mode_checkbox = QCheckBox("Mock mode")
        self.mock_mode_checkbox.setToolTip("Use built-in mock responses for demos and local testing.")
        options_layout.addWidget(self.mock_mode_checkbox)
        options_layout.addStretch(1)
        root.addLayout(options_layout)

        button_layout = QGridLayout()
        root.addLayout(button_layout)

        self.fetch_button = QPushButton("Fetch material output", self)
        self.fetch_button.clicked.connect(self._run_lookup)
        button_layout.addWidget(self.fetch_button, 0, 0)

        self.merge_button = QPushButton("Merge into materials DB", self)
        self.merge_button.clicked.connect(self._merge_into_database)
        self.merge_button.setEnabled(False)
        button_layout.addWidget(self.merge_button, 0, 1)

        self.save_button = QPushButton("Save output as JSON…", self)
        self.save_button.clicked.connect(self._save_output_as_json)
        self.save_button.setEnabled(False)
        button_layout.addWidget(self.save_button, 0, 2)

        self.copy_button = QPushButton("Copy output", self)
        self.copy_button.clicked.connect(self._copy_output)
        self.copy_button.setEnabled(False)
        button_layout.addWidget(self.copy_button, 0, 3)

        self.status_label = QLabel("Ready.")
        self.status_label.setWordWrap(True)
        self.status_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        root.addWidget(self.status_label)

        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText("The generated materials.json output will appear here.")
        root.addWidget(self.output_text, 1)

    def _load_defaults(self) -> None:
        """
        Load initial values into the standalone demo GUI.

        Args:
                None: This method does not accept additional arguments beyond the instance context.

        Steps:
            1. Read the inputs required to  load defaults.
            2. Perform the operations needed to  load defaults.
            3. Return the resulting value or update the relevant application state.

        Returns:
                None: The value returned by this method.
        """
        settings = Settings()
        self.mock_mode_checkbox.setChecked(settings.mock_mode)
        self.database_path_edit.setText(str(Path("materials_database.json")))


    def _build_settings(self) -> Settings:
        """
        Build a Settings instance from the standalone GUI state.

        Args:
                None: This method does not accept additional arguments beyond the instance context.

        Steps:
            1. Read the inputs required to  build settings.
            2. Perform the operations needed to  build settings.
            3. Return the resulting value or update the relevant application state.

        Returns:
                Settings: The settings built from the current GUI state.
        """
        base = Settings()
        return Settings(
            mock_mode=self.mock_mode_checkbox.isChecked(),
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

    def _run_lookup(self) -> None:
        """
        Execute a lookup from the standalone GUI and display the result.

        Args:
                None: This method does not accept additional arguments beyond the instance context.

        Steps:
            1. Read the inputs required to  run lookup.
            2. Perform the operations needed to  run lookup.
            3. Return the resulting value or update the relevant application state.

        Returns:
                None: This method updates the GUI in place with the lookup result.
        """
        supplier_material_number = self.supplier_material_number_edit.text().strip()
        supplier_bpnl = self.supplier_bpnl_edit.text().strip() or None
        site_bpns = self.site_bpns_edit.text().strip() or None
        user_material_key = self.material_key_edit.text().strip() or None

        if not supplier_material_number:
            QMessageBox.warning(self, "Missing input", "Please enter a supplier material number.")
            return

        self.status_label.setText("Running lookup…")
        QApplication.processEvents()

        try:
            settings = self._build_settings()
            service = _build_service(settings)
            result = service.get_profile_for_supplier_material_number(
                supplier_material_number=supplier_material_number,
                supplier_bpnl=supplier_bpnl,
                site_bpns=site_bpns,
            )

            if isinstance(result, SupplierSelectionRequired):
                chosen_bpnl = self._prompt_for_supplier_choice(result)
                if not chosen_bpnl:
                    self.status_label.setText("Lookup paused. No supplier selected.")
                    return
                self.supplier_bpnl_edit.setText(chosen_bpnl)
                result = service.get_profile_for_supplier_material_number(
                    supplier_material_number=supplier_material_number,
                    supplier_bpnl=chosen_bpnl,
                    site_bpns=site_bpns,
                )

            material_key = user_material_key or result.material_name or supplier_material_number
            output = to_custom_output(result, material_key=material_key)
            if not user_material_key and result.material_name:
                self.material_key_edit.setText(result.material_name)
            self._last_output = output
            self._last_profile = {
                "supplier_bpnl": result.supplier_bpnl,
                "supplier_bpnl_source": result.supplier_bpnl_source,
                "supplier_site_bpns": result.supplier_site_bpns,
                "supplier_address_bpna": result.supplier_address_bpna,
                "manufacturer_part_id": result.manufacturer_part_id,
                "lifecycle": result.lifecycle,
                "material_name": result.material_name,
            }
            self.output_text.setPlainText(json.dumps(output, indent=2, ensure_ascii=False))
            self.merge_button.setEnabled(True)
            self.save_button.setEnabled(True)
            self.copy_button.setEnabled(True)
            self.status_label.setText(
                f"Lookup finished. Material key: {material_key}; Supplier BPNL: {result.supplier_bpnl}; lifecycle: {result.lifecycle}; mock mode: {settings.mock_mode}."
            )
        except Exception as exc:  # pragma: no cover - GUI feedback path
            self.status_label.setText("Lookup failed.")
            QMessageBox.critical(self, "Lookup failed", str(exc))

    def _prompt_for_supplier_choice(self, selection: SupplierSelectionRequired) -> str | None:
        """
        Prompt the user to choose one supplier candidate when a material number resolves to multiple BPNLs.

        Args:
                selection (SupplierSelectionRequired): The supplier-selection object presented to the user.

        Steps:
            1. Read the inputs required to  prompt for supplier choice.
            2. Perform the operations needed to  prompt for supplier choice.
            3. Return the resulting value or update the relevant application state.

        Returns:
                str | None: The chosen supplier BPNL, or None when the user cancels.
        """
        options: list[str] = []
        index_to_bpnl: dict[str, str] = {}
        for candidate in selection.candidates:
            label = candidate.supplier_name or "Unknown supplier"
            city = candidate.city_name or "Unknown city"
            country = candidate.country_alpha2 or "--"
            bpna = candidate.address_bpna or "no BPNA"
            text = f"{label} | {candidate.bpnl} | {city}, {country} | {bpna}"
            options.append(text)
            index_to_bpnl[text] = candidate.bpnl

        if not options:
            QMessageBox.warning(self, "No suppliers found", selection.message)
            return None

        choice, ok = QInputDialog.getItem(
            self,
            "Choose supplier",
            selection.message,
            options,
            0,
            False,
        )
        if not ok or not choice:
            return None
        return index_to_bpnl.get(choice)

    def _save_output_as_json(self) -> None:
        """
        Save the current standalone GUI output to a JSON file.

        Args:
                None: This method does not accept additional arguments beyond the instance context.

        Steps:
            1. Read the inputs required to  save output as json.
            2. Perform the operations needed to  save output as json.
            3. Return the resulting value or update the relevant application state.

        Returns:
                None: This method writes the GUI output to a JSON file.
        """
        if not self._last_output:
            QMessageBox.information(self, "No output", "Run a lookup first.")
            return
        default_name = self.material_key_edit.text().strip() or self.supplier_material_number_edit.text().strip() or "material-output"
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save materials JSON output",
            f"{default_name}.json" if not str(default_name).endswith('.json') else str(default_name),
            "JSON files (*.json);;All files (*)",
        )
        if not path:
            return
        Path(path).write_text(json.dumps(self._last_output, indent=2, ensure_ascii=False), encoding="utf-8")
        self.status_label.setText(f"Saved output to {path}")

    def _merge_into_database(self) -> None:
        """
        Merge the current standalone GUI output into a materials database file.

        Args:
                None: This method does not accept additional arguments beyond the instance context.

        Steps:
            1. Read the inputs required to  merge into database.
            2. Perform the operations needed to  merge into database.
            3. Return the resulting value or update the relevant application state.

        Returns:
                None: This method merges the current GUI output into the selected database file.
        """
        if not self._last_output:
            QMessageBox.information(self, "No output", "Run a lookup first.")
            return
        database_path = self.database_path_edit.text().strip()
        if not database_path:
            QMessageBox.warning(self, "Missing database path", "Please choose the materials database JSON file.")
            return
        try:
            database = load_materials_database(database_path)
            merged = merge_material_output(database, self._last_output)
            save_materials_database(database_path, merged)
            material_keys = ", ".join(self._last_output.get("materials", {}).keys()) or "material"
            self.status_label.setText(f"Merged {material_keys} into {database_path}")
            QMessageBox.information(self, "Merge complete", f"Merged {material_keys} into\n{database_path}")
        except Exception as exc:  # pragma: no cover - GUI feedback path
            QMessageBox.critical(self, "Merge failed", str(exc))

    def _copy_output(self) -> None:
        """
        Copy the current standalone GUI output to the clipboard.

        Args:
                None: This method does not accept additional arguments beyond the instance context.

        Steps:
            1. Read the inputs required to  copy output.
            2. Perform the operations needed to  copy output.
            3. Return the resulting value or update the relevant application state.

        Returns:
                None: This method copies the current GUI output to the clipboard.
        """
        text = self.output_text.toPlainText().strip()
        if not text:
            QMessageBox.information(self, "No output", "Run a lookup first.")
            return
        QApplication.clipboard().setText(text)
        self.status_label.setText("Output copied to clipboard.")


def launch_gui() -> None:
    """
    Start the standalone demo GUI application.

    Args:
            None: This method does not accept additional arguments beyond the instance context.

    Steps:
        1. Read the inputs required to launch gui.
        2. Perform the operations needed to launch gui.
        3. Return the resulting value or update the relevant application state.

    Returns:
            int: The GUI process exit code.
    """
    if QApplication is None:  # pragma: no cover - runtime guard only
        raise SystemExit("PyQt5 is not installed. Install it with: pip install PyQt5")

    app = QApplication(sys.argv)
    window = MaterialLookupWindow()
    window.show()
    sys.exit(app.exec_())
