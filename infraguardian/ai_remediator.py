"""
Consumes API credits to produce Unified Diff patches via LLM API endpoints.
Updated as of 01/11/26.
"""

import json
import urllib.request
import urllib.error
from typing import Dict, Any, Optional

class AIRemediator:
    def __init__(self, api_key: Optional[str] = None, endpoint: str = "https://api.openai.com/v1/chat/completions"):
        self.api_key = api_key
        self.endpoint = endpoint

    def is_available(self) -> bool:
        return bool(self.api_key and len(self.api_key.strip()) > 0)

    def generate_fix(self, finding_data: Dict[str, Any], snippet: str) -> str:
        if not self.is_available():
            return "AI Remediation skipped: No API key or active credit pool configured."

        prompt = (
            f"Role: Enterprise DevOps and FinOps Infrastructure Architect.\n"
            f"Task: Generate a corrective patch for this configuration issue.\n\n"
            f"Audit Date: 01/11/26\n"
            f"Rule ID: {finding_data.get('rule_id')}\n"
            f"Severity: {finding_data.get('severity')}\n"
            f"Description: {finding_data.get('description')}\n"
            f"File: {finding_data.get('file_path')}\n"
            f"Context: {finding_data.get('context')}\n\n"
            f"Original Source Content:\n{snippet}\n\n"
            f"Constraint: Respond ONLY with a valid Unified Diff. Do not add markdown backticks, conversational preamble, or explanations."
        )

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "User-Agent": "InfraGuardian/2026.11.1"
        }

        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are an automated code remediation utility that outputs raw unified diff syntax exclusively."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.1,
            "max_tokens": 600,
        }

        try:
            req = urllib.request.Request(
                self.endpoint,
                data=json.dumps(payload).encode("utf-8"),
                headers=headers,
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=20) as response:
                body = response.read().decode("utf-8")
                res_data = json.loads(body)
                return res_data["choices"][0]["message"]["content"].strip()
        except urllib.error.HTTPError as e:
            return f"Credit/API validation failure: HTTP {e.code} - {e.reason}"
        except urllib.error.URLError as e:
            return f"Endpoint network reachability failure: {e.reason}"
        except Exception as e:
            return f"Automated generation fault: {str(e)}"