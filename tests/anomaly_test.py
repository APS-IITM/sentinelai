import sys
from datetime import datetime
from src.mcp_tools.system_tools import SystemTools
from src.anomaly.analyzer import AnomalyAnalyzer

# ==============================================================================
# 🧰 DATA EXTRACTION HELPER
# ==============================================================================
def extract_values(response):
    """
    Extracts raw integer event counts chronologically out of the Splunk response.
    """
    if not response or not isinstance(response, dict):
        return []
        
    data = response.get("data", [])
    values = []

    for item in data:
        if "count" in item:
            try:
                values.append(int(item["count"]))
            except (ValueError, TypeError):
                pass

    return values


# ==============================================================================
# 🎯 PIPELINE RUNNER WITH FALLBACK TELEMETRY GENERATION
# ==============================================================================
def execute_test_stage(engine, source_name, values):
    print("\n" + "─" * 60)
    print(f"🔍 ANALYZING SUBSYSTEM: {source_name}")
    print("─" * 60)
    print(f"Incoming Time Series Window counts: {values}")
    
    try:
        # Executes your Z-score + Isolation Forest calculation
        result = engine.analyze_series(source_name, values)

        if result:
            print(f"🟢 [ALERT FIRED] Anomaly found with severity: {result.severity}")
            print(result.model_dump_json(indent=4))
            return True
        else:
            print("⚪ [CLEAN) No volumetric anomalies identified in this window.")
            return False
            
    except TypeError as te:
        if "record_count" in str(te):
            print("❌ [FATAL FIELD MATCH ERROR] Your AnomalyAnalyzer passed 'record_count'")
            print("   but your ThreatEvent Pydantic model requires 'data_points'!")
            print("👉 FIX: Change 'record_count=values[-1]' to 'data_points=values[-1]' in src/anomaly/analyzer.py")
        else:
            print(f"❌ Execution Exception: {te}")
        return False
    except Exception as e:
        print(f"❌ Execution Exception: {e}")
        return False


# ==============================================================================
# 🚀 MAIN RUNNER
# ==============================================================================
def main():
    print("=" * 60)
    print("🛡️  SENTINELAI: HYBRID ANOMALY DETECTION ENGINE DIAGNOSTIC")
    print("=" * 60)

    # Instantiate core components
    tools = SystemTools()
    engine = AnomalyAnalyzer()

    # Step 1: Attempt to gather live trend data from Splunk via MCP tools
    print("\n[Stage 1] Querying Splunk endpoints via SystemTools...")
    splunk_online = True
    
    try:
        login_data = tools.login_trend()
        error_data = tools.error_trend()
        
        login_values = extract_values(login_data)
        error_values = extract_values(error_data)
    except Exception as e:
        print(f"⚠️  Splunk connection down or misconfigured: {e}")
        splunk_online = False

    # Step 2: Inject synthetic malicious telemetry if Splunk data is empty/offline
    if not splunk_online or not login_values or not error_values:
        print("💡 [MOCK ACTIVATED] Injecting pre-staged multi-stage attack metrics for testing:")
        
        # 12 normal periods followed by a massive brute-force/DDoS volume jump
        login_values = [12, 14, 11, 15, 10, 13, 11, 14, 12, 15, 13, 11, 450]
        
        # Consistent errors followed by an application crash error storm spike
        error_values = [2, 1, 3, 2, 4, 1, 2, 3, 2, 1, 2, 3, 185]
    else:
        print("🟢 Live connection verified. Running against real Splunk index trends.")

    # Step 3: Route extracted metrics into your analytical layer
    auth_alert = execute_test_stage(engine, "AUTHENTICATION", login_values)
    system_alert = execute_test_stage(engine, "ERROR_SYSTEM", error_values)

    print("\n" + "=" * 60)
    print(" Diagnostic Complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
