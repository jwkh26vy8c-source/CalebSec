from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from calebsec.core.models import LogEvent


@dataclass
class SigmaRule:
    rule_id: str
    title: str
    level: str = "medium"
    detection: dict[str, Any] = field(default_factory=dict)
    filepath: str = ""

    def match(self, event: LogEvent) -> tuple[bool, list[str]]:
        event_dict = event.model_dump()
        event_dict.update(event.raw or {})
        condition = str(self.detection.get("condition", "selection")).strip()
        selections = {k: v for k, v in self.detection.items() if k != "condition"}

        def eval_selection(name: str) -> tuple[bool, list[str]]:
            selection = selections.get(name)
            if selection is None:
                return False, []
            return _match_selection(selection, event_dict)

        if " or " in condition:
            matched_fields: list[str] = []
            for part in [p.strip() for p in condition.split(" or ")]:
                ok, fields = eval_selection(part)
                if ok:
                    matched_fields.extend(fields)
            return bool(matched_fields), sorted(set(matched_fields))

        if " and " in condition:
            all_fields: list[str] = []
            for part in [p.strip() for p in condition.split(" and ")]:
                ok, fields = eval_selection(part)
                if not ok:
                    return False, []
                all_fields.extend(fields)
            return True, sorted(set(all_fields))

        return eval_selection(condition)


def _flatten_values(obj: Any) -> list[str]:
    if isinstance(obj, dict):
        vals: list[str] = []
        for v in obj.values():
            vals.extend(_flatten_values(v))
        return vals
    if isinstance(obj, list):
        vals = []
        for v in obj:
            vals.extend(_flatten_values(v))
        return vals
    return [str(obj)]


def _match_selection(selection: Any, event_dict: dict[str, Any]) -> tuple[bool, list[str]]:
    matched_fields: list[str] = []

    if isinstance(selection, list):
        haystack = " ".join(_flatten_values(event_dict)).lower()
        for keyword in selection:
            if str(keyword).lower() in haystack:
                matched_fields.append("keywords")
        return bool(matched_fields), matched_fields

    if not isinstance(selection, dict):
        return False, []

    for raw_field, expected in selection.items():
        field, _, modifier = raw_field.partition("|")
        actual = event_dict.get(field)
        if actual is None:
            return False, []

        expected_values = expected if isinstance(expected, list) else [expected]
        actual_s = str(actual).lower()

        if modifier == "contains":
            if not any(str(v).lower() in actual_s for v in expected_values):
                return False, []
            matched_fields.append(raw_field)
        else:
            if not any(str(actual) == str(v) for v in expected_values):
                return False, []
            matched_fields.append(raw_field)

    return True, matched_fields


def load_rules(rules_dir: Path) -> list[SigmaRule]:
    rules: list[SigmaRule] = []
    if not rules_dir.exists():
        return rules
    for path in sorted(rules_dir.glob("*.yml")) + sorted(rules_dir.glob("*.yaml")):
        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        rules.append(
            SigmaRule(
                rule_id=str(data.get("id") or path.stem),
                title=str(data.get("title") or path.stem),
                level=str(data.get("level") or "medium"),
                detection=data.get("detection") or {},
                filepath=str(path),
            )
        )
    return rules
