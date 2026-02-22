#!/usr/bin/env python3
"""Static syntax evaluator for the Code3D DSL."""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple


DEFINE_RE = re.compile(r"^\s*define\s+([A-Za-z_]\w*)\s*:\s*([A-Za-z_]\w*)\s*$")
LEADING_WS_RE = re.compile(r"^\s*")

BUILTIN_RANGE_ARITIES = {1, 2, 3}
BUILTIN_FILTER_ARITIES = {2}
BUILTIN_CONSTS = {"True", "False", "None"}
SORT_ALLOWED_KEYWORDS = {"key", "reverse"}

SENTINEL_MISSING = object()

CHECKED_RULES = [
    "define_top_block",
    "define_type_validation",
    "syntax_subset",
    "symbol_resolution",
    "call_name_and_arity",
    "sort_usage",
    "loop_control_flow",
]


@dataclass(frozen=True)
class TypeInfo:
    base_types: Set[str]
    array_item_types: Set[str]

    @staticmethod
    def unknown() -> "TypeInfo":
        return TypeInfo(base_types=set(), array_item_types=set())


@dataclass(frozen=True)
class OverloadInfo:
    arity: int
    return_types: Set[str]


@dataclass
class LanguageSpec:
    object_types: Set[str]
    object_aliases: Dict[str, str]
    global_functions: Dict[str, List[OverloadInfo]]
    object_methods: Dict[str, Dict[str, List[OverloadInfo]]]
    object_properties: Dict[str, Dict[str, TypeInfo]]
    method_index: Dict[str, List[Tuple[str, OverloadInfo]]]

    def normalize_object_type(self, type_name: str) -> Optional[str]:
        return self.object_aliases.get(type_name.lower())


def split_union(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, str):
        pieces = value.split("|")
    elif isinstance(value, list):
        pieces = []
        for entry in value:
            pieces.extend(str(entry).split("|"))
    else:
        return []
    normalized = [piece.strip().lower() for piece in pieces if piece and piece.strip()]
    return normalized


def parse_type_node(node: Any) -> TypeInfo:
    if isinstance(node, dict):
        base_types = set(split_union(node.get("type")))
        array_item_types: Set[str] = set()
        if "array" in base_types and node.get("items") is not None:
            nested = parse_type_node(node["items"])
            array_item_types.update(nested.base_types)
            array_item_types.update(nested.array_item_types)
        return TypeInfo(base_types=base_types, array_item_types=array_item_types)
    return TypeInfo(base_types=set(split_union(node)), array_item_types=set())


def parse_method_like(method_def: Dict[str, Any]) -> OverloadInfo:
    parameters = method_def.get("parameters") or []
    arity = len(parameters)
    output_type = method_def.get("outputType")
    return_types = set(split_union(output_type if output_type is not None else "unknown"))
    if not return_types:
        return_types = {"unknown"}
    return OverloadInfo(arity=arity, return_types=return_types)


