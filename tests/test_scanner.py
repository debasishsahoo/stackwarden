"""
Formats and presents scan results for console terminals, JSON feeds, and Markdown documents.
Updated as of 01/11/26.
"""

import json
from typing import List
from .scanner import Finding

class Reporter:
    @staticmethod
    def to_terminal(findings: List[Finding]) -> str:
        if not findings:
            return "Scan complete. All security and cost controls satisfied. Zero violations detected."

        lines = [
            "------------------------------------------------------------------------------",
            "INFRAGUARDIAN QUALITY AUDIT REPORT - 01/11/26",
            "------------------------------------------------------------------------------",
            ""
        ]

        for idx, f in enumerate(findings, 1):
            lines.extend([
                f"[{idx}] {f.severity} | {f.rule_id} | {f.category}",
                f"    Target:      {f.file_path}",
                f"    Violation:   {f.description}",
                f"    Evidence:    {f.context}",
                f"    Guidance:    {f.remediation_hint}",
                "------------------------------------------------------------------------------"
            ])

        lines.append(f"Audit Summary: {len(findings)} finding(s) require review.")
        return "\n".join(lines)

    @staticmethod
    def to_json(findings: List[Finding]) -> str:
        data = [f.to_dict() for f in findings]
        return json.dumps({
            "version": "2026.11.1",
            "audit_date": "01/11/26",
            "findings_count": len(findings),
            "findings": data
        }, indent=2)

    @staticmethod
    def to_markdown(findings: List[Finding]) -> str:
        lines = [
            "# InfraGuardian IaC Compliance Audit Report",
            "",
            "- Audit Date: 01/11/26",
            f"- Total Detected Findings: {len(findings)}",
            "",
            "| Rule ID | Severity | Category | Target File | Description |",
            "|---|---|---|---|---|"
        ]

        for f in findings:
            lines.append(
                f"| {f.rule_id} | {f.severity} | {f.category} | `{f.file_path}` | {f.description} |"
            )

        return "\n".join(lines)