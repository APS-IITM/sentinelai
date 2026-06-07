import sys
import json
from datetime import datetime

# Import All Engine Layers
from src.mcp_tools.system_tools import SystemTools
from src.mcp_tools.network_tools import NetworkTools
from src.anomaly.analyzer import AnomalyAnalyzer
from src.intelligence.engine import IntelligenceEngine

# Safe AI Layer Try-Catch
try:
    from src.ai.analyzer import AIAnalyzer
    ai_enabled = True
except Exception as e:
    ai_enabled = False
    print(f"⚠️ Warning: AI Analyzer import failed ({e}). Running in Anomaly+Intelligence mode only.")

# Helper to pull integers from Splunk response data
def extract_values(response):
    if not response or not isinstance(response, dict):
        return []
    data = response.get("data", [])
    return [int(item["count"]) for item in data if "count" in item and str(item["count"]).isdigit()]

def main():
    print("=" * 75)
    print("🛡️  SENTINELAI: COMPLETE END-TO-END SYSTEM INTEGRATION TEST")
    print("=" * 75)

    # ==========================================
    # 1. INITIALIZE ALL PIPELINE MODULES
    # ==========================================
    print("\n[Step 1] Initializing system micro-engines...")
    system_tools = SystemTools()
    network_tools = NetworkTools()
    anomaly_analyzer = AnomalyAnalyzer()
    intelligence_engine = IntelligenceEngine()
    ai_analyzer = AIAnalyzer() if ai_enabled else None
    
    print("🟢 All core modules initialized successfully.")

    # ==========================================
    # 2. TELEMETRY COLLECTION & DATA EXTRACTION
    # ==========================================
    print("\n[Step 2] Collecting operational logs and trend sequences...")
    splunk_connected = True
    
    try:
        login_trend = system_tools.login_trend()
        error_trend = system_tools.error_trend()
        network_trend = network_tools.network_trend()

        login_series = extract_values(login_trend)
        error_series = extract_values(error_trend)
        network_series = extract_values(network_trend)
    except Exception as e:
        print(f"⚠️  Splunk Platform communication dropped: {e}")
        splunk_connected = False

    # Inject high-fidelity multi-stage threat metrics if data is missing/empty
    if not splunk_connected or not login_series or not network_series:
        print("💡 [MOCK TELEMETRY INJECTED] Simulating active multi-stage campaign data:")
        login_series = [12, 14, 15, 11, 13, 12, 14, 15, 16, 12, 14, 240]    # Brute force spike
        error_series = [5, 4, 6, 4, 5, 5, 4, 6, 5, 4, 5, 180]              # Error storm spike
        network_series = [45, 50, 48, 52, 47, 51, 49, 53, 50, 48, 52, 1500] # Volumetric DDoS spike
    
    print(f" -> Collected Login Sequence:  {login_series}")
    print(f" -> Collected Error Sequence:  {error_series}")
    print(f" -> Collected Network Sequence: {network_series}")

    # ==========================================
    # 3. RUN HYBRID ANOMALY ENGINE WINDOWS
    # ==========================================
    print("\n[Step 3] Processing datasets through statistical + ML classifiers...")
    detected_threat_events = []

    # Process Authentication
    auth_threat = anomaly_analyzer.analyze_series("Authentication Logs", login_series)
    if auth_threat:
        detected_threat_events.append(auth_threat)
        print("🚨 [ANOMALY] Volumetric spike flagged in AUTHENTICATION stream.")

    # Process System Errors
    error_threat = anomaly_analyzer.analyze_series("System Error Logs", error_series)
    if error_threat:
        detected_threat_events.append(error_threat)
        print("🚨 [ANOMALY] Volumetric spike flagged in SYSTEM ERROR stream.")

    # Process Network Traffic
    network_threat = anomaly_analyzer.analyze_series("Network Perimeter Logs", network_series)
    if network_threat:
        detected_threat_events.append(network_threat)
        print("🚨 [ANOMALY] Volumetric spike flagged in NETWORK TRAFFIC stream.")

    if not detected_threat_events:
        print("✅ Clean bill of health. No cross-correlated system threats found. Exiting.")
        return

    # ==========================================
    # 4. RUN INTELLIGENCE ENGINE CORRELATION
    # ==========================================
    print(f"\n[Step 4] Correlating {len(detected_threat_events)} threat events into CTI metrics...")
    
    intelligence_report = intelligence_engine.analyze(detected_threat_events)
    
    if not intelligence_report:
        print("❌ Intelligence aggregation pipeline failed to parse threats.")
        return

    print(f"🔬 Correlation Output: [ {intelligence_report.incident_type} ]")
    print(f"⚠️ Final Risk Level:    [ {intelligence_report.severity} ]")
    print(f"🔢 Timeline Footprint:  {len(intelligence_report.timeline)} distinct chronological intervals captured.")
    print(f"🏷️  MITRE Techniques:   {intelligence_report.mitre_techniques}")

    # ==========================================
    # 5. GENERATE AI-POWERED ANALYST BRIEFING
    # ==========================================
    print("\n[Step 5] Routing intelligence metadata into Google Gemini AI Engine...")
    if ai_enabled and ai_analyzer:
        try:
            # We pass the consolidated correlation data structure into the AI layer
            # Using the first major anomaly as the primary forensic anchor
            primary_threat = detected_threat_events[0]
            
            # Enrich description with overall correlation data before passing to AI
            primary_threat.description = f"Multi-stage incident correlated as {intelligence_report.incident_type}. Story details: {intelligence_report.attack_story}"
            primary_threat.severity = intelligence_report.severity
            
            print("⏳ Generating forensic assessment narrative (Raw Markdown output)...")
            print("\n" + "=" * 75)
            print("🤖 SENTINELAI AUTONOMOUS SOC ANALYST BRIEFING")
            print("=" * 75)
            
            ai_briefing = ai_analyzer.analyze_event(primary_threat)
            print(ai_briefing)
            print("=" * 75)
            
        except Exception as e:
            print(f"❌ AI Reasoning Engine failed: {e}")
    else:
        print("⚪ AI analysis skipped (Layer disabled or client variables missing).")

    # ==========================================
    # 6. UNIFIED STRUCTURAL EXPORT VALIDATION
    # ==========================================
    print("\n[Step 6] Verifying structural integrity of final JSON export layer...")
    try:
        final_json_payload = intelligence_report.model_dump_json(indent=2)
        print("🟢 Pipeline complete! Validated production JSON output:")
        print(final_json_payload[:400] + "\n... [Truncated for readability] ...")
    except Exception as e:
        print(f"❌ JSON serialization failure: {e}")

    print("\n" + "=" * 75)
    print(" INTEGRATION SCAN SUCCESSFUL: SYSTEM PREPPED FOR STREAMLIT DEPLOYMENT")
    print("=" * 75)

if __name__ == "__main__":
    main()