def load_language_spec(schema_path: str) -> LanguageSpec:
    schema_text = Path(schema_path).read_text(encoding="utf-8")
    schema = json.loads(schema_text)

    raw_objects = schema.get("objects")
    raw_functions = schema.get("functions")
    if not isinstance(raw_objects, dict):
        raise ValueError(f"Schema '{schema_path}' is missing a valid objects map")
    if not isinstance(raw_functions, dict):
        raise ValueError(f"Schema '{schema_path}' is missing a valid functions map")

    object_types: Set[str] = set()
    object_aliases: Dict[str, str] = {}
    object_methods: Dict[str, Dict[str, List[OverloadInfo]]] = {}
    object_properties: Dict[str, Dict[str, TypeInfo]] = {}
    method_index: Dict[str, List[Tuple[str, OverloadInfo]]] = {}

    for object_name, object_def in raw_objects.items():
        canonical_name = str(object_name).lower()
        object_types.add(canonical_name)
        object_aliases[canonical_name] = canonical_name
        object_aliases[str(object_name).lower()] = canonical_name

        properties_map: Dict[str, TypeInfo] = {}
        methods_map: Dict[str, List[OverloadInfo]] = {}

        properties = object_def.get("properties") if isinstance(object_def, dict) else {}
        if isinstance(properties, dict):
            for property_name, property_def in properties.items():
                properties_map[str(property_name)] = parse_type_node(property_def)
        object_properties[canonical_name] = properties_map

        methods = object_def.get("methods") if isinstance(object_def, dict) else {}
        if isinstance(methods, dict):
            for method_name, method_def in methods.items():
                if not isinstance(method_def, dict):
                    continue
                overload = parse_method_like(method_def)
                method_key = str(method_name)
                methods_map.setdefault(method_key, []).append(overload)
                method_index.setdefault(method_key, []).append((canonical_name, overload))
        object_methods[canonical_name] = methods_map

    global_functions: Dict[str, List[OverloadInfo]] = {}
    for function_name, overload_defs in raw_functions.items():
        if not isinstance(overload_defs, list):
            continue
        overloads = []
        for overload_def in overload_defs:
            if not isinstance(overload_def, dict):
                continue
            overloads.append(parse_method_like(overload_def))
        global_functions[str(function_name)] = overloads

    return LanguageSpec(
        object_types=object_types,
        object_aliases=object_aliases,
        global_functions=global_functions,
        object_methods=object_methods,
        object_properties=object_properties,
        method_index=method_index,
    )


def diagnostic_from_node(
    code: str,
    message: str,
    node: Optional[ast.AST] = None,
    *,
    line: Optional[int] = None,
    column: Optional[int] = None,
    end_line: Optional[int] = None,
    end_column: Optional[int] = None,
) -> Dict[str, Any]:
    if node is not None:
        line = line if line is not None else getattr(node, "lineno", None)
        node_col = getattr(node, "col_offset", None)
        if column is None and node_col is not None:
            column = node_col + 1
        end_line = end_line if end_line is not None else getattr(node, "end_lineno", None)
        end_col = getattr(node, "end_col_offset", None)
        if end_column is None and end_col is not None:
            end_column = end_col + 1

    if line is None:
        line = 1
    if column is None:
        column = 1

    return {
        "code": code,
        "message": message,
        "line": int(line),
        "column": int(column),
        "end_line": int(end_line) if end_line is not None else None,
        "end_column": int(end_column) if end_column is not None else None,
    }


def preprocess_define_lines(
    code: str,
    spec: LanguageSpec,
) -> Tuple[str, Dict[str, Optional[Set[str]]], List[Dict[str, Any]]]:
    lines = code.split("\n")
    transformed_lines: List[str] = []
    declarations: Dict[str, Optional[Set[str]]] = {}
    errors: List[Dict[str, Any]] = []

    in_declaration_block = True

    for index, line in enumerate(lines):
        line_number = index + 1
        stripped = line.strip()
        indent = LEADING_WS_RE.match(line).group(0) if LEADING_WS_RE.match(line) else ""

        if stripped == "" or stripped.startswith("#"):
            transformed_lines.append(line)
            continue

        define_match = DEFINE_RE.match(line)
        starts_with_define = stripped.startswith("define")

        if in_declaration_block:
            if define_match:
                symbol_name = define_match.group(1)
                declared_type = define_match.group(2)
                normalized_type = spec.normalize_object_type(declared_type)

                if symbol_name in declarations:
                    errors.append(
                        diagnostic_from_node(
                            "DUPLICATE_DEFINE",
                            f"Duplicate declaration for '{symbol_name}'",
                            line=line_number,
                            column=line.find(symbol_name) + 1,
                        )
                    )
                else:
                    if normalized_type is None:
                        errors.append(
                            diagnostic_from_node(
                                "UNKNOWN_TYPE",
                                f"Unknown type '{declared_type}' in declaration of '{symbol_name}'",
                                line=line_number,
                                column=line.find(declared_type) + 1,
                            )
                        )
                        declarations[symbol_name] = None
                    else:
                        declarations[symbol_name] = {normalized_type}

                transformed_lines.append(f"{indent}{symbol_name} = None")
                continue

            if starts_with_define:
                errors.append(
                    diagnostic_from_node(
                        "INVALID_DEFINE_SYNTAX",
                        "Invalid define syntax. Expected: define name: Type",
                        line=line_number,
                        column=line.find("define") + 1,
                    )
                )
                transformed_lines.append(f"{indent}pass")
                continue

            in_declaration_block = False
            transformed_lines.append(line)
            continue

        if starts_with_define:
            errors.append(
                diagnostic_from_node(
                    "DEFINE_NOT_AT_TOP",
                    "define declarations are only allowed in the top declaration block",
                    line=line_number,
                    column=line.find("define") + 1,
                )
            )
            if define_match is None:
                errors.append(
                    diagnostic_from_node(
                        "INVALID_DEFINE_SYNTAX",
                        "Invalid define syntax. Expected: define name: Type",
                        line=line_number,
                        column=line.find("define") + 1,
                    )
                )
            transformed_lines.append(f"{indent}pass")
            continue

        transformed_lines.append(line)

    return "\n".join(transformed_lines), declarations, errors


