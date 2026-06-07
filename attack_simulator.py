"""
SentinelAI: High-Performance Universal Cyber Attack Simulation System
Supports flexible execution modes (single, multiple, or all scenarios) and
triggers exactly ONE consolidated AI analysis report at the end of the runtime loop.
"""

import sys
import time
import json
from datetime import datetime
from rich.console import Console
from rich.markdown import Markdown

# ==========================================
# 📊 ARCHITECTURAL BACKBONE: ENGINE IMPORTS
# ==========================================
from src.anomaly.analyzer import AnomalyAnalyzer
from src.intelligence.engine import IntelligenceEngine

# Safe AI Layer Import Wrapper
try:
    from src.ai.analyzer import AIAnalyzer
    ai_enabled = True
except Exception as e:
    ai_enabled = False
    print(f"⚠️ AI Layer Warning: {e}")
    AIAnalyzer = None

# Global styling console
console = Console()

# ==========================================
# 🛑 SECURITY SCENARIO MATRIX GENERATOR
# ==========================================
class AdvancedAttackMatrix:
    """Generates complex multi-vector security footprints for evaluation."""
    
    @classmethod
    def generate_all(cls) -> dict:
        # Static baseline operational noise profiles
        base_auth = [12, 14, 15, 11, 13, 16, 12, 14, 15, 11, 13, 16, 14, 15, 12]
        base_err  = [2, 4, 3, 1, 2, 5, 2, 4, 3, 1, 2, 5, 3, 2, 4]
        base_net  = [45, 52, 48, 50, 47, 55, 45, 52, 48, 50, 47, 55, 51, 49, 53]

        # Scenario 1: Aggressive credential brute-force attack footprint
        scen_brute = list(base_auth)
        scen_brute[-1] = 680  

        # Scenario 2: Stealthy infrastructure reconnaissance port scan footprint
        scen_recon = [45, 52, 48, 50, 47, 55, 60, 72, 85, 110, 140, 195, 260, 340, 420]

        # Scenario 3: Application layer web software crash cascade footprint
        scen_errors = list(base_err)
        scen_errors[-4:] = [45, 120, 480, 1500]

        # Scenario 4: The Enterprise Killchain (Recon -> Brute Force -> DDoS Collapse)
        kill_auth = list(base_auth)
        kill_err  = list(base_err)
        kill_net  = list(base_net)
        kill_net[-6:]  = [120, 250, 480, 900, 1800, 4500] 
        kill_auth[-3:] = [85, 290, 750]                  
        kill_err[-1]   = 1500                            

        return {
            "1": {
                "title": "Distributed Credential Stuffing Campaign",
                "desc": "Targeting external active directory authentication interfaces.",
                "auth": scen_brute, "error": base_err, "network": base_net
            },
            "2": {
                "title": "Slow Horizontal Infrastructure Reconnaissance Scan",
                "desc": "Anomalous multi-port network map behavior hitting non-standard entry nodes.",
                "auth": base_auth, "error": base_err, "network": scen_recon
            },
            "3": {
                "title": "Post-Exploitation Application Subcomponent Failure",
                "desc": "Web middleware experiencing unhandled exceptions following atypical parameter injection.",
                "auth": base_auth, "error": scen_errors, "network": base_net
            },
            "4": {
                "title": "Advanced Multi-Stage Enterprise Killchain (GRAND PRIZE DEMO)",
                "desc": "Synchronized infrastructure subversion campaign tracking complete threat lifecycle.",
                "auth": kill_auth, "error": kill_err, "network": kill_net
            }
        }

