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
import os
from pathlib import Path
from typing import Iterable


CONFIG_FIELD_LABELS: dict[str, str] = {
    "CX_DATASPACE_VERSION": "Dataspace version",
    "CX_CONNECTOR_BASE_URL": "Connector base URL",
    "CX_CONNECTOR_MANAGEMENT_PATH": "Connector management path",
    "CX_CONNECTOR_API_KEY": "Connector API key",
    "CX_DISCOVERY_AUTH_URL": "Discovery auth URL",
    "CX_DISCOVERY_REALM": "Discovery realm",
    "CX_DISCOVERY_CLIENT_ID": "Discovery client ID",
    "CX_DISCOVERY_CLIENT_SECRET": "Discovery client secret",
    "CX_DISCOVERY_FINDER_URL": "Discovery finder URL",
    "BPN_DISCOVERY_BASE_URL": "BPN Discovery base URL",
    "BPN_DISCOVERY_API_PATH": "BPN Discovery API path",
    "BPN_DISCOVERY_TIMEOUT_SECONDS": "BPN Discovery timeout (s)",
    "BPN_DISCOVERY_API_KEY": "BPN Discovery API key",
    "BPN_DISCOVERY_MATERIAL_NUMBER_TYPE": "BPN Discovery material-number key type",
    "BPDM_POOL_BASE_URL": "BPDM Pool base URL",
    "BPDM_POOL_API_PATH": "BPDM Pool API path",
    "BPDM_TIMEOUT_SECONDS": "BPDM timeout (s)",
    "BPDM_API_KEY": "BPDM API key",
    "DTR_ASSET_LINK_SEARCH_PATH": "DTR asset-link search path",
    "DTR_TIMEOUT_SECONDS": "DTR timeout (s)",
    "CMP_LOOKUP_MODE": "CMP lookup mode",
    "CMP_FIXED_AAS_ID": "CMP fixed AAS ID",
}

REQUIRED_REAL_MODE_ENV_KEYS: tuple[str, ...] = (
    "CX_CONNECTOR_BASE_URL",
    "CX_DISCOVERY_AUTH_URL",
    "CX_DISCOVERY_REALM",
    "CX_DISCOVERY_CLIENT_ID",
    "CX_DISCOVERY_CLIENT_SECRET",
    "CX_DISCOVERY_FINDER_URL",
    "BPDM_POOL_BASE_URL",
)

OPTIONALLY_RECOMMENDED_ENV_KEYS: tuple[str, ...] = (
    "BPN_DISCOVERY_BASE_URL",
    "BPN_DISCOVERY_API_PATH",
    "BPN_DISCOVERY_MATERIAL_NUMBER_TYPE",
)


def get_default_env_path() -> Path:
    """
    Return the default path of the environment file used by the desktop application.

    Args:
            None: This method does not accept additional arguments beyond the instance context.

    Steps:
        1. Read the inputs required to get default env path.
        2. Perform the operations needed to get default env path.
        3. Return the resulting value or update the relevant application state.

    Returns:
            Path: The value returned by this method.
    """
    explicit = os.getenv("CXMC_ENV_PATH")
    if explicit:
        return Path(explicit).expanduser().resolve()
    return Path(__file__).resolve().parent.parent / ".env"


def _candidate_dotenv_paths() -> list[Path]:
    """
    Yield candidate locations that may contain the environment configuration file.

    Args:
            None: This method does not accept additional arguments beyond the instance context.

    Steps:
        1. Read the inputs required to  candidate dotenv paths.
        2. Perform the operations needed to  candidate dotenv paths.
        3. Return the resulting value or update the relevant application state.

    Returns:
            list[Path]: The value returned by this method.
    """
    paths: list[Path] = []
    explicit = os.getenv("CXMC_ENV_PATH")
    if explicit:
        paths.append(Path(explicit).expanduser().resolve())
    cwd_path = Path.cwd() / ".env"
    project_path = get_default_env_path()
    for path in (cwd_path, project_path):
        resolved = path.expanduser().resolve()
        if resolved not in paths:
            paths.append(resolved)
    return paths


def _parse_env_lines(lines: Iterable[str]) -> dict[str, str]:
    """
    Parse dotenv file lines into a dictionary of key-value pairs.

    Args:
            lines (Iterable[str]): The lines used by this method.

    Steps:
        1. Read the inputs required to  parse env lines.
        2. Perform the operations needed to  parse env lines.
        3. Return the resulting value or update the relevant application state.

    Returns:
            dict[str, str]: The value returned by this method.
    """
    data: dict[str, str] = {}
    for raw_line in lines:
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        data[key.strip()] = value.strip()
    return data


