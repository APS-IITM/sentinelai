"""
SentinelAI: Granular Multi-Tier Attack Simulation System
Enables target log-stream segmentation and programmatic intensity injection matrix profiles.
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

try:
    from src.ai.analyzer import AIAnalyzer
    ai_enabled = True
except Exception as e:
    ai_enabled = False
    print(f"⚠️ AI Layer Warning: {e}")
    AIAnalyzer = None

global_console = Console()

# ==========================================
# 🛑 SECURITY SCENARIO MATRIX GENERATOR
# ==========================================
class DynamicAttackMatrix:
    """Generates user-targeted, variable-intensity operational security log anomalies."""
    
    # Clean, industry-standard baseline noise distribution profiles
    BASELINE_AUTH = [12, 14, 15, 11, 13, 16, 12, 14, 15, 11, 13, 16, 14, 15, 12]
    BASELINE_ERR  = [2, 4, 3, 1, 2, 5, 2, 4, 3, 1, 2, 5, 3, 2, 4]
    BASELINE_NET  = [45, 52, 48, 50, 47, 55, 45, 52, 48, 50, 47, 55, 51, 49, 53]

    # Target intensity multipliers determining volumetric spikes
    INTENSITY_MULTIPLIERS = {
        "LOW": 3.5,       # Barely breaks standard Z-Score limits
        "MEDIUM": 8.0,    # Clear visible mathematical outlier
        "HIGH": 25.0,     # Major engineering service degradation threshold
        "CRITICAL": 75.0  # Devastating infrastructural saturation spike
    }

    @classmethod
    def generate_custom_vector(cls, target_log: str, intensity: str) -> dict:
        """Constructs highly tailored spike vectors depending on selected parameters."""
        multiplier = cls.INTENSITY_MULTIPLIERS.get(intensity.upper(), 5.0)
        
        # Fresh baseline deep copy templates
        auth_stream = list(cls.BASELINE_AUTH)
        error_stream = list(cls.BASELINE_ERR)
        net_stream = list(cls.BASELINE_NET)

        title_suffix = f"[{intensity.upper()} INTENSITY PROFILE]"
        
        if target_log == "1":
            # Target Authentication Stream (e.g., Brute Force / Stuffing)
            auth_stream[-1] = int(auth_stream[-1] * multiplier)
            return {
                "title": f"Targeted Authentication Exploitation {title_suffix}",
                "desc": f"Volumetric attack footprint tracking authentication vectors scaled at {multiplier}x noise.",
                "auth": auth_stream, "error": error_stream, "network": net_stream
            }
            
        elif target_log == "2":
            # Target System Error Exceptions Stream
            error_stream[-1] = int(error_stream[-1] * multiplier * 2.5)
            return {
                "title": f"Triggered Infrastructure Exception Storm {title_suffix}",
                "desc": f"Unhandled web middleware crashes producing core telemetry drops scaled at {multiplier}x noise.",
                "auth": auth_stream, "error": error_stream, "network": net_stream
            }
            
        elif target_log == "3":
            # Target Network Ingress Footprints
            net_stream[-1] = int(net_stream[-1] * multiplier)
            return {
                "title": f"Volumetric Network Perimeter Exfiltration Scan {title_suffix}",
                "desc": f"Boundary firewall connection drops showcasing horizontal mapping patterns scaled at {multiplier}x noise.",
                "auth": auth_stream, "error": error_stream, "network": net_stream
            }
            
        elif target_log == "4":
            # The Full System Killchain (Affects ALL log sources simultaneously)
            auth_stream[-1] = int(auth_stream[-1] * multiplier * 0.8)
            error_stream[-1] = int(error_stream[-1] * multiplier * 1.5)
            net_stream[-1] = int(net_stream[-1] * multiplier * 1.2)
            return {
                "title": f"Advanced Synchronized Multi-Stage Killchain {title_suffix}",
                "desc": f"Coordinated infrastructure subversion tracking complete threat footprint across every log telemetry sink.",
                "auth": auth_stream, "error": error_stream, "network": net_stream
            }

# ==========================================
# 🚀 PIPELINE LIFECYCLE MANAGEMENT UTILITIES
# ==========================================
def run_anomaly_detection(data: dict, anomaly_engine) -> list:
    """Evaluates the custom-built data streams mathematically via your existing engines."""
    global_console.print(f"\n[bold gold1]─[/bold gold1]" * 60)
    global_console.print(f"📡 [bold white]EXECUTING VECTOR SIMULATION:[/bold white] {data['title']}")
    global_console.print(f"[dim]Description: {data['desc']}[/dim]")
    global_console.print(f"─" * 60)
    
    threat_profiles = []
    
    # Call your standard production analytical logic wrappers
    auth_res = anomaly_engine.analyze_series("Authentication Logs", data['auth'])
    if auth_res:
        threat_profiles.append(auth_res)
        print("  ⚠️  [ANOMALY FLAG] Volumetric anomaly isolated in Authentication logs.")
        
    error_res = anomaly_engine.analyze_series("System Error Logs", data['error'])
    if error_res:
        threat_profiles.append(error_res)
        print("  ⚠️  [ANOMALY FLAG] Volumetric anomaly isolated in System Error logs.")
        
    net_res = anomaly_engine.analyze_series("Network Perimeter Logs", data['network'])
    if net_res:
        threat_profiles.append(net_res)
        print("  ⚠️  [ANOMALY FLAG] Volumetric anomaly isolated in Network Ingress logs.")

    if not threat_profiles:
        global_console.print("  [bold green]✅ SYSTEM STABLE:[/bold green] Injected values failed to trigger detection engine thresholds.")
        
    return threat_profiles


def trigger_unified_intelligence_briefing(aggregated_threats: list, selected_meta: dict, intel_engine, ai_engine):
    """Compiles total active threats, maps MITRE indicators, and returns a single combined AI analysis brief."""
    global_console.print("\n" + "═" * 80)
    global_console.print(" 🛡️  SENTINELAI CORE CONSOLIDATED INCIDENT CORRELATION MATRIX ".center(80, "═"))
    global_console.print("═" * 80)
    
    # 1. Run Core Strategic CTI Correlation
    start_time = time.time()
    cti_report = intel_engine.analyze(aggregated_threats)
    latency = (time.time() - start_time) * 1000

    print(f" 🔹 Consolidated Signature ID : [ {cti_report.incident_type} ]")
    print(f" 🔹 Peak Integrated Severity    : [ {cti_report.severity} ]")
    print(f" 🔹 Engine Execution Latency    : {latency:.2f} ms")
    
    print("\n🎯 Correlated MITRE ATT&CK Mapping matrix:")
    for code in cti_report.mitre_techniques:
        print(f"   [+] Technique Tracker: {code}")

    print("\n⏱️  Unified Incident Lifecycle Audit Timeline:")
    for i, event in enumerate(cti_report.timeline, 1):
        print(f"   {i} | Node: {event.get('source')} | Attack Phase Profile: {event.get('attack')} ({event.get('severity')})")

    # 2. Trigger Unified Autonomous Generative AI Assessment (Single Call Execution)
    if ai_enabled and ai_engine:
        global_console.print("\n" + "═" * 80)
        global_console.print(" 🤖 AI SOC FORENSIC INTELLIGENCE TASK BRIEFING ".center(80, "═"))
        global_console.print("═" * 80)
        
        orchestration_manifest = {
            "evaluation_timestamp": datetime.utcnow().isoformat() + "Z",
            "injection_parameters": selected_meta,
            "correlation_engine_summary": {
                "signature_match": cti_report.incident_type,
                "global_severity_state": cti_report.severity,
                "mitre_attack_techniques": cti_report.mitre_techniques,
                "automated_narrative_track": cti_report.attack_story
            },
            "raw_incident_timeline": cti_report.timeline
        }

        # Safe injection wrapper into carrier object parameters
        primary_threat = aggregated_threats[0]
        primary_threat.description = json.dumps(orchestration_manifest, indent=2)
        primary_threat.severity = cti_report.severity

        with global_console.status("[bold white]Streaming scenario manifest parameters to Google Gemini Core...[/bold white]"):
            raw_markdown = ai_engine.analyze_event(primary_threat)

        global_console.print("\n")
        global_console.print("[bold cyan]🤖 AI SOC ANALYST CORRELATED REPORT[/bold cyan]", justify="center")
        global_console.print("[dim]─" * global_console.width + "[/dim]")
        global_console.print(Markdown(raw_markdown))
        global_console.print("[dim]─" * global_console.width + "[/dim]\n")
    else:
        print("\n⚪ Generative AI Analysis skipped (Layer disabled or endpoint credentials offline).")


# ==========================================
# 🏁 MAIN INTERACTIVE TERMINAL LOOP
# ==========================================
def main():
    global_console.print("[bold white]========================================================================[/bold white]")
    global_console.print(" 🛡️  SENTINELAI: TARGETED LOG EXTRACTION & ATTACK INTENSITY SIMULATOR ".center(80, " "))
    global_console.print("[bold white]========================================================================[/bold white]")

    # Instantiate Analytical Elements
    anomaly_engine = AnomalyAnalyzer()
    intel_engine = IntelligenceEngine()
    ai_engine = AIAnalyzer() if ai_enabled else None

    # Step 1: Target log-system selection menu layout
    print("\n📦 STEP 1: SELECT TARGET TELEMETRY SOURCE TO COMPROMISE:")
    print("   [1] Authentication Log Stream   (Simulate Brute Force/Credential stuffing)")
    print("   [2] System Error Log Subsystem  (Simulate Application Exploitation/Crashes)")
    print("   [3] Network Perimeter Gateway   (Simulate Port Mapping/Reconnaissance Scans)")
    print("   [4] Complete System Infrastructure (Simulate Full Enterprise Chain - ALL LOGS)")
    
    target_log = input("\nEnter log target selection (1-4): ").strip()
    if target_log not in ["1", "2", "3", "4"]:
        print("❌ Invalid selection matrix target context. Terminating configuration simulation.")
        return

    # Step 2: Choose Threat Multiplier Tier
    print("\n💥 STEP 2: SELECT ATTACK VOLUMETRIC INTENSITY MULTIPLIER LEVEL:")
    print("   [LOW]       Subtle anomalies, easily disguised as background environment jitter.")
    print("   [MEDIUM]    Clear pattern breakout. Traditional security rules trigger alerts.")
    print("   [HIGH]      Critical threshold anomalies. Operations are actively disrupted.")
    print("   [CRITICAL]  Emergency saturation event. Massive infrastructure overload footprint.")
    
    intensity = input("\nEnter intensity profile choice (LOW, MEDIUM, HIGH, CRITICAL): ").strip().upper()
    if intensity not in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]:
        print("❌ Invalid intensity profile index parameter matching. Terminating execution loop.")
        return

    # Step 3: Compile Custom Synthetic Log Stream Profile Variables
    simulation_payload = DynamicAttackMatrix.generate_custom_vector(target_log, intensity)
    
    # Run Analytics Pipeline Engine Flow
    discovered_threats = run_anomaly_detection(simulation_payload, anomaly_engine)
    
    # Step 4: Run Downstream Multi-stage CTI & GenAI Briefing
    if discovered_threats:
        tracker_meta = {"selected_target_code": target_log, "selected_intensity_tier": intensity}
        trigger_unified_intelligence_briefing(discovered_threats, tracker_meta, intel_engine, ai_engine)
    else:
        global_console.print("\n[bold yellow]⚪ SIMULATION COMPLETE:[/bold yellow] No persistent mathematical exceptions caught. AI routing omitted.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting attack configuration manager.")