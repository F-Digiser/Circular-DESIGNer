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

import ast
import copy
from pathlib import Path
from pprint import pformat
from typing import Any, Dict, Iterable, List, MutableMapping, Tuple


Component = Dict[str, Any]
ConnectionPayload = Dict[str, Any]


def iter_components_recursive(items: Iterable[Component]):
    """
    Yield every component contained in a nested component tree.

    Args:
        items (Iterable[Component]): Top-level components whose nested ``components``
            lists should also be traversed.

    Steps:
        1. Iterate through each component in the provided collection.
        2. Yield the current component before examining its descendants.
        3. Read its child components and recursively yield every nested component.

    Returns:
        Iterator[Component]: A generator that yields each component in depth-first,
            parent-before-child order.

    Notes:
        - Uses recursion to traverse arbitrarily nested ``components`` collections.
        - Treats a missing or falsey ``components`` field as an empty child list.
    """
    for item in items:
        yield item
        children = item.get("components", []) or []
        yield from iter_components_recursive(children)



def ensure_disassembly_structure(component: MutableMapping[str, Any]) -> Dict[str, Any]:
    """
    Ensure that a component contains the dictionaries required for connection data.

    Args:
        component (MutableMapping[str, Any]): Component record to inspect and, when
            necessary, populate with connection-related dictionaries.

    Steps:
        1. Create ``disassembly_parameters`` as an empty dictionary when absent.
        2. Validate that ``disassembly_parameters`` is dictionary-like data.
        3. Create and validate the nested ``assigned_connections`` dictionary.

    Returns:
        Dict[str, Any]: The validated ``disassembly_parameters`` dictionary belonging
            to the component.

    Notes:
        - Mutates ``component`` by adding missing nested dictionaries.
        - Raises ``TypeError`` when an existing required structure is not a dictionary.
    """
    dp = component.setdefault("disassembly_parameters", {})
    if not isinstance(dp, dict):
        raise TypeError(f"disassembly_parameters must be a dict for component {component.get('name')!r}")

    ac = dp.setdefault("assigned_connections", {})
    if not isinstance(ac, dict):
        raise TypeError(f"assigned_connections must be a dict for component {component.get('name')!r}")

    return dp



def build_component_lookup(project_data: Dict[str, Any]) -> Dict[str, Component]:
    """
    Create a name-based lookup table for all components in project data.

    Args:
        project_data (Dict[str, Any]): Project structure containing assemblies under
            ``data`` and components nested below each assembly.

    Steps:
        1. Read the top-level assembly records from ``project_data["data"]``.
        2. Traverse each assembly's nested component tree recursively.
        3. Add named components to a dictionary keyed by their unique names.
        4. Reject duplicate component names to keep connection resolution unambiguous.

    Returns:
        Dict[str, Component]: Mapping from each component name to its component record.

    Notes:
        - Components with no name are ignored.
        - Uses ``iter_components_recursive()`` for depth-first traversal.
        - Raises ``ValueError`` when more than one component uses the same name.
    """
    top_level_items = project_data.get("data", []) or []
    components_by_name: Dict[str, Component] = {}

    for assembly in top_level_items:
        for component in iter_components_recursive(assembly.get("components", []) or []):
            name = component.get("name")
            if not name:
                continue
            if name in components_by_name:
                raise ValueError(f"Duplicate component name found: {name!r}. Names must be unique.")
            components_by_name[name] = component

    return components_by_name



def get_assigned_connections(component: Component) -> Dict[str, Any]:
    """
    Return the mutable assigned-connections dictionary for a component.

    Args:
        component (Component): Component whose assigned connections are required.

    Steps:
        1. Ensure the component has valid disassembly and connection structures.
        2. Retrieve the nested ``assigned_connections`` value.
        3. Validate the retrieved value before returning it to the caller.

    Returns:
        Dict[str, Any]: Mutable mapping of target component names to connection
            payload dictionaries.

    Notes:
        - Calls ``ensure_disassembly_structure()`` and can therefore mutate the component.
        - Raises ``TypeError`` when ``assigned_connections`` is not a dictionary.
    """
    dp = ensure_disassembly_structure(component)
    assigned = dp["assigned_connections"]
    if not isinstance(assigned, dict):
        raise TypeError(f"assigned_connections must be a dict for component {component.get('name')!r}")
    return assigned