# ==========================================
# 🚀 CORE SIMULATION RUNNER PIPELINE
# ==========================================
def run_anomaly_detection(scenario_id: str, data: dict, anomaly_engine) -> list:
    """
    Evaluates raw dataset streams mathematically.
    Returns a list of any discovered ThreatEvent anomalies.
    """
    print("\n" + "─" * 80)
    print(f" 🔍 RUNNING SCENARIO {scenario_id}: {data['title'].upper()} ".center(80, "─"))
    print("─" * 80)
    print(f" ▸ Context Focus: {data['desc']}")
    
    scenario_threats = []
    
    auth_res = anomaly_engine.analyze_series(f"Auth_Stream_Scen_{scenario_id}", data['auth'])
    if auth_res: 
        scenario_threats.append(auth_res)
        print("   ⚠️  [ANOMALY FIRED] Volumetric surge flagged in Authentication logs.")
        
    error_res = anomaly_engine.analyze_series(f"System_Errors_Scen_{scenario_id}", data['error'])
    if error_res: 
        scenario_threats.append(error_res)
        print("   ⚠️  [ANOMALY FIRED] Volumetric surge flagged in System Exception logs.")
        
    net_res = anomaly_engine.analyze_series(f"Network_Ingress_Scen_{scenario_id}", data['network'])
    if net_res: 
        scenario_threats.append(net_res)
        print("   ⚠️  [ANOMALY FIRED] Volumetric surge flagged in Network Perimeter logs.")

    if not scenario_threats:
        print("   ✅ Subsystem status clear. Telemetry fluctuations fall within normal noise levels.")
        
    return scenario_threats


def trigger_unified_intelligence_briefing(aggregated_threats: list, selected_scenarios: dict, intel_engine, ai_engine):
    """
    Compiles all global threat payloads gathered during the run, 
    executes CTI correlation mapping, and calls the Google Gemini API exactly ONCE 
    with context for all completed scenarios.
    """
    print("\n" + "═" * 80)
    print(" 🛠️  SENTINELAI GLOBAL INTELLIGENCE CORRELATION CORE ".center(80, "═"))
    print("═" * 80)
    
    print(f"⚙️ Ingesting batch pipeline dataset. Total Threat Objects collected: {len(aggregated_threats)}")
    
    # 1. Run Core Strategic CTI Correlation
    start_time = time.time()
    cti_report = intel_engine.analyze(aggregated_threats)
    latency = (time.time() - start_time) * 1000

    print(f" 🔹 Consolidated Signature ID : [ {cti_report.incident_type} ]")
    print(f" 🔹 Maximum System Risk State  : [ {cti_report.severity} ]")
    print(f" 🔹 Analytics Processing Speed : {latency:.2f} ms")
    
    print("\n🎯 Correlated MITRE ATT&CK Mapping matrix:")
    for code in cti_report.mitre_techniques:
        print(f"   [+] Technique: {code}")

    print("\n⏱️  Unified Incident Lifecycle Audit Timeline (All Chosen Scenarios Combined):")
    for i, event in enumerate(cti_report.timeline, 1):
        print(f"   {i} | Time: {event.get('time')} | Node Source: {event.get('source')} | Vector Code: {event.get('attack')} ({event.get('severity')})")

    # 2. Trigger Unified Autonomous Generative AI Assessment (Single Call Execution)
    if ai_enabled and ai_engine:
        print("\n" + "═" * 80)
        print(" 🤖 SINGLE-CALL AI SOC ANALYST UNIFIED FORENSIC ASSIGNMENT ".center(80, "═"))
        print("═" * 80)
        print("⏳ Constructing consolidated multi-vector prompt parameters...")
        print("🚀 Dispatching structural telemetry context model payload to Google Gemini API...")
        
        # Package macro-metadata from ALL executed scenarios into an explicit manifest
        orchestration_manifest = {
            "evaluation_timestamp": datetime.utcnow().isoformat() + "Z",
            "simulated_scenarios_executed": [
                {"id": s_id, "title": s_info["title"], "scope": s_info["desc"]} 
                for s_id, s_info in selected_scenarios.items()
            ],
            "correlation_engine_summary": {
                "signature_match": cti_report.incident_type,
                "global_severity_state": cti_report.severity,
                "mitre_attack_techniques": cti_report.mitre_techniques,
                "automated_narrative_track": cti_report.attack_story
            },
            "raw_incident_timeline": cti_report.timeline,
            "total_extracted_telemetry_anomalies": len(aggregated_threats)
        }

        # Safe injection wrapper into a single carrier threat object properties
        primary_threat = aggregated_threats[0]
        primary_threat.description = json.dumps(orchestration_manifest, indent=2)
        primary_threat.severity = cti_report.severity

        # Request raw string from the updated backend API
        raw_markdown = ai_engine.analyze_event(primary_threat)

        # -------------------------------------------------------------
        # 💎 SINGLE UNIFIED TERMINAL RENDERING LAYER
        # -------------------------------------------------------------
        console.print("\n")
        console.print("[bold cyan]🤖 AI SOC ANALYST BRIEFING[/bold cyan]", justify="center")
        console.print("[dim]─" * console.width + "[/dim]")
        
        # Parse output markup content exactly once
        console.print(Markdown(raw_markdown))
        
        console.print("[dim]─" * console.width + "[/dim]\n")
        # -------------------------------------------------------------
    else:
        print("\n⚪ AI Analysis skipped (Layer disabled or model credentials missing).")
        
    print("\n" + "═" * 80)
    print(" UNIFIED FORENSIC ANALYSIS PIPELINE RUN COMPLETE ".center(80, "═"))
    print("═" * 80)


