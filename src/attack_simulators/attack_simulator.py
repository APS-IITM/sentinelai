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

# Mocking your structural additions to integrate seamlessly with standard execution flow
class AttackClassifier:
    @staticmethod
    def classify(values):
        if len(values) == 0: return "UNKNOWN"
        avg = sum(values) / len(values)
        peak = max(values)
        
        if peak > avg * 3: return "BRUTE_FORCE_ATTACK"
        if peak > avg * 2: return "NETWORK_SCAN"
        if avg > 100: return "ERROR_STORM"
        return "NORMAL_ACTIVITY"

class EventCorrelator:
    @staticmethod
    def _get_attr(e, key, default=None):
        if isinstance(e, dict): return e.get(key, default)
        return getattr(e, key, default)

    @staticmethod
    def correlate(events):
        if not events: return "UNKNOWN", 0
        attacks = set()
        for e in events:
            attack_type = EventCorrelator._get_attr(e, "attack_type", "UNKNOWN")
            attacks.add(attack_type)
        
        attacks.discard(None)
        attacks.discard("UNKNOWN")
        if not attacks: return "UNKNOWN", 0

        # Correlation logic tree routing
        if "BRUTE_FORCE_ATTACK" in attacks and "NETWORK_SCAN" in attacks: return "RECON_TO_CREDENTIAL_ATTACK", 90
        if "NETWORK_SCAN" in attacks and "DDOS_ATTACK" in attacks: return "RECON_TO_DDOS", 85
        if "BRUTE_FORCE_ATTACK" in attacks and "SYSTEM_EXPLOIT" in attacks: return "EXPLOITATION_CHAIN_ATTACK", 88
        if len(attacks) > 1: return "MULTI_STAGE_ATTACK", 75
        return list(attacks)[0], 60

# ==========================================
# 🛑 SECURITY SCENARIO MATRIX GENERATOR
# ==========================================
class DynamicAttackMatrix:
    """Generates precise volumetric spikes to trigger specific analytical branches."""
    
    BASELINE_AUTH = [12, 14, 15, 11, 13, 16, 12, 14, 15, 11, 13, 16, 14, 15, 12]
    BASELINE_ERR  = [2, 4, 3, 1, 2, 5, 2, 4, 3, 1, 2, 5, 3, 2, 4]
    BASELINE_NET  = [45, 52, 48, 50, 47, 55, 45, 52, 48, 50, 47, 55, 51, 49, 53]

    @classmethod
    def generate_custom_vector(cls, scenario_target: str, stage_profile: str) -> dict:
        """
        Builds specific analytical conditions:
        - BRUTE_FORCE_ATTACK: requires peak > avg * 3
        - NETWORK_SCAN: requires peak > avg * 2
        - ERROR_STORM: requires avg > 100
        """
        auth_stream = list(cls.BASELINE_AUTH)
        error_stream = list(cls.BASELINE_ERR)
        net_stream = list(cls.BASELINE_NET)

        title_suffix = f"[{stage_profile.upper()} MODE]"
        
        # Scenario 1: Authentication Attacks
        if scenario_target == "1":
            if stage_profile == "BRUTE_FORCE":
                auth_stream[-1] = int(sum(auth_stream) * 4) # Guarantees peak > avg * 3
            return {
                "title": f"Targeted Authentication Exploitation {title_suffix}",
                "desc": "Simulating high volume auth attempt patterns to isolate password spraying vectors.",
                "auth": auth_stream, "error": error_stream, "network": net_stream,
                "forced_classification": "BRUTE_FORCE_ATTACK"
            }
            
        # Scenario 2: System Exceptions / Resource Floods
        elif scenario_target == "2":
            if stage_profile == "ERROR_STORM":
                error_stream = [120, 140, 115, 130, 150, 110, 125, 135, 145, 160] # Guarantees avg > 100
            return {
                "title": f"Triggered Infrastructure Exception Storm {title_suffix}",
                "desc": "Flooding system error collection endpoints to saturate log logging storage engines.",
                "auth": auth_stream, "error": error_stream, "network": net_stream,
                "forced_classification": "ERROR_STORM"
            }
            
        # Scenario 3: Perimeter Scans
        elif scenario_target == "3":
            if stage_profile == "NETWORK_SCAN":
                net_stream[-1] = int(sum(net_stream) * 2.2) # Guarantees peak > avg * 2
            return {
                "title": f"Volumetric Network Perimeter Exfiltration Scan {title_suffix}",
                "desc": "Simulating widespread horizontal reconnaissance probing across internal firewalls.",
                "auth": auth_stream, "error": error_stream, "network": net_stream,
                "forced_classification": "NETWORK_SCAN"
            }
            
        # Scenario 4: Multi-Stage Cross-Functional Attack Chains
        elif scenario_target == "4":
            if stage_profile == "RECON_TO_CREDENTIAL":
                net_stream[-1] = int(sum(net_stream) * 2.2)
                auth_stream[-1] = int(sum(auth_stream) * 4)
            elif stage_profile == "EXPLOITATION_CHAIN":
                auth_stream[-1] = int(sum(auth_stream) * 4)
                error_stream = [110, 115, 120, 130, 105, 140, 110, 115, 125, 150]
            else: # Standard multi stage fallback 
                net_stream[-1] = int(sum(net_stream) * 2.2)
                error_stream = [110, 115, 120, 130, 105, 140, 110, 115, 125, 150]

            return {
                "title": f"Advanced Synchronized Multi-Stage Killchain {title_suffix}",
                "desc": "Coordinating interleaved cross-vector events to test relational heuristics logic rules.",
                "auth": auth_stream, "error": error_stream, "network": net_stream,
                "forced_classification": "MULTI_STAGE_CHAIN"
            }

