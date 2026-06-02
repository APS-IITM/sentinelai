# 🛡️ SentinelAI

### AI-Powered Incident Intelligence for Splunk Security Operations

SentinelAI is an AI-driven incident investigation platform that helps security teams detect, analyze, and understand security incidents faster using Splunk telemetry, anomaly detection, MCP-powered investigation tools, and AI reasoning.

Instead of manually searching through thousands of log events, analysts receive AI-generated incident intelligence reports containing severity assessments, root-cause analysis, supporting evidence, remediation recommendations, and suggested SPL queries.

---

## 🚀 Features

### 🔍 Splunk Integration

* Connects to Splunk Enterprise or Splunk Cloud
* Executes SPL queries through Python
* Retrieves and processes security telemetry

### 🧰 MCP Investigation Tools

* Log retrieval tools
* Incident window analysis
* Custom SPL query execution
* Evidence collection

### 🚨 Anomaly Detection

* Failed-login spike detection
* Error-rate anomaly detection
* Suspicious activity identification
* Incident severity scoring

### 🤖 AI-Powered Incident Intelligence

* Automated incident summaries
* Root-cause analysis
* Security recommendations
* Suggested SPL investigations

### 📊 Interactive Dashboard

* Streamlit-based SOC dashboard
* Incident feed
* Investigation workspace
* Evidence visualization

### 🎯 Attack Simulation

* Brute-force attack simulator
* Synthetic security event generation
* Automated detection testing

---

## 🏗️ Architecture

```text
User
 │
 ▼
Streamlit Dashboard
 │
 ▼
Incident Intelligence Engine
 │
 ├── MCP Investigation Tools
 ├── Anomaly Detection Engine
 └── AI Reasoning Engine
 │
 ▼
Splunk Platform
 │
 ▼
Security Telemetry & Logs
```

---

## 📂 Project Structure

```text
sentinelai/
│
├── app/
├── src/
│   ├── splunk/
│   ├── mcp_tools/
│   ├── anomaly/
│   ├── ai/
│   ├── intelligence/
│   └── simulator/
│
├── tests/
├── docs/
├── requirements.txt
├── README.md
└── .env
```

---

## 🛠️ Technology Stack

* Python
* Splunk Enterprise / Splunk Cloud
* Splunk SDK
* Streamlit
* Pandas
* Requests
* Python Dotenv
* MCP Tool Architecture
* AI Hosted Models

---

## 🎯 Project Goal

SentinelAI aims to reduce security investigation time by automatically:

1. Detecting suspicious activity
2. Collecting relevant evidence
3. Investigating incidents
4. Generating AI-powered intelligence reports
5. Recommending remediation actions

---

## 📅 Development Timeline

| Day | Milestone                 |
| --- | ------------------------- |
| 1   | Splunk Environment Setup  |
| 2   | Query Layer               |
| 3   | MCP Tools                 |
| 4   | Anomaly Detection         |
| 5   | AI Integration            |
| 6   | Intelligence Engine       |
| 7   | Streamlit Dashboard       |
| 8   | Interactive Investigation |
| 9   | Attack Simulation         |
| 10  | Final Submission          |

---

## 📜 License

This project is licensed under the MIT License.