def load_env_file(path: Path | None = None) -> dict[str, str]:
    """
    Load key-value pairs from an environment file.

    Args:
            path (Path | None): The relative API path to call.

    Steps:
        1. Read the inputs required to load env file.
        2. Perform the operations needed to load env file.
        3. Return the resulting value or update the relevant application state.

    Returns:
            dict[str, str]: The value returned by this method.
    """
    target = path or get_default_env_path()
    if not target.exists():
        return {}
    return _parse_env_lines(target.read_text(encoding="utf-8").splitlines())


def save_env_values(values: dict[str, str], path: Path | None = None) -> Path:
    """
    Write key-value pairs to an environment file while preserving a stable ordering.

    Args:
            values (dict[str, str]): The values used by this method.
            path (Path | None): The relative API path to call.

    Steps:
        1. Read the inputs required to save env values.
        2. Perform the operations needed to save env values.
        3. Return the resulting value or update the relevant application state.

    Returns:
            Path: The value returned by this method.
    """
    target = (path or get_default_env_path()).expanduser().resolve()
    existing = load_env_file(target)
    existing.update({k: v for k, v in values.items() if v is not None})
    target.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"{key}={existing[key]}" for key in sorted(existing)]
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return target


def _load_dotenv() -> None:
    """
    Load environment values from the discovered dotenv file candidates into the process environment.

    Args:
            None: This method does not accept additional arguments beyond the instance context.

    Steps:
        1. Read the inputs required to  load dotenv.
        2. Perform the operations needed to  load dotenv.
        3. Return the resulting value or update the relevant application state.

    Returns:
            None: The value returned by this method.
    """
    for dotenv_path in _candidate_dotenv_paths():
        if not dotenv_path.exists():
            continue
        for key, value in load_env_file(dotenv_path).items():
            os.environ.setdefault(key, value)
        break


_load_dotenv()


def _as_bool(value: str | None, default: bool = False) -> bool:
    """
    Convert an environment value into a boolean flag.

    Args:
            value (str | None): The value used by this method.
            default (bool): The default used by this method.

    Steps:
        1. Read the inputs required to  as bool.
        2. Perform the operations needed to  as bool.
        3. Return the resulting value or update the relevant application state.

    Returns:
            bool: The value returned by this method.
    """
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


