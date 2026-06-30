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

import os
import uvicorn


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
    host = os.getenv("API_HOST", "127.0.0.1")
    port = int(os.getenv("API_PORT", "8000"))
    uvicorn.run("cx_material_consumer.api:app", host=host, port=port, reload=False)


if __name__ == "__main__":
    main()
