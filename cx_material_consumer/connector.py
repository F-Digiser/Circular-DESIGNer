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

from .exceptions import DiscoveryError
from .models import DIGITAL_TWIN_REGISTRY_TYPE


class ConnectorRuntime:
    """
    Wrap connector-discovery and DTR-session setup logic for real Catena-X mode.

    Class-Level Constants:
        None.

    Attributes:
        connection_manager (Any): Stores the connection manager value.
        consumer_connector_service (Any): Stores the consumer connector service value.
        discovery_service (Any): Stores the discovery service value.

    Methods:
        __init__(): Initialize the object with the provided dependencies, default values, and internal state.
        find_connector_by_bpn(): Resolve the connector endpoint for a supplier BPNL.
        open_dtr_session(): Open a connector-backed session to the supplier Digital Twin Registry.
    """
    def __init__(
        self,
        dataspace_version: str,
        connector_base_url: str,
        connector_management_path: str,
        connector_headers: dict[str, str],
        discovery_auth_url: str,
        discovery_realm: str,
        discovery_client_id: str,
        discovery_client_secret: str,
        discovery_finder_url: str,
    ) -> None:
        """
        Initialize the object with the provided dependencies, default values, and internal state.

        Args:
                dataspace_version (str): The dataspace version used by this method.
                connector_base_url (str): The connector base url used by this method.
                connector_management_path (str): The connector management path used by this method.
                connector_headers (dict[str, str]): The connector headers used by this method.
                discovery_auth_url (str): The discovery auth url used by this method.
                discovery_realm (str): The discovery realm used by this method.
                discovery_client_id (str): The discovery client id used by this method.
                discovery_client_secret (str): The discovery client secret used by this method.
                discovery_finder_url (str): The discovery finder url used by this method.

        Steps:
            1. Read the provided dependencies and configuration values.
            2. Store them on the instance for later use.
            3. Prepare any internal state required by later method calls.

        Returns:
                None: This initializer configures the instance state in place.
        """
        try:
            from tractusx_sdk.dataspace.managers.connection import MemoryConnectionManager
            from tractusx_sdk.dataspace.managers import OAuth2Manager
            from tractusx_sdk.dataspace.services.connector import ServiceFactory
            from tractusx_sdk.dataspace.services.discovery import DiscoveryFinderService, ConnectorDiscoveryService
        except Exception as exc:
            raise DiscoveryError(
                "tractusx-sdk is not installed or could not be imported. "
                "Install dependencies for real Catena-X mode, or enable MOCK_MODE=true for local testing."
            ) from exc

        self.connection_manager = MemoryConnectionManager()
        self.consumer_connector_service = ServiceFactory.get_connector_consumer_service(
            dataspace_version=dataspace_version,
            base_url=connector_base_url,
            dma_path=connector_management_path,
            headers=connector_headers,
            connection_manager=self.connection_manager,
        )

        oauth = OAuth2Manager(
            auth_url=discovery_auth_url,
            realm=discovery_realm,
            clientid=discovery_client_id,
            clientsecret=discovery_client_secret,
        )
        discovery_finder_service = DiscoveryFinderService(
            url=discovery_finder_url,
            oauth=oauth,
        )
        self.discovery_service = ConnectorDiscoveryService(
            oauth=oauth,
            discovery_finder_service=discovery_finder_service,
        )

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
        try:
            result = self.discovery_service.find_connector_by_bpn(bpnl)
            if isinstance(result, list) and result:
                return result[0]["address"]
            if isinstance(result, dict):
                return result["address"]
            raise DiscoveryError(f"No connector found for {bpnl}")
        except Exception as exc:
            raise DiscoveryError(f"Connector discovery failed for {bpnl}: {exc}") from exc

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
        try:
            dataplane_url, access_token = self.consumer_connector_service.do_dsp(
                counter_party_id=supplier_bpnl,
                counter_party_address=supplier_dsp_endpoint,
                filter_expression=self.consumer_connector_service.get_filter_expression(
                    key="'http://purl.org/dc/terms/type'.'@id'",
                    operator="=",
                    value=DIGITAL_TWIN_REGISTRY_TYPE,
                ),
                policies=[],
            )
            return dataplane_url, access_token
        except Exception as exc:
            raise DiscoveryError(f"Failed to open DTR DSP session: {exc}") from exc