class Validator:
    def __init__(
        self,
        spec: LanguageSpec,
        declarations: Dict[str, Optional[Set[str]]],
    ) -> None:
        self.spec = spec
        self.errors: List[Dict[str, Any]] = []
        self.warnings: List[Dict[str, Any]] = []
        self.loop_depth = 0
        self.scopes: List[Dict[str, Optional[Set[str]]]] = [dict(declarations)]

    def error(self, code: str, message: str, node: Optional[ast.AST] = None) -> None:
        self.errors.append(diagnostic_from_node(code, message, node))

    def warning(self, code: str, message: str, node: Optional[ast.AST] = None) -> None:
        self.warnings.append(diagnostic_from_node(code, message, node))

    def push_scope(self, symbols: Optional[Dict[str, Optional[Set[str]]]] = None) -> None:
        self.scopes.append(symbols or {})

    def pop_scope(self) -> None:
        self.scopes.pop()

    def resolve_symbol(self, name: str) -> object:
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return SENTINEL_MISSING

    def update_symbol_type(self, name: str, type_info: TypeInfo) -> None:
        if not type_info.base_types:
            return
        for scope in reversed(self.scopes):
            if name in scope:
                scope[name] = set(type_info.base_types)
                return

    def is_loaded_name_allowed(self, name: str) -> bool:
        if name in BUILTIN_CONSTS:
            return True
        return self.resolve_symbol(name) is not SENTINEL_MISSING

    def infer_expr_type(self, node: ast.AST) -> TypeInfo:
        if isinstance(node, ast.Name):
            resolved = self.resolve_symbol(node.id)
            if resolved is SENTINEL_MISSING or resolved is None:
                return TypeInfo.unknown()
            return TypeInfo(base_types=set(resolved), array_item_types=set())

        if isinstance(node, ast.Constant):
            value = node.value
            if isinstance(value, bool):
                return TypeInfo(base_types={"boolean"}, array_item_types=set())
            if isinstance(value, (int, float)):
                return TypeInfo(base_types={"number"}, array_item_types=set())
            if isinstance(value, str):
                return TypeInfo(base_types={"string"}, array_item_types=set())
            return TypeInfo.unknown()

        if isinstance(node, ast.List) or isinstance(node, ast.Tuple):
            item_types: Set[str] = set()
            for element in node.elts:
                item_types.update(self.infer_expr_type(element).base_types)
            return TypeInfo(base_types={"array"}, array_item_types=item_types)

        if isinstance(node, ast.Attribute):
            receiver_type = self.infer_expr_type(node.value)
            property_types: Set[str] = set()
            array_items: Set[str] = set()
            for receiver in receiver_type.base_types:
                property_map = self.spec.object_properties.get(receiver, {})
                property_type = property_map.get(node.attr)
                if property_type is None:
                    continue
                property_types.update(property_type.base_types)
                array_items.update(property_type.array_item_types)
            if property_types:
                return TypeInfo(base_types=property_types, array_item_types=array_items)
            return TypeInfo.unknown()

        if isinstance(node, ast.Subscript):
            value_type = self.infer_expr_type(node.value)
            if "array" in value_type.base_types and value_type.array_item_types:
                return TypeInfo(base_types=set(value_type.array_item_types), array_item_types=set())
            return TypeInfo.unknown()

        if isinstance(node, ast.Compare):
            return TypeInfo(base_types={"boolean"}, array_item_types=set())

        if isinstance(node, ast.BoolOp):
            return TypeInfo(base_types={"boolean"}, array_item_types=set())

        if isinstance(node, ast.Lambda):
            return TypeInfo(base_types={"function"}, array_item_types=set())

        if isinstance(node, ast.Call):
            return self.infer_call_type(node)

        return TypeInfo.unknown()

    def infer_call_type(self, node: ast.Call) -> TypeInfo:
        if isinstance(node.func, ast.Name):
            name = node.func.id
            if name == "range":
                return TypeInfo(base_types={"array"}, array_item_types=set())
            if name == "filter":
                return TypeInfo(base_types={"array"}, array_item_types=set())
            overloads = self.spec.global_functions.get(name, [])
            if not overloads:
                return TypeInfo.unknown()
            arity = len(node.args) + len(node.keywords)
            return_types: Set[str] = set()
            for overload in overloads:
                if overload.arity == arity:
                    return_types.update(overload.return_types)
            if return_types:
                return TypeInfo(base_types=return_types, array_item_types=set())
            return TypeInfo.unknown()

        if isinstance(node.func, ast.Attribute):
            if node.func.attr == "sort":
                return TypeInfo(base_types={"void"}, array_item_types=set())
            receiver_types = self.infer_expr_type(node.func.value).base_types
            arity = len(node.args) + len(node.keywords)
            return_types: Set[str] = set()
            for receiver in receiver_types:
                method_map = self.spec.object_methods.get(receiver, {})
                for overload in method_map.get(node.func.attr, []):
                    if overload.arity == arity:
                        return_types.update(overload.return_types)
            if return_types:
                return TypeInfo(base_types=return_types, array_item_types=set())
            return TypeInfo.unknown()

        return TypeInfo.unknown()

    def validate(self, module: ast.Module) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        for statement in module.body:
            self.check_stmt(statement)
        return self.errors, self.warnings

    def check_stmt(self, node: ast.stmt) -> None:
        if isinstance(node, ast.Assign):
            self.check_expr(node.value)
            value_type = self.infer_expr_type(node.value)
            for target in node.targets:
                self.check_assignment_target(target)
                for name in self.extract_target_names(target):
                    self.update_symbol_type(name, value_type)
            return

        if isinstance(node, ast.AugAssign):
            self.check_expr(node.value)
            self.check_augassign_target(node.target)
            return

        if isinstance(node, ast.Expr):
            self.check_expr(node.value)
            return

        if isinstance(node, ast.For):
            self.check_for(node)
            return

        if isinstance(node, ast.While):
            self.check_expr(node.test)
            self.loop_depth += 1
            for child in node.body:
                self.check_stmt(child)
            self.loop_depth -= 1
            for child in node.orelse:
                self.check_stmt(child)
            return

        if isinstance(node, ast.If):
            self.check_expr(node.test)
            for child in node.body:
                self.check_stmt(child)
            for child in node.orelse:
                self.check_stmt(child)
            return

        if isinstance(node, ast.Pass):
            return

        if isinstance(node, ast.Break):
            if self.loop_depth <= 0:
                self.error("UNSUPPORTED_SYNTAX_NODE", "break is only allowed inside loops", node)
            return

        if isinstance(node, ast.Continue):
            if self.loop_depth <= 0:
                self.error("UNSUPPORTED_SYNTAX_NODE", "continue is only allowed inside loops", node)
            return

        self.error(
            "UNSUPPORTED_SYNTAX_NODE",
            f"Unsupported statement syntax: {type(node).__name__}",
            node,
        )

    def check_for(self, node: ast.For) -> None:
        self.check_expr(node.iter)
        iterable_type = self.infer_expr_type(node.iter)
        target_names = self.extract_target_names(node.target)
        if target_names is None:
            self.error(
                "UNSUPPORTED_SYNTAX_NODE",
                "Unsupported for-loop target. Only name/tuple/list targets are allowed.",
                node.target,
            )
            target_names = []
        loop_symbol_types: Dict[str, Optional[Set[str]]] = {}
        inferred_item_types: Optional[Set[str]] = None
        if "array" in iterable_type.base_types and iterable_type.array_item_types:
            inferred_item_types = set(iterable_type.array_item_types)

        for name in target_names:
            loop_symbol_types[name] = set(inferred_item_types) if inferred_item_types else None

        self.push_scope(loop_symbol_types)
        self.loop_depth += 1
        for child in node.body:
            self.check_stmt(child)
        self.loop_depth -= 1
        for child in node.orelse:
            self.check_stmt(child)
        self.pop_scope()

    def extract_target_names(self, target: ast.AST) -> Optional[List[str]]:
        if isinstance(target, ast.Name):
            return [target.id]
        if isinstance(target, (ast.Tuple, ast.List)):
            names: List[str] = []
            for element in target.elts:
                sub_names = self.extract_target_names(element)
                if sub_names is None:
                    return None
                names.extend(sub_names)
            return names
        return None

    def check_augassign_target(self, target: ast.AST) -> None:
        if isinstance(target, ast.Name):
            if self.resolve_symbol(target.id) is SENTINEL_MISSING:
                self.error(
                    "UNDECLARED_SYMBOL",
                    f"Symbol '{target.id}' must be declared with define before use",
                    target,
                )
            return
        self.check_assignment_target(target)

    def check_assignment_target(self, target: ast.AST) -> None:
        if isinstance(target, ast.Name):
            return
        if isinstance(target, (ast.Tuple, ast.List)):
            for element in target.elts:
                self.check_assignment_target(element)
            return
        if isinstance(target, ast.Attribute):
            self.check_expr(target.value)
            return
        if isinstance(target, ast.Subscript):
            self.check_expr(target.value)
            self.check_slice(target.slice)
            return
        self.error(
            "UNSUPPORTED_SYNTAX_NODE",
            f"Unsupported assignment target: {type(target).__name__}",
            target,
        )

    def check_slice(self, node: ast.AST) -> None:
        if isinstance(node, ast.Slice):
            if node.lower is not None:
                self.check_expr(node.lower)
            if node.upper is not None:
                self.check_expr(node.upper)
            if node.step is not None:
                self.check_expr(node.step)
            return
        self.check_expr(node)

    def check_expr(self, node: ast.AST) -> None:
        if isinstance(node, ast.Name):
            if isinstance(node.ctx, ast.Load):
                if not self.is_loaded_name_allowed(node.id):
                    self.error(
                        "UNDECLARED_SYMBOL",
                        f"Symbol '{node.id}' must be declared with define before use",
                        node,
                    )
            return

        if isinstance(node, ast.Constant):
            return

        if isinstance(node, (ast.Tuple, ast.List)):
            for element in node.elts:
                self.check_expr(element)
            return

        if isinstance(node, ast.Dict):
            for key in node.keys:
                if key is not None:
                    self.check_expr(key)
            for value in node.values:
                self.check_expr(value)
            return

        if isinstance(node, ast.Attribute):
            self.check_expr(node.value)
            return

        if isinstance(node, ast.Subscript):
            self.check_expr(node.value)
            self.check_slice(node.slice)
            return

        if isinstance(node, ast.BinOp):
            self.check_expr(node.left)
            self.check_expr(node.right)
            return

        if isinstance(node, ast.UnaryOp):
            self.check_expr(node.operand)
            return

        if isinstance(node, ast.BoolOp):
            for value in node.values:
                self.check_expr(value)
            return

        if isinstance(node, ast.Compare):
            self.check_expr(node.left)
            for comparator in node.comparators:
                self.check_expr(comparator)
            return

        if isinstance(node, ast.Call):
            self.check_call(node)
            return

        if isinstance(node, ast.Lambda):
            lambda_scope: Dict[str, Optional[Set[str]]] = {}
            for arg in node.args.posonlyargs + node.args.args + node.args.kwonlyargs:
                lambda_scope[arg.arg] = None
            if node.args.vararg is not None:
                lambda_scope[node.args.vararg.arg] = None
            if node.args.kwarg is not None:
                lambda_scope[node.args.kwarg.arg] = None

            for default in node.args.defaults:
                self.check_expr(default)
            for default in node.args.kw_defaults:
                if default is not None:
                    self.check_expr(default)

            self.push_scope(lambda_scope)
            self.check_expr(node.body)
            self.pop_scope()
            return

        if isinstance(node, ast.IfExp):
            self.check_expr(node.test)
            self.check_expr(node.body)
            self.check_expr(node.orelse)
            return

        if isinstance(node, ast.JoinedStr):
            for value in node.values:
                self.check_expr(value)
            return

        if isinstance(node, ast.FormattedValue):
            self.check_expr(node.value)
            return

        self.error(
            "UNSUPPORTED_SYNTAX_NODE",
            f"Unsupported expression syntax: {type(node).__name__}",
            node,
        )

    def check_call(self, node: ast.Call) -> None:
        for argument in node.args:
            self.check_expr(argument)
        for keyword in node.keywords:
            self.check_expr(keyword.value)

        actual_arity = len(node.args) + len(node.keywords)

        if isinstance(node.func, ast.Name):
            function_name = node.func.id

            if function_name == "sort":
                self.error(
                    "INVALID_SORT_USAGE",
                    "sort must be called as a method, e.g. obj.sort(...)",
                    node.func,
                )
                return

            if function_name == "range":
                if actual_arity not in BUILTIN_RANGE_ARITIES:
                    self.error(
                        "INVALID_BUILTIN_USAGE",
                        "range expects 1 to 3 arguments",
                        node,
                    )
                return

            if function_name == "filter":
                if actual_arity not in BUILTIN_FILTER_ARITIES:
                    self.error(
                        "INVALID_BUILTIN_USAGE",
                        "filter expects exactly 2 arguments",
                        node,
                    )
                return

            overloads = self.spec.global_functions.get(function_name)
            if overloads is None:
                self.error(
                    "UNKNOWN_FUNCTION",
                    f"Unknown function '{function_name}'",
                    node.func,
                )
                return

            valid_arities = {overload.arity for overload in overloads}
            if actual_arity not in valid_arities:
                self.error(
                    "ARITY_MISMATCH",
                    f"Function '{function_name}' does not accept {actual_arity} argument(s)",
                    node,
                )
            return

        if isinstance(node.func, ast.Attribute):
            self.check_expr(node.func.value)
            method_name = node.func.attr

            if method_name == "sort":
                if len(node.args) != 0:
                    self.error(
                        "INVALID_SORT_USAGE",
                        "sort only accepts keyword arguments: key and reverse",
                        node,
                    )
                    return
                invalid_keywords = [
                    keyword.arg for keyword in node.keywords if keyword.arg not in SORT_ALLOWED_KEYWORDS
                ]
                if invalid_keywords:
                    self.error(
                        "INVALID_SORT_USAGE",
                        f"sort received unsupported keyword(s): {', '.join(invalid_keywords)}",
                        node,
                    )
                return

            receiver_types = self.infer_expr_type(node.func.value).base_types

            if receiver_types:
                method_overloads: List[OverloadInfo] = []
                for receiver_type in receiver_types:
                    method_overloads.extend(
                        self.spec.object_methods.get(receiver_type, {}).get(method_name, [])
                    )
                if not method_overloads:
                    self.error(
                        "UNKNOWN_METHOD",
                        f"Unknown method '{method_name}' for receiver type(s): {', '.join(sorted(receiver_types))}",
                        node.func,
                    )
                    return

                valid_arities = {overload.arity for overload in method_overloads}
                if actual_arity not in valid_arities:
                    self.error(
                        "ARITY_MISMATCH",
                        f"Method '{method_name}' does not accept {actual_arity} argument(s)",
                        node,
                    )
                return

            indexed = self.spec.method_index.get(method_name, [])
            if not indexed:
                self.error(
                    "UNKNOWN_METHOD",
                    f"Unknown method '{method_name}'",
                    node.func,
                )
                return

            valid_arities = {entry[1].arity for entry in indexed}
            if actual_arity not in valid_arities:
                self.error(
                    "ARITY_MISMATCH",
                    f"Method '{method_name}' does not accept {actual_arity} argument(s)",
                    node,
                )
                return

            self.warning(
                "UNKNOWN_RECEIVER_TYPE",
                f"Receiver type is unknown; '{method_name}' call arity validated only",
                node.func.value,
            )
            return

        self.error(
            "UNKNOWN_FUNCTION",
            "Unsupported callable target. Only direct function calls and object methods are allowed.",
            node.func,
        )


