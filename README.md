🛡️ SentinelAI: Autonomous Agentic Security Operations & CTI EngineSentinelAI is an advanced, autonomous incident intelligence platform engineered for the Splunk Agentic Ops Hackathon. It shifts Security Operations Centers (SOCs) from manual log parsing to an AI-driven, agentic ecosystem. By combining always-on telemetry ingestion, multi-layered machine learning anomaly engines, and a custom Model Context Protocol (MCP) server, SentinelAI enables AI agents to query Splunk core data securely, correlate threats, and auto-generate comprehensive Cyber Threat Intelligence (CTI) reports.🏗️ System Architecture & Data Flow                   +----------------------------------+
                   |       Human SOC Analyst          |
                   +----------------------------------+
                                    │
                                    ▼
                   +----------------------------------+
                   |       Streamlit Dashboard        |
                   +----------------------------------+
                     │                              ▲
                     │ (Triggers Simulations)       │ (Reads Insights)
                     ▼                              │
+----------------------------------+      +----------------------------------+
|      Threat Actor Simulator      |      |    Cyber Threat Intelligence     |
|   (Brute Force, Scan, DoS)       |      |     Reports (Supabase Store)     |
+----------------------------------+      +----------------------------------+
                     │                                      ▲
                     ▼ (Appends Data)                       │ (Saves CTI Payload)
+----------------------------------+                        │
|          Splunk SIEM             |      +----------------------------------+
|    (Security Telemetry Logs)     |      |       Intelligence Engine        |
+----------------------------------+      |  (MITRE Mapping & Story Gen)     |
                     │                                      ▲
                     ▼ (Continuous Polling)                 │ (Fires Anomaly Dict)
+----------------------------------+                        │
|  Autonomous Splunk Data Daemon   |      +----------------------------------+
|      (splunk_daemon.py Loop)     |─────>|      Anomaly Detection Core      |
+----------------------------------+      | (Z-Score & Isolation Forest ML)  |
                     │                    +----------------------------------+
                     │ (Exposes JSON-RPC Schema)
                     ▼
+----------------------------------+
|    Model Context Protocol Server |
|      (MCP / BaseTool Logic)      |
+----------------------------------+
                     │
                     ▼ (Executes Autonomous SPL Queries)
+----------------------------------+
|     Agentic AI Reasoning Core     |
|     (Threat Hunting Assistant)    |
+----------------------------------+
🚀 Key Architectural FeaturesAutonomous $24/7$ Splunk Ingestion: Features a decoupled, always-on background polling daemon (splunk_daemon.py). It profiles SIEM telemetry via automated SPL tracking inquiries completely independent of frontend state layers.Overfitting-Resistant Anomaly Engine: Utilizes moving Z-Scores (StatisticalDetector) along with an asynchronous Isolation Forest ML model (MLDetector). By training strictly on historical windows (data[:-1]) and predicting on the active edge (data[-1:]), the system eliminates data leakage.Agentic Model Context Protocol (MCP): Connects Large Language Models safely to enterprise data pipelines. The AI agent executes custom, targeted SPL query loops directly against Splunk endpoints through standardized JSON-RPC schemas.Automated CTI Engine & Playbooks: Classifies attack signatures dynamically (AttackClassifier), correlates vectors over timelines (TimelineBuilder), updates MITRE ATT&CK Mapping Matrices, and links playbooks directly from its response matrices.🛠️ Technology Ecosystem StackSIEM Foundation: Splunk Enterprise (Core Administrative Port 8089)Framework Core: Streamlit (Analytical Viewport Interface)Mathematical Operations: NumPy, Pandas, SciPy (Z-Score Linear Formulations)Machine Learning Engine: Scikit-Learn (IsolationForest Ensemble Clustering)Agent Integration Standard: Model Context Protocol (MCP Protocol Spec)Storage Layer: Supabase Database (PostgreSQL Engine Core)⚙️ Installation & Running Locally1. Pre-requisites & Core Sandbox ProvisioningEnsure you have a valid Splunk Enterprise instance active with a Developer License applied, listening over local management ports (8089).2. System Dependency InstallationBashgit clone https://github.com/your-username-here/sentinelai.git
cd sentinelai
pip install -r requirements.txt
3. Key Mapping Configuration (.env)Generate a .env deployment file inside your project root following this syntax schema layout:Code snippetSPLUNK_HOST=localhost
SPLUNK_PORT=8089
SPLUNK_USERNAME=admin
SPLUNK_PASSWORD=your_secure_password_here

SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-secure-service-role-access-token

OPENAI_API_KEY=sk-proj-your-api-agent-token-here
4. Direct Terminal System ExecutionLaunch the unified core using your shell workspace. The system hooks an automated single-instance execution controller (@st.cache_resource) to launch your background daemon monitoring process cleanly alongside the dashboard:Bashexport PYTHONPATH=.
streamlit run app.py
⚖️ LicenseDistributed under the MIT Open Source License. See the LICENSE document file for absolute details.
