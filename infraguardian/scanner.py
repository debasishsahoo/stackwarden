"""
Scans parsed JSON, YAML, and Terraform codebases against governance rules.
Updated as of 01/11/26.
"""

import json
import yaml
from pathlib import Path
from typing import List, Dict, Any
from .rules import BUILTIN_RULES

class Finding:
    def __init__(self, rule: Dict[str, Any], file_path: str, context: str):
        self.rule_id = rule["id"]
        self.severity = rule["severity"]
        self.category = rule["category"]
        self.description = rule["description"]
        self.remediation_hint = rule["remediation_hint"]
        self.file_path = file_path
        self.context = context

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "severity": self.severity,
            "category": self.category,
            "description": self.description,
            "remediation_hint": self.remediation_hint,
            "file_path": self.file_path,
            "context": self.context,
        }

class Scanner:
    def __init__(self, custom_rules: List[Dict[str, Any]] = None):
        self.rules = BUILTIN_RULES + (custom_rules or [])

    def scan_file(self, file_path: Path) -> List[Finding]:
        findings: List[Finding] = []
        if not file_path.exists():
            return findings

        if file_path.suffix in [".json", ".tfplan"]:
            findings.extend(self._scan_json(file_path))
        elif file_path.suffix in [".yaml", ".yml"]:
            findings.extend(self._scan_yaml(file_path))
        elif file_path.suffix == ".tf":
            findings.extend(self._scan_raw_tf(file_path))

        return findings

    def _scan_json(self, file_path: Path) -> List[Finding]:
        findings = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            findings.extend(self._evaluate_data(data, str(file_path)))
        except (json.JSONDecodeError, OSError):
            pass
        return findings

    def _scan_yaml(self, file_path: Path) -> List[Finding]:
        findings = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                docs = yaml.safe_load_all(f)
                for doc in docs:
                    if isinstance(doc, dict):
                        findings.extend(self._evaluate_data(doc, str(file_path)))
        except (yaml.YAMLError, OSError):
            pass
        return findings

    def _scan_raw_tf(self, file_path: Path) -> List[Finding]:
        findings = []
        try:
            content = file_path.read_text(encoding="utf-8")
            for rule in self.rules:
                if rule["target"] != "terraform":
                    continue
                for val in rule.get("forbidden_values", []):
                    if str(val) in content and rule["resource"] in content:
                        findings.append(Finding(rule, str(file_path), f"Direct token match detected: {val}"))
        except OSError:
            pass
        return findings

    def _evaluate_data(self, data: Any, file_path: str) -> List[Finding]:
        findings = []

        def recurse(node: Any):
            if isinstance(node, dict):
                for rule in self.rules:
                    target_res = rule.get("resource")
                    if target_res and (target_res in str(node.get("type", "")) or target_res in str(node.get("kind", ""))):
                        field = rule.get("field")
                        if field and field in node:
                            field_val = node[field]
                            for bad_val in rule.get("forbidden_values", []):
                                if bad_val == field_val or (isinstance(field_val, list) and bad_val in field_val):
                                    findings.append(Finding(rule, file_path, f"Field '{field}' matches disallowed value: {bad_val}"))
                            for flagged in rule.get("flagged_values", []):
                                if flagged == field_val:
                                    findings.append(Finding(rule, file_path, f"Field '{field}' triggered advisory review: {flagged}"))
                for v in node.values():
                    recurse(v)
            elif isinstance(node, list):
                for item in node:
                    recurse(item)

        recurse(data)
        return findings