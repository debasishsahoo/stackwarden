"""
Policy definitions for Terraform and Kubernetes configurations.
Updated as of 01/11/26.
"""

from typing import List, Dict, Any

BUILTIN_RULES: List[Dict[str, Any]] = [
    {
        "id": "SEC-TF-001",
        "target": "terraform",
        "resource": "aws_security_group",
        "field": "cidr_blocks",
        "forbidden_values": ["0.0.0.0/0"],
        "severity": "CRITICAL",
        "category": "Security",
        "description": "Security group authorizes unrestricted ingress from the public internet (0.0.0.0/0).",
        "remediation_hint": "Restrict ingress to dedicated corporate CIDRs or trusted internal IP ranges."
    },
    {
        "id": "SEC-TF-002",
        "target": "terraform",
        "resource": "aws_s3_bucket",
        "field": "acl",
        "forbidden_values": ["public-read", "public-read-write"],
        "severity": "HIGH",
        "category": "Security",
        "description": "S3 bucket configuration permits public access via legacy ACL settings.",
        "remediation_hint": "Set S3 bucket ACL to private and enable AWS S3 Public Access Block."
    },
    {
        "id": "COST-TF-001",
        "target": "terraform",
        "resource": "aws_instance",
        "field": "instance_type",
        "flagged_values": ["m5.12xlarge", "m5.24xlarge", "c5.18xlarge", "p4de.24xlarge"],
        "severity": "MEDIUM",
        "category": "FinOps",
        "description": "High-compute instance allocated without explicit justification tags, risking cost spikes.",
        "remediation_hint": "Evaluate latest Graviton instance families or confirm capacity reservation requirements."
    },
    {
        "id": "SEC-K8S-001",
        "target": "kubernetes",
        "resource": "Pod",
        "field": "privileged",
        "forbidden_values": [True],
        "severity": "CRITICAL",
        "category": "Security",
        "description": "Container executes in privileged mode, enabling host operating system escape vectors.",
        "remediation_hint": "Set securityContext.privileged to false and drop unnecessary Linux capabilities."
    },
    {
        "id": "COST-K8S-001",
        "target": "kubernetes",
        "resource": "Deployment",
        "field": "resources",
        "check_type": "presence",
        "severity": "LOW",
        "category": "FinOps",
        "description": "Missing resource requests and limits can lead to CPU throttling and unmetered node consumption.",
        "remediation_hint": "Define spec.containers[*].resources.requests and limits explicitly."
    }
]