# ==========================================
# 🚀 PIPELINE LIFECYCLE MANAGEMENT UTILITIES
# ==========================================
def run_anomaly_detection(data: dict, anomaly_engine) -> list:
    """Passes array payloads into the pipeline and maps classifications natively."""
    global_console.print(f"\n[bold gold1]─[/bold gold1]" * 60)
    global_console.print(f"📡 [bold white]EXECUTING VECTOR SIMULATION:[/bold white] {data['title']}")
    global_console.print(f"[dim]Description: {data['desc']}[/dim]")
    global_console.print(f"─" * 60)
    
    synthetic_events = []
    
    # Process Auth Track
    auth_class = AttackClassifier.classify(data['auth'])
    if auth_class != "NORMAL_ACTIVITY":
        global_console.print(f"  ⚠️  [ANOMALY FLAG] Authentication Core: Detected [bold red]{auth_class}[/bold red]")
        synthetic_events.append({"source": "Authentication Logs", "attack_type": auth_class, "severity": "HIGH"})
        
    # Process Error Track
    error_class = AttackClassifier.classify(data['error'])
    if error_class != "NORMAL_ACTIVITY":
        global_console.print(f"  ⚠️  [ANOMALY FLAG] System Exception Core: Detected [bold red]{error_class}[/bold red]")
        # Explicit override to map to specific MITRE rule criteria if parsing multi-stages
        type_label = "SYSTEM_EXPLOIT" if data.get("forced_classification") == "EXPLOITATION_CHAIN" else error_class
        synthetic_events.append({"source": "System Error Logs", "attack_type": type_label, "severity": "CRITICAL"})
        
    # Process Network Track
    net_class = AttackClassifier.classify(data['network'])
    if net_class != "NORMAL_ACTIVITY":
        global_console.print(f"  ⚠️  [ANOMALY FLAG] Network Perimeter Core: Detected [bold red]{net_class}[/bold red]")
        synthetic_events.append({"source": "Network Perimeter Logs", "attack_type": net_class, "severity": "MEDIUM"})

    if not synthetic_events:
        global_console.print("  [bold green]✅ SYSTEM STABLE:[/bold green] Array values evaluated as standard noise baseline profiles.")
        
    return synthetic_events

def trigger_unified_intelligence_briefing(aggregated_threats: list, selected_meta: dict, intel_engine, ai_engine):
    """Executes rule validation and invokes the Generative AI core analysis context."""
    global_console.print("\n" + "═" * 80)
    global_console.print(" 🛡️  SENTINELAI RULES ENGINE ENGINE CORRELATION LAYER ".center(80, "═"))
    global_console.print("═" * 80)
    
    # Direct execution of your custom EventCorrelator static code sequence
    correlation_signature, hazard_score = EventCorrelator.correlate(aggregated_threats)
    
    global_console.print(f" 🔹 Calculated Threat Signature Matrix : [bold gold1]{correlation_signature}[/bold gold1]")
    global_console.print(f" 🔹 Engine Matrix Confidence Score      : [ {hazard_score} / 100 ]")
    global_console.print(f" 🔹 Active Correlated Events Count      : [ {len(aggregated_threats)} Log Items ]")

    if ai_enabled and ai_engine:
        global_console.print("\n" + "═" * 80)
        global_console.print(" 🤖 AI SOC FORENSIC INTELLIGENCE TASK BRIEFING ".center(80, "═"))
        global_console.print("═" * 80)
        
        manifest = {
            "evaluation_timestamp": datetime.utcnow().isoformat() + "Z",
            "correlation_engine_summary": {
                "signature_match": correlation_signature,
                "global_severity_state": "HIGH" if hazard_score >= 75 else "MEDIUM",
                "hazard_score": hazard_score
            },
            "raw_incident_timeline": aggregated_threats
        }

        # Pack data cleanly inside your carrier event architecture
        class UnifiedThreatCarrier:
            def __init__(self, description, severity):
                self.description = description
                self.severity = severity

        payload_carrier = UnifiedThreatCarrier(json.dumps(manifest, indent=2), "CRITICAL" if hazard_score > 80 else "HIGH")

        with global_console.status("[bold white]Streaming scenario manifest parameters to Google Gemini Core...[/bold white]"):
            raw_markdown = ai_engine.analyze_event(payload_carrier)

        global_console.print("\n")
        global_console.print("[bold cyan]🤖 AI SOC ANALYST CORRELATED REPORT[/bold cyan]", justify="center")
        global_console.print("[dim]─" * global_console.width + "[/dim]")
        global_console.print(Markdown(raw_markdown))
        global_console.print("[dim]─" * global_console.width + "[/dim]\n")

