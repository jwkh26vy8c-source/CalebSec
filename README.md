# CalebSec Security Operations Platform

CalebSec is a modular SOC-style cybersecurity platform built with **FastAPI**, **SQLite**, and a modern web dashboard. It is designed to simulate real security operations workflows including SIEM monitoring, alert triage, IOC enrichment, MITRE ATT&CK mapping, phishing analysis, case tracking, audit logging, and analyst investigation notes.

---

## Project Purpose

This project was built as a hands-on cybersecurity portfolio project to demonstrate practical blue-team and SOC analyst skills. CalebSec simulates how security teams collect logs, review alerts, investigate suspicious activity, enrich indicators of compromise, and document findings.

---

## Key Features

- SIEM-style dashboard
- Security log ingestion
- Alert monitoring
- SOC alert triage workflow
- Threat intelligence / IOC lookup
- Local IOC risk scoring
- MITRE ATT&CK mapping
- Case management
- Analyst notes
- Audit trail
- Phishing detection capability
- Suspicious activity simulation
- Hosted demo mode
- FastAPI backend
- SQLite database
- Render deployment support

---

# SOC Modules

## Dashboard

The main dashboard provides a high-level overview of current alerts, logs, open cases, and security activity.

---

## SOC Alert Triage

The SOC triage module allows analysts to review simulated security alerts, assign statuses, add notes, and track investigation decisions.

### Supported statuses

- New
- Investigating
- Escalated
- Resolved
- False Positive

---

## Threat Intelligence

The threat intelligence module supports IOC lookups for:

- IP addresses
- Domains
- URLs
- Hashes
- Suspicious command strings

Each lookup produces:

- Risk score
- Verdict
- MITRE mapping
- Summary of suspicious indicators

---

## MITRE ATT&CK Mapping

Alerts and suspicious behaviors are mapped to MITRE ATT&CK techniques such as:

- T1110 – Brute Force
- T1059.001 – PowerShell
- T1071 – Application Layer Protocol
- T1566 – Phishing
- T1204 – User Execution

---

# Example Use Cases

- Investigating brute-force login activity
- Reviewing suspicious PowerShell behavior
- Identifying potential malware beaconing
- Analyzing phishing indicators
- Enriching suspicious IPs and domains
- Tracking analyst investigation notes
- Simulating SOC alert response workflows

---

# Technology Stack

- Python
- FastAPI
- SQLite
- Jinja2 Templates
- HTML/CSS
- Render
- GitHub

---

# Project Structure

```text
CalebSec/
├── main.py
├── database.py
├── detection.py
├── soc_extensions.py
├── threat_intel.py
├── templates/
│   ├── dashboard.html
│   ├── soc_triage.html
│   └── threat_intel.html
├── static/
├── docs/
│   ├── portfolio_summary.md
│   ├── soc_workflow.md
│   ├── threat_intel_workflow.md
│   └── resume_bullets.md
├── screenshots/
└── README.md
```

---

# How to Run Locally

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPO.git
cd YOUR-REPO
```

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
uvicorn main:app --reload
```

Open the app:

```text
http://127.0.0.1:8000
```

---

# Important Routes

```text
/                 Main dashboard
/alerts           Alerts
/logs             Logs
/cases            Cases
/audit            Audit trail
/mitre            MITRE & training
/soc-triage       SOC alert triage
/threat-intel     Threat intelligence lookup
```

---
# Screenshots

## Dashboard Overview
![Dashboard Overview](screenshots/calebsec-dashboard-overview.png)

## Admin Login
![Admin Login](screenshots/calebsec-admin-login.png)

## Alert Investigation
![Alert Investigation](screenshots/calebsec-alert-investigation.png)

## MITRE ATT&CK Training
![MITRE Training](screenshots/calebsec-mitre-training.png)





```text
screenshots/dashboard.png
screenshots/soc-triage.png
screenshots/threat-intel.png
screenshots/alerts.png
screenshots/cases.png
```

Then reference them like this:

```markdown
![Dashboard](screenshots/dashboard.png)
![SOC Triage](screenshots/soc-triage.png)
![Threat Intel](screenshots/threat-intel.png)
```

---

# Portfolio Value

This project demonstrates:

- Security operations knowledge
- Alert triage workflow understanding
- Threat intelligence concepts
- Detection engineering fundamentals
- MITRE ATT&CK familiarity
- Incident response documentation
- Python web application development
- Database-backed security tooling
- Practical blue-team project experience

---

# Interview Talking Points

- Built a FastAPI-based SOC platform to simulate alert triage and investigation workflows.
- Added IOC enrichment and threat scoring to support analyst decision-making.
- Implemented MITRE ATT&CK mapping for suspicious behaviors and detections.
- Developed case management and analyst note workflows similar to real SOC tooling.
- Added phishing analysis and suspicious activity simulations to demonstrate incident response concepts.
- Designed detection logic for brute force attacks, PowerShell abuse, malware beaconing, and credential theft scenarios.
- Implemented audit logging, role-protected actions, session security, and rate limiting.
- Deployed the platform publicly using Render and maintained the project through GitHub workflows.

---

# Future Improvements

Planned future enhancements include:

- Suricata integration
- Zeek integration
- SOAR automation
- Email header analysis
- Cloud security monitoring
- Threat feed integrations
- Analyst metrics dashboard

---

# Disclaimer

This project is for educational and portfolio purposes only. It is not intended to replace production-grade SIEM, SOAR, EDR, or threat intelligence platforms.