def evaluate_syntax(code: str, schema_path: str = "src/data/user-language.schema.json") -> Dict[str, Any]:
    spec = load_language_spec(schema_path)
    transformed_code, declarations, pre_errors = preprocess_define_lines(code, spec)

    errors: List[Dict[str, Any]] = list(pre_errors)
    warnings: List[Dict[str, Any]] = []

    try:
        module = ast.parse(transformed_code, mode="exec")
    except SyntaxError as exc:
        errors.append(
            diagnostic_from_node(
                "SYNTAX_ERROR",
                exc.msg,
                line=exc.lineno or 1,
                column=exc.offset or 1,
                end_line=getattr(exc, "end_lineno", None),
                end_column=getattr(exc, "end_offset", None),
            )
        )
        line_count = 0 if code == "" else code.count("\n") + 1
        return {
            "valid": False,
            "errors": errors,
            "warnings": warnings,
            "metadata": {
                "schema_path": str(schema_path),
                "line_count": line_count,
                "checked_rules": CHECKED_RULES,
            },
        }

    validator = Validator(spec=spec, declarations=declarations)
    validator_errors, validator_warnings = validator.validate(module)
    errors.extend(validator_errors)
    warnings.extend(validator_warnings)

    line_count = 0 if code == "" else code.count("\n") + 1
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "metadata": {
            "schema_path": str(schema_path),
            "line_count": line_count,
            "checked_rules": CHECKED_RULES,
        },
    }


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate Code3D DSL syntax")
    parser.add_argument("--code", help="Inline code string to evaluate")
    parser.add_argument("--file", dest="file_path", help="Path to file containing DSL code")
    parser.add_argument(
        "--schema",
        default="src/data/user-language.schema.json",
        help="Path to language schema JSON",
    )
    return parser.parse_args(list(argv))


def load_input_code(args: argparse.Namespace) -> str:
    if args.code is not None:
        return args.code
    if args.file_path is not None:
        return Path(args.file_path).read_text(encoding="utf-8")
    return sys.stdin.read()


def main(argv: Optional[Iterable[str]] = None) -> int:
    try:
        args = parse_args(argv if argv is not None else sys.argv[1:])
    except SystemExit:
        return 2

    try:
        code = load_input_code(args)
        report = evaluate_syntax(code, schema_path=args.schema)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 2

    print(json.dumps(report, indent=2))
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
