from setuptools import setup, find_packages

setup(
    name="infraguardian",
    version="2026.11.1",
    description="Static analysis, FinOps auditing, and automated remediation for Cloud IaC",
    author="InfraGuardian Open Source Community",
    packages=find_packages(),
    install_requires=[
        "pyyaml>=6.0.2",
        "requests>=2.32.3",
    ],
    entry_points={
        "console_scripts": [
            "infraguardian=infraguardian.cli:main",
        ],
    },
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Security",
        "Topic :: System :: Systems Administration",
    ],
)