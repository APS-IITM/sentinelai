# 🛡️ SentinelAI: Autonomous Agentic Security Operations & CTI Engine

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Splunk](https://img.shields.io/badge/Splunk-Enterprise-green)
![MCP](https://img.shields.io/badge/MCP-Agentic%20Protocol-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-brightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🚀 Overview

SentinelAI is an autonomous, AI-powered Security Operations and Cyber Threat Intelligence (CTI) platform built for the Splunk Agentic Ops Hackathon.

Traditional Security Operations Centers (SOCs) spend countless hours manually reviewing logs, correlating alerts, and creating incident reports. SentinelAI transforms this workflow into an intelligent, agent-driven ecosystem capable of:

* Continuous Splunk telemetry monitoring
* Real-time anomaly detection
* Autonomous threat hunting
* MITRE ATT&CK mapping
* Cyber Threat Intelligence (CTI) generation
* Agentic investigation using MCP
* Persistent intelligence storage

The platform combines machine learning, agentic reasoning, and security analytics to reduce analyst workload and accelerate incident response.

---

# 🎯 Problem Statement

Modern SOC teams face:

* Massive volumes of security logs
* Alert fatigue
* Slow threat investigation cycles
* Manual CTI report generation
* Limited contextual threat correlation

SentinelAI addresses these challenges by introducing autonomous agents capable of understanding, correlating, and investigating security events directly from Splunk telemetry.

---

# 🏗️ System Architecture

```text
                   +----------------------------------+
                   |       Human SOC Analyst          |
                   +----------------------------------+
                                    │
                                    ▼
                   +----------------------------------+
                   |       Streamlit Dashboard        |
                   +----------------------------------+
                     │                              ▲
                     │                              │
                     ▼                              │

+----------------------------------+
|      Threat Actor Simulator      |
|   (Brute Force, Scan, DoS)       |
+----------------------------------+
                     │
                     ▼

+----------------------------------+
|          Splunk SIEM             |
|    (Security Telemetry Logs)     |
+----------------------------------+
                     │
                     ▼

+----------------------------------+
|  Autonomous Splunk Data Daemon   |
|      (splunk_daemon.py)          |
+----------------------------------+
                     │
                     ▼

+----------------------------------+
|      Anomaly Detection Core      |
| Z-Score + Isolation Forest ML    |
+----------------------------------+
                     │
                     ▼

+----------------------------------+
|      Intelligence Engine         |
| MITRE Mapping & CTI Generation   |
+----------------------------------+
                     │
                     ▼

+----------------------------------+
|     Supabase Intelligence DB     |
+----------------------------------+
                     ▲
                     │

+----------------------------------+
|     MCP Server & AI Agents       |
+----------------------------------+
```

---

# 🔄 Data Flow

1. Security telemetry is generated or ingested into Splunk.
2. Background daemon continuously polls Splunk.
3. Events are analyzed by anomaly detection engines.
4. Detected anomalies are classified.
5. Threat intelligence is correlated.
6. MITRE ATT&CK techniques are mapped.
7. CTI reports are generated automatically.
8. Intelligence is stored in Supabase.
9. AI agents query data through MCP tools.
10. Analysts interact through the Streamlit dashboard.

---

# ✨ Core Features

## 📡 Autonomous Splunk Monitoring

* 24/7 telemetry ingestion
* Continuous SPL query execution
* Independent background daemon
* Near real-time event processing

---

## 🤖 Multi-Layer Anomaly Detection

### Statistical Detector

* Rolling baseline analysis
* Dynamic Z-score calculations
* Outlier identification

### Machine Learning Detector

* Isolation Forest model
* Unsupervised anomaly detection
* Historical-only training
* Data leakage prevention

---

## 🧠 Agentic Threat Hunting

SentinelAI implements an MCP (Model Context Protocol) server that enables AI agents to:

* Query Splunk securely
* Execute SPL searches
* Investigate incidents autonomously
* Gather contextual intelligence
* Generate analyst-ready findings

---

## 🎯 MITRE ATT&CK Mapping

Automatically maps detected activities to:

* Tactics
* Techniques
* Threat behaviors
* Investigation recommendations

---

## 📖 Cyber Threat Intelligence Engine

Generates structured CTI reports including:

* Incident summary
* Threat classification
* Timeline reconstruction
* MITRE mapping
* Risk assessment
* Recommended playbooks

---

## 🗄️ Intelligence Persistence

Supabase stores:

* Security anomalies
* Threat intelligence
* CTI reports
* Investigation history
* MITRE mappings

---

## 🎭 Attack Simulation Framework

Built-in simulation modules:

* Brute Force Attacks
* Port Scanning
* Reconnaissance Activity
* Denial of Service Events

Used for testing and demonstrating platform capabilities.

---

# 🛠️ Technology Stack

| Layer           | Technology           |
| --------------- | -------------------- |
| SIEM            | Splunk Enterprise    |
| Dashboard       | Streamlit            |
| Backend         | Python               |
| ML              | Scikit-Learn         |
| Statistics      | NumPy, SciPy, Pandas |
| Database        | Supabase PostgreSQL  |
| Agent Framework | MCP                  |
| Threat Mapping  | MITRE ATT&CK         |
| API Layer       | JSON-RPC             |

---

# 📂 Project Structure

```text
sentinelai/
│
├── app.py
├── main.py
├── config/
│
├── daemon/
│   └── splunk_daemon.py
│
├── detectors/
│   ├── statistical_detector.py
│   └── ml_detector.py
│
├── intelligence/
│   ├── attack_classifier.py
│   ├── timeline_builder.py
│   └── cti_generator.py
│
├── mcp_server/
│   ├── server.py
│   └── tools.py
│
├── simulator/
│   ├── brute_force.py
│   ├── dos.py
│   └── scanner.py
│
├── storage/
│   └── supabase_client.py
│
├── dashboard/
│
├── requirements.txt
├── .env.example
└── README.md
```

---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone https://github.com/your-username/sentinelai.git

cd sentinelai
```

## 2. Create Virtual Environment

```bash
python -m venv venv

source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment

Create a `.env` file:

```env
SPLUNK_HOST=localhost
SPLUNK_PORT=8089
SPLUNK_USERNAME=admin
SPLUNK_PASSWORD=your_password

SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_key

OPENAI_API_KEY=your_api_key
```

---

# ▶️ Running SentinelAI

Start the platform:

```bash
export PYTHONPATH=.

streamlit run app.py
```

Or:

```bash
python main.py
```

---

# 📊 Example Workflow

1. Simulate a brute-force attack.
2. Attack logs appear in Splunk.
3. Daemon ingests telemetry.
4. ML engine detects anomaly.
5. Intelligence engine classifies attack.
6. MITRE ATT&CK techniques are mapped.
7. CTI report is generated.
8. Report is stored in Supabase.
9. Analyst reviews findings from dashboard.

---

# 🔮 Future Enhancements

* Multi-SIEM Support
* Sigma Rule Conversion
* SOAR Integrations
* Threat Feed Enrichment
* Multi-Agent Collaboration
* LLM Fine-Tuned Security Models
* Automated Incident Response

---

# 🏆 Splunk Agentic Ops Hackathon

SentinelAI demonstrates how agentic AI systems can transform Security Operations by:

* Reducing analyst workload
* Accelerating investigations
* Automating CTI generation
* Improving threat visibility
* Enabling autonomous threat hunting

---

# 👨‍💻 Authors

Built for the Splunk Agentic Ops Hackathon.

Contributors are welcome.

---

# 📜 License

This project is licensed under the MIT License.

See the LICENSE file for details.
