# 🛡️ SentinelAI: Autonomous Agentic Security Operations & Cyber Threat Intelligence Engine

> **Splunk Agentic Ops Hackathon Submission**
>
> Track: **Security**

---

# 📌 Problem Statement

Security Operations Centers (SOCs) generate massive volumes of alerts and telemetry every day. Analysts often spend significant time manually reviewing logs, correlating events, identifying attack patterns, and preparing incident reports.

This creates several challenges:

* Alert fatigue
* Slow incident investigations
* Limited contextual threat intelligence
* Manual threat correlation workflows
* Delayed response times

SentinelAI addresses these challenges by combining Splunk telemetry, machine learning, and agentic AI workflows to automatically detect, classify, investigate, and explain security incidents.

---

# 🚀 Solution Overview

SentinelAI is an autonomous Security Operations and Cyber Threat Intelligence (CTI) platform that transforms raw security telemetry into actionable intelligence.

The platform continuously:

1. Ingests security telemetry
2. Detects anomalies
3. Classifies attack patterns
4. Maps threats to MITRE ATT&CK
5. Generates CTI reports
6. Assists investigations through AI-powered agents

Rather than producing more alerts, SentinelAI helps analysts understand the story behind an incident.

---

# 🤖 How AI Is Used

SentinelAI leverages AI across multiple stages of the security workflow.

### Machine Learning Anomaly Detection

* Isolation Forest identifies unusual activity patterns
* Statistical Z-Score analysis validates anomalies
* Multi-layer detection reduces false positives

### Agentic Security Investigation

Using MCP-enabled tools, AI agents can:

* Query operational security data
* Investigate suspicious activity
* Correlate events
* Assist threat hunting workflows

### Cyber Threat Intelligence Generation

The Intelligence Engine automatically:

* Builds attack timelines
* Generates incident summaries
* Maps activity to MITRE ATT&CK
* Produces analyst-ready CTI reports

---

# 🔍 Splunk Integration

SentinelAI uses Splunk as its primary telemetry and security data source.

### Splunk Components

* Splunk Enterprise
* SPL Queries
* Splunk Telemetry Pipelines
* Security Event Monitoring

### Data Flow

1. Security events are generated or ingested.
2. Splunk stores and indexes telemetry.
3. SentinelAI continuously polls Splunk data.
4. Anomaly engines evaluate incoming activity.
5. Intelligence is generated from detected threats.
6. Results are presented through the dashboard and AI agents.

---

# 🏗️ Architecture Diagram

> Include an image named:

```text
docs/architecture.png
```

The architecture diagram should illustrate:

* Splunk Enterprise
* Splunk MCP Server
* SentinelAI Intelligence Engine
* Anomaly Detection Layer
* Supabase Database
* Streamlit Dashboard
* AI Agents
* Data Flow Between Components

---

# ⚙️ Key Features

## 📡 Continuous Telemetry Monitoring

* Real-time event processing
* Background daemon architecture
* Automated ingestion workflows

## 🤖 Hybrid Anomaly Detection

* Z-Score statistical detection
* Isolation Forest machine learning
* Dynamic risk scoring

## 🎯 Threat Classification

Detects and classifies:

* Brute Force Attacks
* Port Scans
* Denial of Service Events
* Error Storms
* Authentication Anomalies

## 🧠 Agentic Threat Hunting

* MCP-powered investigation tools
* AI-assisted incident analysis
* Autonomous security workflows

## 📊 Cyber Threat Intelligence

* MITRE ATT&CK mapping
* Timeline reconstruction
* Incident scoring
* CTI report generation

## 🗄️ Persistent Intelligence Storage

* Historical investigations
* Threat records
* Intelligence reports
* Security analytics

---

# 🛠️ Technology Stack

| Component        | Technology           |
| ---------------- | -------------------- |
| SIEM             | Splunk Enterprise    |
| AI Agents        | MCP Framework        |
| Machine Learning | Scikit-Learn         |
| Statistics       | NumPy, Pandas, SciPy |
| Dashboard        | Streamlit            |
| Database         | Supabase PostgreSQL  |
| Language         | Python               |
| Logging          | Loguru               |

---

# 📂 Repository Structure

```text
sentinelai/
│
├── main.py
├── app.py
├── splunk_daemon.py
├── requirements.txt
├── README.md
├── LICENSE
│
├── docs/
│   └── architecture.png
│
├── src/
│   ├── anomaly/
│   ├── intelligence/
│   ├── simulator/
│   ├── storage/
│   ├── mcp_tools/
│
└── assets/
    ├── screenshots/
    └── demo/
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/your-username/sentinelai.git

cd sentinelai
```

## Create Virtual Environment

```bash
python -m venv venv

source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Configuration

Create a `.env` file:

```env
SPLUNK_HOST=localhost
SPLUNK_PORT=8089
SPLUNK_USERNAME=admin
SPLUNK_PASSWORD=password

SUPABASE_URL=your_url
SUPABASE_KEY=your_key

GEMINI_API_KEY=your_api_key
```

---

# ▶️ Running the Project

### Start Background Processing

```bash
python -m src.daemon.splunk_daemon
```

### Launch Dashboard

```bash
streamlit run app.py
```

---

# 🧪 Demo Workflow

1. Launch SentinelAI.
2. Generate simulated attack activity.
3. Observe telemetry ingestion.
4. Watch anomaly detection trigger.
5. Review generated threat intelligence.
6. Investigate findings through the dashboard.
7. Access AI-assisted threat analysis.

---

# 🎥 Demo Video

Demo Video:

```text
https://youtube.com/your-demo-link
```

---

# 🏆 Hackathon Alignment

SentinelAI aligns with the **Security Track** by:

* Accelerating threat detection
* Automating investigation workflows
* Improving incident response efficiency
* Leveraging Splunk telemetry
* Integrating AI agents through MCP
* Generating actionable cyber threat intelligence

---

# 🔮 Future Roadmap

* Multi-agent investigations
* SOAR integrations
* Threat feed enrichment
* Sigma rule generation
* Natural language threat hunting
* Automated incident response actions
* Multi-SIEM support

---

# 📜 License

Licensed under the MIT License.

See the LICENSE file for details.
