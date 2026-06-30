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

from .cli import _build_service
from .config import Settings
from .material_service import MaterialConsumerService


def build_service(settings: Settings | None = None) -> MaterialConsumerService:
    """
    Build and return the configured material consumer service instance.

    Args:
            settings (Settings | None): The runtime settings used to configure the service or client.

    Steps:
        1. Read the inputs required to build service.
        2. Perform the operations needed to build service.
        3. Return the resulting value or update the relevant application state.

    Returns:
            MaterialConsumerService: The configured material consumer service instance.
    """
    return _build_service(settings or Settings())
