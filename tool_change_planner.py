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
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple


@dataclass(frozen=True)
class ConnectionEdge:
    """
    Represents one unique connection edge between two parts.

    Class-Level Constants:
        None.

    Attributes:
        a (str): The first part name in normalized edge order.
        b (str): The second part name in normalized edge order.
        connection_type (str): The assigned connection type between the two parts.
        tool (str): The tool required to sever the connection.
        amount (int): The quantity of this connection type between the two parts.

    Methods:
        None. This dataclass is used as an immutable data container.
    """
    a: str
    b: str
    connection_type: str
    tool: str
    amount: int


@dataclass
class ToolChangeResult:
    """
    Stores the outcome of a full tool change planning computation.

    Class-Level Constants:
        None.

    Attributes:
        tool_change_count (int): Number of tool changes required by the computed plan.
        tools_used (List[str]): Sorted list of distinct tools required by the input data.
        tool_order (List[str]): Order in which tools are selected by the planner.
        part_sequence (List[str]): Valid removal sequence for parts based on predecessor constraints.
        actions (List[Dict[str, Any]]): Ordered action log describing tool selections, severing, and removals.
        edge_count (int): Number of unique deduplicated connection edges.
        distinct_tool_count (int): Number of distinct tools used across all edges.

    Methods:
        to_dict(): Convert the result object into a plain dictionary.
    """
    tool_change_count: int
    tools_used: List[str]
    tool_order: List[str]
    part_sequence: List[str]
    actions: List[Dict[str, Any]]
    edge_count: int
    distinct_tool_count: int

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the result object into a serializable dictionary.

        Args:
            None.

        Steps:
            1. Read the dataclass fields from the current instance.
            2. Convert the dataclass into a dictionary using `asdict`.
            3. Return the generated dictionary.

        Returns:
            Dict[str, Any]: Dictionary representation of the planning result.

        Notes:
            - Nested dataclass content is also converted recursively by `asdict`.
        """
        return asdict(self)


class ToolChangeComputationError(RuntimeError):
    """
    Raised when tool change planning cannot be completed from the provided data.

    Class-Level Constants:
        None.

    Attributes:
        None. This exception class inherits all data from `RuntimeError`.

    Methods:
        None. This class is used only as a custom exception type.
    """
    pass


def load_python_literal_file(path: str | Path) -> Any:
    """
    Load and parse a Python-literal file.

    Args:
        path (str | Path): Path to a file containing a Python literal structure.

    Steps:
        1. Read the file content as UTF-8 text.
        2. Parse the text using `ast.literal_eval`.
        3. Return the parsed Python object.

    Returns:
        Any: Parsed object loaded from the Python-literal file.

    Notes:
        - This helper expects files formatted as valid Python literals rather than strict JSON.
    """
    raw = Path(path).read_text(encoding='utf-8')
    return ast.literal_eval(raw)


def extract_component_list(payload: Any) -> List[Dict[str, Any]]:
    """
    Extract a component list from one of the supported payload structures.

    Args:
        payload (Any): Input payload containing component definitions.

    Steps:
        1. Return the payload directly when it is already a list of component dictionaries.
        2. Check for a top-level `components` list when the payload is a dictionary.
        3. Check for a top-level `data` list containing entries with `components`.
        4. Collect and return all component dictionaries discovered in the supported layouts.
        5. Raise `ToolChangeComputationError` when the payload structure is unsupported.

    Returns:
        List[Dict[str, Any]]: Extracted list of component dictionaries.

    Notes:
        - Supported layouts are a plain list, a dictionary with `components`,
          or a dictionary with `data` entries that each contain `components`.
    """
    if isinstance(payload, list):
        return [c for c in payload if isinstance(c, dict)]

    if isinstance(payload, dict):
        if isinstance(payload.get('components'), list):
            return [c for c in payload['components'] if isinstance(c, dict)]

        data = payload.get('data')
        if isinstance(data, list):
            components: List[Dict[str, Any]] = []
            for entry in data:
                if isinstance(entry, dict) and isinstance(entry.get('components'), list):
                    components.extend(c for c in entry['components'] if isinstance(c, dict))
            return components

    raise ToolChangeComputationError(
        "Unsupported file structure. Expected a list of components, a dict with 'components', "
        "or a dict with 'data' entries containing 'components'."
    )


def iter_components_recursive(component: Dict[str, Any]) -> Iterable[Dict[str, Any]]:
    """
    Recursively yield a component and all nested child components.

    Args:
        component (Dict[str, Any]): Root component dictionary to traverse.

    Steps:
        1. Yield the current component.
        2. Read the nested `components` list from the current component.
        3. Recursively yield each child dictionary and its descendants.

    Returns:
        Iterable[Dict[str, Any]]: Generator of component dictionaries in depth-first order.

    Notes:
        - Non-dictionary child entries are ignored.
    """
    yield component
    for child in component.get('components', []) or []:
        if isinstance(child, dict):
            yield from iter_components_recursive(child)


def is_container_only(component: Dict[str, Any]) -> bool:
    """
    Determine whether a component acts only as a hierarchy container.

    Args:
        component (Dict[str, Any]): Component dictionary to evaluate.

    Steps:
        1. Check whether the component has child components.
        2. Check whether the component defines its own `disassembly_parameters`.
        3. Return True when the component has children but no disassembly parameters.
        4. Return False for removable parts or nodes without children.

    Returns:
        bool: True when the component is a container-only hierarchy node, otherwise False.

    Notes:
        - Container-only nodes are excluded from the removable part sequence by default.
    """
    has_children = bool(component.get('components'))
    has_disassembly = isinstance(component.get('disassembly_parameters'), dict)
    return has_children and not has_disassembly


def flatten_components(components: Sequence[Dict[str, Any]], *, include_container_nodes: bool = False) -> List[Dict[str, Any]]:
    """
    Flatten nested component trees into a single list.

    Args:
        components (Sequence[Dict[str, Any]]): Root components to traverse.
        include_container_nodes (bool): Whether to include hierarchy container nodes in the result.

    Steps:
        1. Iterate through each root component.
        2. Traverse each component recursively.
        3. Include every node when `include_container_nodes` is True.
        4. Otherwise skip container-only nodes.
        5. Return the flattened component list.

    Returns:
        List[Dict[str, Any]]: Flattened list of component dictionaries.

    Notes:
        - This helper normalizes nested assembly structures before planning begins.
    """
    flattened: List[Dict[str, Any]] = []
    for component in components:
        for node in iter_components_recursive(component):
            if include_container_nodes or not is_container_only(node):
                flattened.append(node)
    return flattened


def _as_positive_int(value: Any, default: int = 1) -> int:
    """
    Convert a value to a positive integer with fallback behavior.

    Args:
        value (Any): Input value to convert.
        default (int): Fallback value returned when conversion fails or produces a non-positive result.

    Steps:
        1. Attempt to convert the input to a float and round it.
        2. Cast the rounded value to an integer.
        3. Return the parsed value when it is greater than zero.
        4. Return the fallback value when parsing fails or the result is not positive.

    Returns:
        int: A positive integer parsed from the input or the fallback value.

    Notes:
        - Any exception during conversion causes the fallback value to be returned.
    """
    try:
        parsed = int(round(float(value)))
        return parsed if parsed > 0 else default
    except Exception:
        return default


def build_predecessor_map(components: Sequence[Dict[str, Any]]) -> Dict[str, Set[str]]:
    """
    Build the predecessor dependency map used for part removal ordering.

    Args:
        components (Sequence[Dict[str, Any]]): Flattened component dictionaries.

    Steps:
        1. Collect all valid component names.
        2. Initialize an empty predecessor set for each named component.
        3. Read the `covered_by` list from each component's disassembly parameters.
        4. Add valid predecessor names to the matching component entry.
        5. Return the completed predecessor mapping.

    Returns:
        Dict[str, Set[str]]: Mapping of part names to prerequisite parts that must be removed first.

    Notes:
        - Self-dependencies and names not present in the component list are ignored.
    """
    names = {c.get('name') for c in components if c.get('name')}
    predecessors: Dict[str, Set[str]] = {name: set() for name in names}

    for component in components:
        name = component.get('name')
        if name not in names:
            continue
        covered_by = (component.get('disassembly_parameters', {}).get('covered_by', []) or [])
        for predecessor in covered_by:
            if predecessor in names and predecessor != name:
                predecessors[name].add(predecessor)

    return predecessors


def build_unique_edges(components: Sequence[Dict[str, Any]]) -> List[ConnectionEdge]:
    """
    Build a deduplicated list of connection edges across all components.

    Args:
        components (Sequence[Dict[str, Any]]): Flattened component dictionaries.

    Steps:
        1. Collect all valid component names.
        2. Iterate through each component's assigned connections.
        3. Normalize each edge by sorting the connected part names.
        4. Read the required tool and connection amount for each connection type.
        5. Deduplicate mirrored definitions so each logical edge appears once.
        6. Validate that duplicate edge definitions do not disagree on the required tool.
        7. Return the sorted list of unique connection edges.

    Returns:
        List[ConnectionEdge]: Deduplicated connection edge objects.

    Notes:
        - When duplicate mirrored entries disagree on the tool, a `ToolChangeComputationError` is raised.
        - For duplicate edges, the maximum amount value is preserved.
    """
    names = {c.get('name') for c in components if c.get('name')}
    dedup: Dict[Tuple[str, str, str], Dict[str, Any]] = {}

    for component in components:
        a = component.get('name')
        if a not in names:
            continue

        assigned = component.get('disassembly_parameters', {}).get('assigned_connections', {}) or {}
        if not isinstance(assigned, dict):
            continue

        for b, typed_connections in assigned.items():
            if b not in names or b == a:
                continue
            if not isinstance(typed_connections, dict):
                continue

            for connection_type, info in typed_connections.items():
                info = info if isinstance(info, dict) else {}
                tool = str(info.get('tool') or 'UNKNOWN_TOOL')
                amount = _as_positive_int(info.get('amount', 1), default=1)
                key = (min(a, b), max(a, b), str(connection_type))

                if key not in dedup:
                    dedup[key] = {'tool': tool, 'amount': amount}
                else:
                    existing_tool = dedup[key]['tool']
                    if existing_tool != tool:
                        raise ToolChangeComputationError(
                            f"Conflicting tool definitions for edge {key}: '{existing_tool}' vs '{tool}'."
                        )
                    dedup[key]['amount'] = max(dedup[key]['amount'], amount)

    return [
        ConnectionEdge(a=key[0], b=key[1], connection_type=key[2], tool=value['tool'], amount=value['amount'])
        for key, value in sorted(dedup.items())
    ]


def _topological_part_order(predecessors: Dict[str, Set[str]]) -> List[str]:
    """
    Compute a valid part removal order from predecessor constraints.

    Args:
        predecessors (Dict[str, Set[str]]): Mapping of parts to the parts that must be removed first.

    Steps:
        1. Initialize the remaining and removed part sets.
        2. Identify parts whose predecessor requirements are already satisfied.
        3. Pick the lexicographically first ready part for deterministic output.
        4. Add the selected part to the removal order and mark it as removed.
        5. Repeat until all parts are ordered or no valid next step exists.
        6. Raise `ToolChangeComputationError` if a cycle or unsatisfied dependency is detected.

    Returns:
        List[str]: Deterministic topological order of removable parts.

    Notes:
        - The result is deterministic because ready nodes are sorted before selection.
    """
    remaining = set(predecessors)
    removed: Set[str] = set()
    order: List[str] = []

    while remaining:
        ready = sorted(name for name in remaining if predecessors[name].issubset(removed))
        if not ready:
            raise ToolChangeComputationError(
                'covered_by contains a cycle or unsatisfied dependency; no valid part order exists.'
            )
        pick = ready[0]
        order.append(pick)
        remaining.remove(pick)
        removed.add(pick)

    return order


def compute_min_tool_changes(
    components: Sequence[Dict[str, Any]],
    *,
    count_initial_pick_as_change: bool = False,
    include_container_nodes: bool = False,
) -> ToolChangeResult:
    """
    Compute a deterministic full-disassembly plan and minimal tool change count.

    Args:
        components (Sequence[Dict[str, Any]]): Component dictionaries used to derive dependencies and connections.
        count_initial_pick_as_change (bool): Whether the first tool selection should count as a tool change.
        include_container_nodes (bool): Whether container-only hierarchy nodes should remain in the part sequence.

    Steps:
        1. Flatten the component structure into a planning-ready list.
        2. Build the predecessor dependency map for removable parts.
        3. Build the unique connection edge list and determine the required tools.
        4. Compute a valid topological removal order for parts.
        5. Derive the tool order from the sorted list of distinct tools.
        6. Compute the tool change count based on the selected counting rule.
        7. Generate ordered action entries for tool selection, severing connections, and removing parts.
        8. Return the complete `ToolChangeResult`.

    Returns:
        ToolChangeResult: Structured result containing the computed plan, counts, and action sequence.

    Notes:
        - Container-only nodes are ignored by default so nested assemblies behave like flat files.
        - When no tools are required, the tool order is empty and the tool change count is zero.
        - The current implementation uses sorted distinct tools as the deterministic tool order.
    """
    flat_components = flatten_components(list(components), include_container_nodes=include_container_nodes)
    predecessors = build_predecessor_map(flat_components)
    edges = build_unique_edges(flat_components)

    distinct_tools = sorted({edge.tool for edge in edges})
    part_order = _topological_part_order(predecessors)

    if not distinct_tools:
        tool_change_count = 0
        tool_order: List[str] = []
    else:
        tool_order = distinct_tools[:]
        tool_change_count = len(tool_order) if count_initial_pick_as_change else max(0, len(tool_order) - 1)

    actions: List[Dict[str, Any]] = []
    current_tool: Optional[str] = None
    for tool in tool_order:
        if current_tool is None:
            actions.append({'action': 'select_tool', 'tool': tool})
        elif current_tool != tool:
            actions.append({'action': 'tool_change', 'from': current_tool, 'to': tool})
        current_tool = tool

        severed_edges = [
            {
                'a': edge.a,
                'b': edge.b,
                'connection_type': edge.connection_type,
                'amount': edge.amount,
            }
            for edge in edges
            if edge.tool == tool
        ]
        if severed_edges:
            actions.append({'action': 'sever_connections', 'tool': tool, 'edges': severed_edges})

    for part_name in part_order:
        actions.append({'action': 'remove_part', 'part': part_name})

    return ToolChangeResult(
        tool_change_count=tool_change_count,
        tools_used=distinct_tools,
        tool_order=tool_order,
        part_sequence=part_order,
        actions=actions,
        edge_count=len(edges),
        distinct_tool_count=len(distinct_tools),
    )


__all__ = [
    'ConnectionEdge',
    'ToolChangeResult',
    'ToolChangeComputationError',
    'load_python_literal_file',
    'extract_component_list',
    'iter_components_recursive',
    'is_container_only',
    'flatten_components',
    'build_predecessor_map',
    'build_unique_edges',
    'compute_min_tool_changes',
]