def snapshot_edges(components_by_name: Dict[str, Component]) -> List[Tuple[str, str, ConnectionPayload]]:
    """
    Capture all directed connection entries before any connection data is changed.

    Args:
        components_by_name (Dict[str, Component]): Lookup mapping component names to
            their component records.

    Steps:
        1. Inspect the assigned-connections mapping of every source component.
        2. Validate each source mapping and each individual connection payload.
        3. Deep-copy every source-target-payload tuple into a snapshot list.

    Returns:
        List[Tuple[str, str, ConnectionPayload]]: Independent copies of all directed
            edges in the current component graph.

    Notes:
        - Normalizes a ``None`` assigned-connections mapping or payload to an empty dict.
        - Uses ``copy.deepcopy()`` so subsequent mutation does not alter the snapshot.
        - Raises ``TypeError`` for malformed mappings or payloads.
    """
    edges: List[Tuple[str, str, ConnectionPayload]] = []

    for source_name, source_component in components_by_name.items():
        assigned = source_component.get("disassembly_parameters", {}).get("assigned_connections", {})
        if assigned is None:
            assigned = {}
        if not isinstance(assigned, dict):
            raise TypeError(f"assigned_connections must be a dict for component {source_name!r}")

        for target_name, payload in assigned.items():
            if payload is None:
                payload = {}
            if not isinstance(payload, dict):
                raise TypeError(
                    f"Connection payload from {source_name!r} to {target_name!r} must be a dict"
                )
            edges.append((source_name, target_name, copy.deepcopy(payload)))

    return edges



