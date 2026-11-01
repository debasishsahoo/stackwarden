# InfraGuardian

- Version: 2026.11.1
- Date: 01/11/26
- License: Apache 2.0

InfraGuardian is a static analysis and remediation tool built for DevOps, Platform, and Cloud Architecture teams. It shifts infrastructure policy compliance, FinOps cost auditing, and energy-aware cloud standards directly into developer git branches by scanning Terraform declarations, compiled plans, and Kubernetes manifests.

---

## Core Capabilities

1. Static Policy Evaluation
Verifies infrastructure code against security baselines (such as open inbound security groups and unconfined container contexts) and cost control frameworks (such as unmonitored compute instance sizing and undefined Kubernetes CPU/memory requests).

2. Native Pipeline Integration
Provides deterministic exit codes and flexible formatting options (standard console output, JSON streams, and Markdown summaries) for continuous integration systems.

3. Automated Patch Generation via API Credits
Leverages user-supplied LLM API credits to convert detected misconfigurations into valid unified diff patches, reducing engineering remediation time.

---

## Installation

### Installation via Source
Ensure Python 3.10 or higher is installed:

```bash
git clone https://github.com/your-org/infraguardian.git
cd infraguardian
pip install -r requirements.txt
pip install -e .
