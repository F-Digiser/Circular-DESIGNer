""""    
    Copyright (C) 2026  Digiser, Riech & Nebel

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

from PyQt5.QtWidgets import (
    QDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from cx_material_consumer.config import Settings, get_default_env_path


class ConfigurationDialog(QDialog):
    """
    Provide a dialog that displays and edits the Catena-X runtime configuration required for real mode lookups.

    Class-Level Constants:
        FIELD_ORDER (Any): Defines the f i e l d  o r d e r constant.

    Attributes:
        env_path (Any): Stores the env path value.
        settings (Any): Stores the settings value.
        edits (dict[str, QLineEdit]): Stores the edits value.

    Methods:
        __init__(): Initialize the object with the provided dependencies, default values, and internal state.
        _build_ui(): Create and arrange the widgets used by the dialog or window.
        _field_label(): Return the user-facing label text for one environment key.
        _create_line_edit_for(): Create a line edit widget for one configuration value.
        _load_values_into_form(): Load the current configuration values into the dialog form.
        _collect_values(): Collect the current form values from the dialog widgets.
        _settings_from_form(): Build a Settings object from the values currently entered in the dialog.
        _missing_required_labels(): Return the human-readable labels of the required configuration fields that are missing.
        on_validate(): Validate the current dialog values and show the validation result to the user.
        on_save(): Persist the current configuration values and close the dialog when validation succeeds.
    """

    FIELD_ORDER = [
        "CX_DATASPACE_VERSION",
        "CX_CONNECTOR_BASE_URL",
        "CX_CONNECTOR_MANAGEMENT_PATH",
        "CX_CONNECTOR_API_KEY",
        "CX_DISCOVERY_AUTH_URL",
        "CX_DISCOVERY_REALM",
        "CX_DISCOVERY_CLIENT_ID",
        "CX_DISCOVERY_CLIENT_SECRET",
        "CX_DISCOVERY_FINDER_URL",
        "BPN_DISCOVERY_BASE_URL",
        "BPN_DISCOVERY_API_PATH",
        "BPN_DISCOVERY_TIMEOUT_SECONDS",
        "BPN_DISCOVERY_API_KEY",
        "BPN_DISCOVERY_MATERIAL_NUMBER_TYPE",
        "BPDM_POOL_BASE_URL",
        "BPDM_POOL_API_PATH",
        "BPDM_TIMEOUT_SECONDS",
        "BPDM_API_KEY",
        "DTR_ASSET_LINK_SEARCH_PATH",
        "DTR_TIMEOUT_SECONDS",
        "CMP_LOOKUP_MODE",
        "CMP_FIXED_AAS_ID",
    ]

    def __init__(self, parent=None):
        """
        Initialize the object with the provided dependencies, default values, and internal state.

        Args:
                parent (Any): The parent widget or object used to own dialogs and message boxes.

        Steps:
            1. Read the provided dependencies and configuration values.
            2. Store them on the instance for later use.
            3. Prepare any internal state required by later method calls.

        Returns:
                None: This initializer configures the instance state in place.
        """
        super().__init__(parent)
        self.setWindowTitle("Configuration")
        self.resize(760, 720)

        self.env_path = get_default_env_path()
        self.settings = Settings()
        self.edits: dict[str, QLineEdit] = {}

        self._build_ui()
        self._load_values_into_form()

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
        layout = QVBoxLayout(self)

        intro = QLabel(
            "Required fields are marked with *. These are the minimum settings for real Catena-X mode.\n"
            "BPN Discovery settings are optional in general, but they are recommended when the supplier BPNL should\n"
            "be resolved automatically from a supplier material number without entering the BPNL manually."
        )
        intro.setWordWrap(True)
        layout.addWidget(intro)

        env_label = QLabel(f"Configuration file: {self.env_path}")
        env_label.setWordWrap(True)
        layout.addWidget(env_label)

        required_group = QGroupBox("Minimum required for real mode")
        required_form = QFormLayout(required_group)
        for key in Settings.required_real_mode_env_keys():
            required_form.addRow(self._field_label(key, required=True), self._create_line_edit_for(key))
        layout.addWidget(required_group)

        optional_group = QGroupBox("Optional / advanced")
        optional_form = QFormLayout(optional_group)
        optional_keys = [key for key in self.FIELD_ORDER if key not in Settings.required_real_mode_env_keys()]
        for key in optional_keys:
            optional_form.addRow(self._field_label(key, required=False), self._create_line_edit_for(key))
        layout.addWidget(optional_group)

        self.status_label = QLabel("")
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)

        buttons = QHBoxLayout()
        self.validate_button = QPushButton("Validate")
        self.validate_button.clicked.connect(self.on_validate)
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.on_save)
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.accept)
        buttons.addWidget(self.validate_button)
        buttons.addWidget(self.save_button)
        buttons.addStretch(1)
        buttons.addWidget(self.close_button)
        layout.addLayout(buttons)

    def _field_label(self, key: str, required: bool) -> str:
        """
        Return the user-facing label text for one environment key.

        Args:
                key (str): The key used by this method.
                required (bool): The required used by this method.

        Steps:
            1. Read the inputs required to  field label.
            2. Perform the operations needed to  field label.
            3. Return the resulting value or update the relevant application state.

        Returns:
                str: The user-facing label text for the requested configuration key.
        """
        label = Settings.label_for_env_key(key)
        return f"{label} *" if required else label

    def _create_line_edit_for(self, key: str) -> QLineEdit:
        """
        Create a line edit widget for one configuration value.

        Args:
                key (str): The key used by this method.

        Steps:
            1. Read the inputs required to  create line edit for.
            2. Perform the operations needed to  create line edit for.
            3. Return the resulting value or update the relevant application state.

        Returns:
                QLineEdit: The configured line edit widget for the requested configuration key.
        """
        edit = QLineEdit()
        if "SECRET" in key or key.endswith("API_KEY"):
            edit.setEchoMode(QLineEdit.Password)
        self.edits[key] = edit
        return edit

    def _load_values_into_form(self) -> None:
        """
        Load the current configuration values into the dialog form.

        Args:
                None: This method does not accept additional arguments beyond the instance context.

        Steps:
            1. Read the inputs required to  load values into form.
            2. Perform the operations needed to  load values into form.
            3. Return the resulting value or update the relevant application state.

        Returns:
                None: The value returned by this method.
        """
        values = self.settings.to_env_dict()
        for key, edit in self.edits.items():
            edit.setText(values.get(key, ""))

    def _collect_values(self) -> dict[str, str]:
        """
        Collect the current form values from the dialog widgets.

        Args:
                None: This method does not accept additional arguments beyond the instance context.

        Steps:
            1. Read the inputs required to  collect values.
            2. Perform the operations needed to  collect values.
            3. Return the resulting value or update the relevant application state.

        Returns:
                dict[str, str]: The form values collected from the dialog widgets.
        """
        return {key: edit.text().strip() for key, edit in self.edits.items()}

    def _settings_from_form(self) -> Settings:
        """
        Build a Settings object from the values currently entered in the dialog.

        Args:
                None: This method does not accept additional arguments beyond the instance context.

        Steps:
            1. Read the inputs required to  settings from form.
            2. Perform the operations needed to  settings from form.
            3. Return the resulting value or update the relevant application state.

        Returns:
                Settings: The settings object created from the current form values.
        """
        values = self._collect_values()
        try:
            bpn_timeout = int(values.get("BPN_DISCOVERY_TIMEOUT_SECONDS", "30") or "30")
            bpdm_timeout = int(values.get("BPDM_TIMEOUT_SECONDS", "30") or "30")
            dtr_timeout = int(values.get("DTR_TIMEOUT_SECONDS", "30") or "30")
        except ValueError as exc:
            raise ValueError("Timeout settings must be integer numbers.") from exc

        return Settings(
            mock_mode=False,
            dataspace_version=values.get("CX_DATASPACE_VERSION", "saturn") or "saturn",
            connector_base_url=values.get("CX_CONNECTOR_BASE_URL", ""),
            connector_management_path=values.get("CX_CONNECTOR_MANAGEMENT_PATH", "/management") or "/management",
            connector_api_key=values.get("CX_CONNECTOR_API_KEY", ""),
            discovery_auth_url=values.get("CX_DISCOVERY_AUTH_URL", ""),
            discovery_realm=values.get("CX_DISCOVERY_REALM", ""),
            discovery_client_id=values.get("CX_DISCOVERY_CLIENT_ID", ""),
            discovery_client_secret=values.get("CX_DISCOVERY_CLIENT_SECRET", ""),
            discovery_finder_url=values.get("CX_DISCOVERY_FINDER_URL", ""),
            bpn_discovery_base_url=values.get("BPN_DISCOVERY_BASE_URL", ""),
            bpn_discovery_api_path=values.get("BPN_DISCOVERY_API_PATH", "/api/v1.0/search") or "/api/v1.0/search",
            bpn_discovery_timeout_seconds=bpn_timeout,
            bpn_discovery_api_key=values.get("BPN_DISCOVERY_API_KEY", ""),
            bpn_discovery_material_number_type=values.get("BPN_DISCOVERY_MATERIAL_NUMBER_TYPE", "materialNumber") or "materialNumber",
            bpdm_pool_base_url=values.get("BPDM_POOL_BASE_URL", ""),
            bpdm_pool_api_path=values.get("BPDM_POOL_API_PATH", "/pool/v6") or "/pool/v6",
            bpdm_timeout_seconds=bpdm_timeout,
            bpdm_api_key=values.get("BPDM_API_KEY", ""),
            dtr_asset_link_search_path=values.get("DTR_ASSET_LINK_SEARCH_PATH", "/lookup/shells") or "/lookup/shells",
            dtr_timeout_seconds=dtr_timeout,
            cmp_lookup_mode=values.get("CMP_LOOKUP_MODE", "planned-part-twin") or "planned-part-twin",
            cmp_fixed_aas_id=values.get("CMP_FIXED_AAS_ID", ""),
        )

    def _missing_required_labels(self, settings: Settings) -> list[str]:
        """
        Return the human-readable labels of the required configuration fields that are missing.

        Args:
                settings (Settings): The runtime settings used to configure the service or client.

        Steps:
            1. Read the inputs required to  missing required labels.
            2. Perform the operations needed to  missing required labels.
            3. Return the resulting value or update the relevant application state.

        Returns:
                list[str]: The human-readable labels of the required fields that are still missing.
        """
        return [Settings.label_for_env_key(key) for key in settings.missing_real_mode_fields()]

    def on_validate(self) -> None:
        """
        Validate the current dialog values and show the validation result to the user.

        Args:
                None: This method does not accept additional arguments beyond the instance context.

        Steps:
            1. Read the inputs required to on validate.
            2. Perform the operations needed to on validate.
            3. Return the resulting value or update the relevant application state.

        Returns:
                None: The value returned by this method.
        """
        try:
            settings = self._settings_from_form()
        except Exception as exc:
            QMessageBox.warning(self, "Invalid configuration", str(exc))
            return

        missing = self._missing_required_labels(settings)
        if missing:
            bullets = "\n".join(f"- {label}" for label in missing)
            message = (
                "Real mode is not configured yet. Please fill in the minimum required fields:\n\n"
                f"{bullets}"
            )
            self.status_label.setText(message)
            QMessageBox.information(self, "Configuration incomplete", message)
            return

        message = (
            "Real mode minimum configuration looks complete.\n"
            "Optional BPN Discovery settings are still recommended if users should resolve supplier BPNLs "
            "from material numbers automatically."
        )
        self.status_label.setText(message)
        QMessageBox.information(self, "Configuration valid", message)

    def on_save(self) -> None:
        """
        Persist the current configuration values and close the dialog when validation succeeds.

        Args:
                None: This method does not accept additional arguments beyond the instance context.

        Steps:
            1. Read the inputs required to on save.
            2. Perform the operations needed to on save.
            3. Return the resulting value or update the relevant application state.

        Returns:
                None: The value returned by this method.
        """
        try:
            settings = self._settings_from_form()
        except Exception as exc:
            QMessageBox.warning(self, "Invalid configuration", str(exc))
            return

        saved_path = settings.save_to_env_file(self.env_path)
        missing = self._missing_required_labels(settings)
        if missing:
            bullets = "\n".join(f"- {label}" for label in missing)
            message = (
                f"Configuration was saved to {saved_path}, but real mode is still incomplete.\n\n"
                "Please fill in the minimum required fields:\n"
                f"{bullets}"
            )
            self.status_label.setText(message)
            QMessageBox.warning(self, "Configuration saved but incomplete", message)
            return

        message = f"Configuration saved successfully to {saved_path}."
        self.status_label.setText(message)
        QMessageBox.information(self, "Configuration saved", message)