def mirror_empty_assigned_connections(project_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Mirror empty assigned-connection payloads onto their counterpart components.

    Args:
        project_data (Dict[str, Any]): Project data containing nested components and
            their assigned-connection mappings.

    Steps:
        1. Build a lookup of all components and snapshot the original directed edges.
        2. Identify edges whose payload is empty, representing deletion intent.
        3. Locate each existing counterpart component for those empty edges.
        4. Set the reverse edge payload to an empty dictionary.

    Returns:
        Dict[str, Any]: The same project dictionary after mirrored empty payloads have
            been applied.

    Notes:
        - Mutates ``project_data`` in place.
        - Only empty payloads are mirrored; non-empty source payloads are ignored.
        - An existing non-empty reverse payload is overwritten with ``{}``.
        - References to counterpart components absent from the project are skipped.
    """
    components_by_name = build_component_lookup(project_data)
    original_edges = snapshot_edges(components_by_name)

    for source_name, target_name, payload in original_edges:
        if payload:
            continue

        target_component = components_by_name.get(target_name)
        if target_component is None:
            continue

        target_assigned = get_assigned_connections(target_component)
        target_assigned[source_name] = {}

    return project_data



def delete_empty_assigned_connections(project_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Remove assigned-connection entries whose payloads are empty dictionaries.

    Args:
        project_data (Dict[str, Any]): Project data containing nested components and
            assigned-connection entries to clean.

    Steps:
        1. Build a lookup of all named components in the project.
        2. Retrieve each component's assigned-connections dictionary.
        3. Collect target names mapped to empty dictionary payloads.
        4. Delete each collected target entry from its source component.

    Returns:
        Dict[str, Any]: The same project dictionary after empty entries are removed.

    Notes:
        - Mutates ``project_data`` in place.
        - Removes only empty dictionary payloads and leaves non-empty entries unchanged.
        - Keeps an emptied ``assigned_connections`` mapping as ``{}``.
    """
    components_by_name = build_component_lookup(project_data)

    for component in components_by_name.values():
        assigned = get_assigned_connections(component)
        empty_targets = [
            target_name
            for target_name, payload in assigned.items()
            if isinstance(payload, dict) and not payload
        ]

        for target_name in empty_targets:
            del assigned[target_name]

    return project_data



def mirror_empty_assigned_connections_and_delete(project_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Propagate empty connection deletion intent and remove the resulting empty entries.

    Args:
        project_data (Dict[str, Any]): Project data containing potentially asymmetric
            empty assigned-connection entries.

    Steps:
        1. Mirror every empty connection payload to the corresponding reverse edge.
        2. Delete all empty assigned-connection entries from the component graph.
        3. Return the cleaned, synchronized project structure.

    Returns:
        Dict[str, Any]: The same project dictionary after empty connection pairs have
            been mirrored and removed.

    Notes:
        - Mutates ``project_data`` in place.
        - Combines ``mirror_empty_assigned_connections()`` with
            ``delete_empty_assigned_connections()``.
    """
    mirror_empty_assigned_connections(project_data)
    delete_empty_assigned_connections(project_data)
    return project_data



def synchronize_assigned_connections_by_richer_side(project_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Synchronize each component pair using the payload with more connection types.

    Args:
        project_data (Dict[str, Any]): Project data containing directed assigned
            connections that may differ between counterpart components.

    Steps:
        1. Build a lookup for all named components and initialize processed-pair tracking.
        2. Inspect each directed connection whose counterpart component exists.
        3. Compare the number of connection types on both directions of the pair.
        4. Deep-copy the richer payload to both sides when one side has more entries.
        5. Leave equal-sized payloads unchanged because no unambiguous winner exists.

    Returns:
        Dict[str, Any]: The same project dictionary with asymmetric pairs synchronized
            where a richer payload can be determined.

    Notes:
        - Mutates ``project_data`` in place.
        - Counts payload dictionary keys as connection types; missing or empty sides count as zero.
        - Processes each unordered component pair only once.
        - Skips missing counterpart components and raises ``TypeError`` for invalid payload types.
    """
    components_by_name = build_component_lookup(project_data)
    processed_pairs = set()

    for source_name, source_component in components_by_name.items():
        source_assigned = source_component.get("disassembly_parameters", {}).get("assigned_connections", {})
        if source_assigned is None:
            source_assigned = {}
        if not isinstance(source_assigned, dict):
            raise TypeError(f"assigned_connections must be a dict for component {source_name!r}")

        candidate_targets = set(source_assigned.keys())

        for target_name in list(candidate_targets):
            if target_name not in components_by_name:
                continue

            pair_key = tuple(sorted((source_name, target_name)))
            if pair_key in processed_pairs:
                continue
            processed_pairs.add(pair_key)

            target_component = components_by_name[target_name]

            source_assigned_live = get_assigned_connections(source_component)
            target_assigned_live = get_assigned_connections(target_component)

            payload_ab = source_assigned_live.get(target_name, {})
            payload_ba = target_assigned_live.get(source_name, {})

            if payload_ab is None:
                payload_ab = {}
            if payload_ba is None:
                payload_ba = {}

            if not isinstance(payload_ab, dict):
                raise TypeError(
                    f"Connection payload from {source_name!r} to {target_name!r} must be a dict"
                )
            if not isinstance(payload_ba, dict):
                raise TypeError(
                    f"Connection payload from {target_name!r} to {source_name!r} must be a dict"
                )

            count_ab = len(payload_ab)
            count_ba = len(payload_ba)

            if count_ab > count_ba:
                winner = copy.deepcopy(payload_ab)
            elif count_ba > count_ab:
                winner = copy.deepcopy(payload_ba)
            else:
                continue

            source_assigned_live[target_name] = copy.deepcopy(winner)
            target_assigned_live[source_name] = copy.deepcopy(winner)

    return project_data



def load_python_literal_file(path: str | Path) -> Dict[str, Any]:
    """
    Load project data stored as a Python literal representation.

    Args:
        path (str | Path): Path to a UTF-8 text file containing a Python literal
            dictionary structure.

    Steps:
        1. Convert the supplied path to a ``Path`` object.
        2. Read the full text content using UTF-8 encoding.
        3. Parse the text safely as Python literal data.

    Returns:
        Dict[str, Any]: Parsed project data read from the specified file.

    Notes:
        - Uses ``ast.literal_eval()`` rather than executing arbitrary Python code.
        - Parsing or file-system errors are propagated to the caller.
    """
    text = Path(path).read_text(encoding="utf-8")
    return ast.literal_eval(text)



def save_python_literal_file(data: Dict[str, Any], path: str | Path) -> None:
    """
    Write project data to a formatted Python literal text file.

    Args:
        data (Dict[str, Any]): Project data to serialize.
        path (str | Path): Destination path for the UTF-8 output file.

    Steps:
        1. Format the project dictionary as a readable Python literal string.
        2. Preserve dictionary insertion order while applying a fixed output width.
        3. Write the formatted representation to the destination path in UTF-8.

    Returns:
        None: The function writes to disk and does not return a value.

    Notes:
        - Uses ``pprint.pformat()`` with ``sort_dicts=False`` and a width of 100.
        - Existing content at ``path`` is overwritten.
    """
    Path(path).write_text(pformat(data, sort_dicts=False, width=100), encoding="utf-8")


if __name__ == "__main__":
    input_file = "input_mirror_assigned_components.txt"
    output_file = "output_mirror_assigned_components_generated.txt"

    data = load_python_literal_file(input_file)
    mirror_empty_assigned_connections_and_delete(data)
    synchronize_assigned_connections_by_richer_side(data)
    save_python_literal_file(data, output_file)
    print(f"Processed connections written to: {output_file}")
