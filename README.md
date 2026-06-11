# 🛡️ SentinelAI: Autonomous Agentic Security Operations & Cyber Threat Intelligence Engine

> **Built for the Splunk Agentic Ops Hackathon**
>
> Transforming raw security telemetry into actionable intelligence through autonomous agents, machine learning, and real-time threat correlation.

---

## 🚀 Overview

Modern Security Operations Centers (SOCs) face an overwhelming volume of alerts, logs, and security events every day. Analysts often spend more time investigating data than responding to threats.

**SentinelAI** is an autonomous Security Operations and Cyber Threat Intelligence (CTI) platform designed to bridge that gap. By combining continuous telemetry ingestion, machine learning–based anomaly detection, threat classification, and agentic reasoning through the Model Context Protocol (MCP), SentinelAI transforms raw security events into meaningful intelligence.

Rather than generating another dashboard full of alerts, SentinelAI focuses on answering critical questions:

* What happened?
* Why did it happen?
* How severe is the threat?
* Which MITRE ATT&CK techniques are involved?
* What actions should be taken next?

---

# 🎯 Key Capabilities

### 📡 Continuous Security Telemetry Processing

A dedicated background worker continuously ingests and processes security events, ensuring analysis remains active regardless of dashboard state.

### 🤖 Hybrid Anomaly Detection

Combines statistical analysis and machine learning to identify suspicious behavior:

* Rolling Z-Score anomaly detection
* Isolation Forest outlier detection
* Dynamic risk scoring
* False-positive reduction through multi-layer validation

### 🧠 Context-Aware Threat Classification

Detected anomalies are enriched with contextual intelligence and automatically classified into attack categories such as:

* Brute Force Attacks
* Port Scanning
* Denial-of-Service Activity
* Error Storms
* Suspicious Authentication Patterns

### 🔍 Agentic Threat Investigation

Through MCP-powered tools, AI agents can securely interact with operational security data, perform investigations, and assist analysts with contextual threat hunting.

### 📊 Cyber Threat Intelligence Generation

SentinelAI converts isolated anomalies into structured intelligence by:

* Correlating related events
* Building attack timelines
* Mapping behaviors to MITRE ATT&CK
* Generating analyst-ready CTI reports

### 🗄️ Persistent Intelligence Storage

All intelligence artifacts are stored in Supabase for future investigation, reporting, and historical analysis.

---

# 🏗️ Architecture

```text
                   ┌─────────────────────────┐
                   │    Security Analyst     │
                   └────────────┬────────────┘
                                │
                                ▼
                   ┌─────────────────────────┐
                   │   Streamlit Dashboard   │
                   └────────────┬────────────┘
                                │
                                ▼
                   ┌─────────────────────────┐
                   │   Threat Simulator UI   │
                   └────────────┬────────────┘
                                │
                                ▼
                   ┌─────────────────────────┐
                   │     Supabase Queue      │
                   └────────────┬────────────┘
                                │
                                ▼
                   ┌─────────────────────────┐
                   │     Splunk Daemon       │
                   │  Continuous Processing  │
                   └────────────┬────────────┘
                                │
                ┌───────────────┴───────────────┐
                ▼                               ▼

      ┌───────────────────┐         ┌───────────────────┐
      │ Statistical Layer │         │ Machine Learning  │
      │    Z-Score        │         │ Isolation Forest  │
      └───────────────────┘         └───────────────────┘
                │                               │
                └───────────────┬───────────────┘
                                ▼
                   ┌─────────────────────────┐
                   │ Intelligence Engine     │
                   │ Classification + CTI    │
                   └────────────┬────────────┘
                                │
                                ▼
                   ┌─────────────────────────┐
                   │ MCP Server & AI Agents  │
                   └─────────────────────────┘
```

---

# 🔄 Processing Workflow

### 1. Event Generation

The Attack Simulation Engine generates realistic security events with varying severity levels ranging from **LOW** to **CRITICAL**.

### 2. Continuous Ingestion

The background daemon continuously polls incoming events and prepares them for analysis.

### 3. Anomaly Detection

Each event stream passes through multiple analytical layers:

* Statistical anomaly detection
* Machine learning anomaly detection
* Risk scoring
* Event correlation

### 4. Threat Classification

Suspicious events are categorized into attack patterns using metadata analysis and behavioral signatures.

### 5. Intelligence Generation

Verified threats are transformed into actionable intelligence through:

* Timeline construction
* Threat scoring
* MITRE ATT&CK mapping
* CTI report generation

### 6. Analyst Investigation

Security analysts and AI agents access intelligence through the Streamlit dashboard and MCP tools.

---

# ✨ Why SentinelAI?

Most security platforms stop at detection.

SentinelAI goes further by combining:

* Detection
* Classification
* Correlation
* Investigation
* Intelligence Generation

into a unified autonomous workflow.

The result is a system that helps analysts spend less time searching through logs and more time understanding threats.