# ==========================================
# 🏁 MAIN INTERACTIVE TERMINAL LOOP
# ==========================================
def main():
    global_console.print("[bold white]========================================================================[/bold white]")
    global_console.print(" 🛡️  SENTINELAI: TARGETED LOG EXTRACTION & ATTACK INTENSITY SIMULATOR ".center(80, " "))
    global_console.print("[bold white]========================================================================[/bold white]")

    anomaly_engine = AnomalyAnalyzer()
    intel_engine = IntelligenceEngine()
    ai_engine = AIAnalyzer() if ai_enabled else None

    # Step 1: Target Choice Matrix Selector
    print("\n📦 STEP 1: SELECT VECTOR SIMULATION PAIR CATEGORY:")
    print("   [1] Authentication Log Vectors")
    print("   [2] System Error Exception Architectures")
    print("   [3] Network Perimeter Gateway Routers")
    print("   [4] Correlated Multi-Stage Attack Chains (Cross-Telemetry)")
    
    target_log = input("\nEnter target index (1-4): ").strip()
    if target_log not in ["1", "2", "3", "4"]: return

    # Step 2: Adaptive Tier Routing Rules
    print("\n💥 STEP 2: SELECT PRECISE SIMULATION STAGE TARGET RULE:")
    stage_profile = ""
    if target_log == "1":
        print("   [BRUTE_FORCE] Sets peak > avg * 3 validation logic loops.")
        print("   [NORMAL]      Runs default user baseline environment noise loops.")
        choice = input("\nSelect Stage Target Profile: ").strip().upper()
        stage_profile = "BRUTE_FORCE" if choice == "BRUTE_FORCE" else "NORMAL"
    elif target_log == "2":
        print("   [ERROR_STORM] Overwrites list matrix indexes so total avg > 100.")
        print("   [NORMAL]      Runs default user baseline environment noise loops.")
        choice = input("\nSelect Stage Target Profile: ").strip().upper()
        stage_profile = "ERROR_STORM" if choice == "ERROR_STORM" else "NORMAL"
    elif target_log == "3":
        print("   [NETWORK_SCAN] Sets peak > avg * 2 validation logic loops.")
        print("   [NORMAL]      Runs default user baseline environment noise loops.")
        choice = input("\nSelect Stage Target Profile: ").strip().upper()
        stage_profile = "NETWORK_SCAN" if choice == "NETWORK_SCAN" else "NORMAL"
    elif target_log == "4":
        print("   [RECON_TO_CREDENTIAL] Triggers 'RECON_TO_CREDENTIAL_ATTACK' rule block (Score: 90).")
        print("   [EXPLOITATION_CHAIN]  Triggers 'EXPLOITATION_CHAIN_ATTACK' rule block (Score: 88).")
        print("   [STANDARD_MULTI]      Triggers basic 'MULTI_STAGE_ATTACK' rule block (Score: 75).")
        choice = input("\nSelect Stage Target Profile: ").strip().upper()
        if choice in ["RECON_TO_CREDENTIAL", "EXPLOITATION_CHAIN", "STANDARD_MULTI"]:
            stage_profile = choice
        else:
            stage_profile = "STANDARD_MULTI"

    # Process and build specific payloads
    simulation_payload = DynamicAttackMatrix.generate_custom_vector(target_log, stage_profile)
    discovered_threats = run_anomaly_detection(simulation_payload, anomaly_engine)
    
    if discovered_threats:
        tracker_meta = {"target_log_index": target_log, "stage_profile": stage_profile}
        trigger_unified_intelligence_briefing(discovered_threats, tracker_meta, intel_engine, ai_engine)
    else:
        global_console.print("\n[bold yellow]⚪ SIMULATION COMPLETE:[/bold yellow] Baseline limits maintained. Routing canceled.")

if __name__ == "__main__":
    main()