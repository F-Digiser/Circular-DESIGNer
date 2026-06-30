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
from pathlib import Path
from typing import Any


DEFAULT_DATABASE: dict[str, Any] = {"materials": {}}


def load_materials_database(path: str | Path) -> dict[str, Any]:
    """
    Load the materials database from a JSON file.

    Args:
            path (str | Path): The relative API path to call.

    Steps:
        1. Read the inputs required to load materials database.
        2. Perform the operations needed to load materials database.
        3. Return the resulting value or update the relevant application state.

    Returns:
            dict: The loaded materials database structure.
    """
    p = Path(path)
    if not p.exists():
        return {"materials": {}}
    data = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Materials database must be a JSON object.")
    materials = data.get("materials")
    if materials is None:
        data["materials"] = {}
    elif not isinstance(materials, dict):
        raise ValueError("Materials database field 'materials' must be a JSON object.")
    return data


def merge_material_output(database: dict[str, Any], new_output: dict[str, Any]) -> dict[str, Any]:
    """
    Merge one output payload into the in-memory materials database structure.

    Args:
            database (dict[str, Any]): The database used by this method.
            new_output (dict[str, Any]): The new output used by this method.

    Steps:
        1. Read the inputs required to merge material output.
        2. Perform the operations needed to merge material output.
        3. Return the resulting value or update the relevant application state.

    Returns:
            dict: The updated materials database structure.
    """
    if not isinstance(database, dict):
        raise ValueError("Database must be a JSON object.")
    if not isinstance(new_output, dict):
        raise ValueError("New output must be a JSON object.")

    db_materials = database.setdefault("materials", {})
    if not isinstance(db_materials, dict):
        raise ValueError("Database field 'materials' must be a JSON object.")

    new_materials = new_output.get("materials", {})
    if not isinstance(new_materials, dict):
        raise ValueError("Output field 'materials' must be a JSON object.")

    db_materials.update(new_materials)
    return database


def save_materials_database(path: str | Path, database: dict[str, Any]) -> None:
    """
    Perform the operation required to save materials database.

    Args:
            path (str | Path): The relative API path to call.
            database (dict[str, Any]): The database used by this method.

    Steps:
        1. Read the inputs required to save materials database.
        2. Perform the operations needed to save materials database.
        3. Return the resulting value or update the relevant application state.

    Returns:
            None: The value returned by this method.
    """
    p = Path(path)
    if p.parent and not p.parent.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(database, indent=2, ensure_ascii=False), encoding="utf-8")