# ==========================================
# 🏁 MAIN ENTRY CONTROL RUNNER
# ==========================================
def main():
    print("=" * 80)
    print(" 🛡️  SENTINELAI: BATCH CYBER SECURITY SIMULATION SYSTEM ".center(80, " "))
    print("=" * 80)

    # Instantiate Engines
    anomaly_engine = AnomalyAnalyzer()
    intel_engine = IntelligenceEngine()
    ai_engine = AIAnalyzer() if ai_enabled else None

    # Load All Scenario Profiles
    scenarios = AdvancedAttackMatrix.generate_all()

    print("\n💡 Pre-Staged Simulation Incident Selection Options:")
    for num, sc in scenarios.items():
        print(f"  [{num}] {sc['title']}")
        
    print("\n📝 FLEXIBLE INPUT MODES AVAILABLE:")
    print("   ▸ [ONLY ONE]  Type a single number (e.g., '4')")
    print("   ▸ [ALL]       Type the keyword 'all'")
    print("   ▸ [MULTIPLE]  Type numbers separated by commas (e.g., '1,3' or '1,2,4')")
    
    try:
        choice = input("\nEnter your simulation choice: ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting simulator platform.")
        sys.exit(0)

    # Containers for global correlation accumulation
    global_threat_pool = []
    executed_scenarios_tracker = {}

    # Parse inputs adaptively
    if choice.lower() == "all":
        target_ids = list(scenarios.keys())
    else:
        target_ids = [c.strip() for c in choice.split(",") if c.strip() in scenarios]

    if not target_ids:
        print("❌ Invalid entry or no valid scenario numbers found. Aborting test workflow.")
        return

    # Sequentially execute mathematical anomaly evaluations
    for num in target_ids:
        scenario_anomalies = run_anomaly_detection(num, scenarios[num], anomaly_engine)
        global_threat_pool.extend(scenario_anomalies)
        # Dynamic tracking registration
        executed_scenarios_tracker[num] = scenarios[num]
        time.sleep(0.1)

    # Trigger correlation engine and AI exactly ONCE after all calculations conclude
    if global_threat_pool:
        trigger_unified_intelligence_briefing(
            aggregated_threats=global_threat_pool, 
            selected_scenarios=executed_scenarios_tracker, 
            intel_engine=intel_engine, 
            ai_engine=ai_engine
        )
    else:
        print("\n✅ Simulation Scan Finished: No anomalies detected. AI invocation skipped.")


if __name__ == "__main__":
    main()