@dataclass(frozen=True)
class Settings:
    """
    Store the runtime configuration values used to build clients and switch between mock mode and real Catena-X mode.

    Class-Level Constants:
        None.

    Attributes:
        mock_mode (bool): Stores the mock mode value.
        dataspace_version (str): Stores the dataspace version value.
        connector_base_url (str): Stores the connector base url value.
        connector_management_path (str): Stores the connector management path value.
        connector_api_key (str): Stores the connector api key value.
        discovery_auth_url (str): Stores the discovery auth url value.
        discovery_realm (str): Stores the discovery realm value.
        discovery_client_id (str): Stores the discovery client id value.
        discovery_client_secret (str): Stores the discovery client secret value.
        discovery_finder_url (str): Stores the discovery finder url value.
        bpn_discovery_base_url (str): Stores the bpn discovery base url value.
        bpn_discovery_api_path (str): Stores the bpn discovery api path value.
        bpn_discovery_timeout_seconds (int): Stores the bpn discovery timeout seconds value.
        bpn_discovery_api_key (str): Stores the bpn discovery api key value.
        bpn_discovery_material_number_type (str): Stores the bpn discovery material number type value.
        bpdm_pool_base_url (str): Stores the bpdm pool base url value.
        bpdm_pool_api_path (str): Stores the bpdm pool api path value.
        bpdm_timeout_seconds (int): Stores the bpdm timeout seconds value.
        bpdm_api_key (str): Stores the bpdm api key value.
        dtr_asset_link_search_path (str): Stores the dtr asset link search path value.
        dtr_timeout_seconds (int): Stores the dtr timeout seconds value.
        cmp_lookup_mode (str): Stores the cmp lookup mode value.
        cmp_fixed_aas_id (str): Stores the cmp fixed aas id value.

    Methods:
        connector_headers(): Return the HTTP headers used for connector-related requests.
        bpdm_headers(): Return the HTTP headers used for BPDM requests.
        bpn_discovery_headers(): Return the HTTP headers used for BPN discovery requests.
        required_real_mode_env_keys(): Return the configuration keys that must be set for real Catena-X mode.
        optional_real_mode_env_keys(): Return the supported configuration keys that are optional or advanced.
        label_for_env_key(): Return a user-friendly label for one environment key.
        missing_real_mode_fields(): Return the list of required real-mode configuration keys that are currently missing.
        to_env_dict(): Convert the settings object into a dictionary that can be written to an environment file.
        apply_to_environment(): Apply the current settings values to the process environment.
        save_to_env_file(): Persist the current settings values to an environment file.
    """
    mock_mode: bool = _as_bool(os.getenv("MOCK_MODE"), False)

    dataspace_version: str = os.getenv("CX_DATASPACE_VERSION", "saturn")
    connector_base_url: str = os.getenv("CX_CONNECTOR_BASE_URL", "")
    connector_management_path: str = os.getenv("CX_CONNECTOR_MANAGEMENT_PATH", "/management")
    connector_api_key: str = os.getenv("CX_CONNECTOR_API_KEY", "")

    discovery_auth_url: str = os.getenv("CX_DISCOVERY_AUTH_URL", "")
    discovery_realm: str = os.getenv("CX_DISCOVERY_REALM", "")
    discovery_client_id: str = os.getenv("CX_DISCOVERY_CLIENT_ID", "")
    discovery_client_secret: str = os.getenv("CX_DISCOVERY_CLIENT_SECRET", "")
    discovery_finder_url: str = os.getenv("CX_DISCOVERY_FINDER_URL", "")

    bpn_discovery_base_url: str = os.getenv("BPN_DISCOVERY_BASE_URL", "")
    bpn_discovery_api_path: str = os.getenv("BPN_DISCOVERY_API_PATH", "/api/v1.0/search")
    bpn_discovery_timeout_seconds: int = int(os.getenv("BPN_DISCOVERY_TIMEOUT_SECONDS", "30"))
    bpn_discovery_api_key: str = os.getenv("BPN_DISCOVERY_API_KEY", "")
    bpn_discovery_material_number_type: str = os.getenv("BPN_DISCOVERY_MATERIAL_NUMBER_TYPE", "materialNumber")

    bpdm_pool_base_url: str = os.getenv("BPDM_POOL_BASE_URL", "")
    bpdm_pool_api_path: str = os.getenv("BPDM_POOL_API_PATH", "/pool/v6")
    bpdm_timeout_seconds: int = int(os.getenv("BPDM_TIMEOUT_SECONDS", "30"))
    bpdm_api_key: str = os.getenv("BPDM_API_KEY", "")

    dtr_asset_link_search_path: str = os.getenv("DTR_ASSET_LINK_SEARCH_PATH", "/lookup/shells")
    dtr_timeout_seconds: int = int(os.getenv("DTR_TIMEOUT_SECONDS", "30"))

    cmp_lookup_mode: str = os.getenv("CMP_LOOKUP_MODE", "planned-part-twin")
    cmp_fixed_aas_id: str = os.getenv("CMP_FIXED_AAS_ID", "")

    def connector_headers(self) -> dict[str, str]:
        """
        Return the HTTP headers used for connector-related requests.

        Args:
                None: This method does not accept additional arguments beyond the instance context.

        Steps:
            1. Read the inputs required to connector headers.
            2. Perform the operations needed to connector headers.
            3. Return the resulting value or update the relevant application state.

        Returns:
                dict[str, str]: The HTTP headers used for connector requests.
        """
        headers = {"Content-Type": "application/json"}
        if self.connector_api_key:
            headers["X-Api-Key"] = self.connector_api_key
        return headers

    def bpdm_headers(self) -> dict[str, str]:
        """
        Return the HTTP headers used for BPDM requests.

        Args:
                None: This method does not accept additional arguments beyond the instance context.

        Steps:
            1. Read the inputs required to bpdm headers.
            2. Perform the operations needed to bpdm headers.
            3. Return the resulting value or update the relevant application state.

        Returns:
                dict[str, str]: The HTTP headers used for BPDM requests.
        """
        headers = {"Content-Type": "application/json"}
        if self.bpdm_api_key:
            headers["X-Api-Key"] = self.bpdm_api_key
        return headers

    def bpn_discovery_headers(self) -> dict[str, str]:
        """
        Return the HTTP headers used for BPN discovery requests.

        Args:
                None: This method does not accept additional arguments beyond the instance context.

        Steps:
            1. Read the inputs required to bpn discovery headers.
            2. Perform the operations needed to bpn discovery headers.
            3. Return the resulting value or update the relevant application state.

        Returns:
                dict[str, str]: The HTTP headers used for BPN discovery requests.
        """
        headers = {"Content-Type": "application/json"}
        if self.bpn_discovery_api_key:
            headers["X-Api-Key"] = self.bpn_discovery_api_key
        return headers

    @staticmethod
    def required_real_mode_env_keys() -> tuple[str, ...]:
        """
        Return the configuration keys that must be set for real Catena-X mode.

        Args:
                None: This method does not accept additional arguments beyond the instance context.

        Steps:
            1. Read the inputs required to required real mode env keys.
            2. Perform the operations needed to required real mode env keys.
            3. Return the resulting value or update the relevant application state.

        Returns:
                list[str]: The environment keys that are mandatory for real mode.
        """
        return REQUIRED_REAL_MODE_ENV_KEYS

    @staticmethod
    def optional_real_mode_env_keys() -> tuple[str, ...]:
        """
        Return the supported configuration keys that are optional or advanced.

        Args:
                None: This method does not accept additional arguments beyond the instance context.

        Steps:
            1. Read the inputs required to optional real mode env keys.
            2. Perform the operations needed to optional real mode env keys.
            3. Return the resulting value or update the relevant application state.

        Returns:
                list[str]: The supported configuration keys that are optional.
        """
        return OPTIONALLY_RECOMMENDED_ENV_KEYS

    @staticmethod
    def label_for_env_key(key: str) -> str:
        """
        Return a user-friendly label for one environment key.

        Args:
                key (str): The key used by this method.

        Steps:
            1. Read the inputs required to label for env key.
            2. Perform the operations needed to label for env key.
            3. Return the resulting value or update the relevant application state.

        Returns:
                str: The user-facing label for the requested environment key.
        """
        return CONFIG_FIELD_LABELS.get(key, key)

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
        values = self.to_env_dict()
        return [key for key in REQUIRED_REAL_MODE_ENV_KEYS if not values.get(key, "").strip()]

    def to_env_dict(self) -> dict[str, str]:
        """
        Convert the settings object into a dictionary that can be written to an environment file.

        Args:
                None: This method does not accept additional arguments beyond the instance context.

        Steps:
            1. Read the inputs required to to env dict.
            2. Perform the operations needed to to env dict.
            3. Return the resulting value or update the relevant application state.

        Returns:
                dict[str, str]: The settings represented as environment key-value pairs.
        """
        return {
            "MOCK_MODE": "true" if self.mock_mode else "false",
            "CX_DATASPACE_VERSION": self.dataspace_version,
            "CX_CONNECTOR_BASE_URL": self.connector_base_url,
            "CX_CONNECTOR_MANAGEMENT_PATH": self.connector_management_path,
            "CX_CONNECTOR_API_KEY": self.connector_api_key,
            "CX_DISCOVERY_AUTH_URL": self.discovery_auth_url,
            "CX_DISCOVERY_REALM": self.discovery_realm,
            "CX_DISCOVERY_CLIENT_ID": self.discovery_client_id,
            "CX_DISCOVERY_CLIENT_SECRET": self.discovery_client_secret,
            "CX_DISCOVERY_FINDER_URL": self.discovery_finder_url,
            "BPN_DISCOVERY_BASE_URL": self.bpn_discovery_base_url,
            "BPN_DISCOVERY_API_PATH": self.bpn_discovery_api_path,
            "BPN_DISCOVERY_TIMEOUT_SECONDS": str(self.bpn_discovery_timeout_seconds),
            "BPN_DISCOVERY_API_KEY": self.bpn_discovery_api_key,
            "BPN_DISCOVERY_MATERIAL_NUMBER_TYPE": self.bpn_discovery_material_number_type,
            "BPDM_POOL_BASE_URL": self.bpdm_pool_base_url,
            "BPDM_POOL_API_PATH": self.bpdm_pool_api_path,
            "BPDM_TIMEOUT_SECONDS": str(self.bpdm_timeout_seconds),
            "BPDM_API_KEY": self.bpdm_api_key,
            "DTR_ASSET_LINK_SEARCH_PATH": self.dtr_asset_link_search_path,
            "DTR_TIMEOUT_SECONDS": str(self.dtr_timeout_seconds),
            "CMP_LOOKUP_MODE": self.cmp_lookup_mode,
            "CMP_FIXED_AAS_ID": self.cmp_fixed_aas_id,
        }

    def apply_to_environment(self) -> None:
        """
        Apply the current settings values to the process environment.

        Args:
                None: This method does not accept additional arguments beyond the instance context.

        Steps:
            1. Read the inputs required to apply to environment.
            2. Perform the operations needed to apply to environment.
            3. Return the resulting value or update the relevant application state.

        Returns:
                None: The value returned by this method.
        """
        for key, value in self.to_env_dict().items():
            os.environ[key] = value

    def save_to_env_file(self, path: Path | None = None) -> Path:
        """
        Persist the current settings values to an environment file.

        Args:
                path (Path | None): The relative API path to call.

        Steps:
            1. Read the inputs required to save to env file.
            2. Perform the operations needed to save to env file.
            3. Return the resulting value or update the relevant application state.

        Returns:
                Path: The value returned by this method.
        """
        self.apply_to_environment()
        return save_env_values(self.to_env_dict(), path)
