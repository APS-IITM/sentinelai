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
# 🧠 STATIC PRODUCTION ENGINE DEFINITIONS
# ==========================================
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

        if "BRUTE_FORCE_ATTACK" in attacks and "NETWORK_SCAN" in attacks: return "RECON_TO_CREDENTIAL_ATTACK", 90
        if "NETWORK_SCAN" in attacks and "DDOS_ATTACK" in attacks: return "RECON_TO_DDOS", 85
        if "BRUTE_FORCE_ATTACK" in attacks and "SYSTEM_EXPLOIT" in attacks: return "EXPLOITATION_CHAIN_ATTACK", 88
        if len(attacks) > 1: return "MULTI_STAGE_ATTACK", 75
        return list(attacks)[0], 60

class RiskScorer:
    @staticmethod
    def calculate(volume_score: int, anomaly_score: int):
        # Weighted fusion model: 60% Volume, 40% Anomaly Signature Weight
        score = (volume_score * 0.6) + (anomaly_score * 0.4)
        return min(int(score), 100)

    @staticmethod
    def severity(score: int):
        if score >= 85: return "CRITICAL"
        if score >= 70: return "HIGH"
        if score >= 50: return "MEDIUM"
        return "LOW"

# ==========================================
# 🛑 SECURITY SCENARIO MATRIX GENERATOR
# ==========================================
class DynamicAttackMatrix:
    """Generates precise metric streams engineered to force calculated risk states."""
    
    BASELINE_AUTH = [12, 14, 15, 11, 13, 16, 12, 14, 15, 11, 13, 16, 14, 15, 12]
    BASELINE_ERR  = [2, 4, 3, 1, 2, 5, 2, 4, 3, 1, 2, 5, 3, 2, 4]
    BASELINE_NET  = [45, 52, 48, 50, 47, 55, 45, 52, 48, 50, 47, 55, 51, 49, 53]

    @classmethod
    def generate_targeted_profile(cls, target_log: str, threat_level: str) -> dict:
        """
        Dynamically designs baseline arrays and overrides scores to safely map out 
        exact target outputs matching the RiskScorer specifications.
        """
        auth_stream = list(cls.BASELINE_AUTH)
        error_stream = list(cls.BASELINE_ERR)
        net_stream = list(cls.BASELINE_NET)
        
        # Configure static test matrix weights
        if threat_level == "CRITICAL":   # Goal: Score >= 85
            v_score, a_score = 95, 90
            auth_stream[-1] = int(sum(auth_stream) * 6)
            error_stream = [150] * 12
        elif threat_level == "HIGH":     # Goal: 70 <= Score < 85
            v_score, a_score = 75, 80
            net_stream[-1] = int(sum(net_stream) * 3)
        elif threat_level == "MEDIUM":   # Goal: 50 <= Score < 70
            v_score, a_score = 55, 60
            auth_stream[-1] = int(sum(auth_stream) * 3.2)
        else:                            # LOW Tier fallback / background noise
            v_score, a_score = 25, 30

        desc_meta = f"Testing system infrastructure limits at an explicit {threat_level} severity boundary."

        # Map execution streams based on selected components
        if target_log == "1":
            return {"title": f"Auth Stream Analysis [{threat_level}]", "desc": desc_meta, "auth": auth_stream, "error": list(cls.BASELINE_ERR), "network": list(cls.BASELINE_NET), "v": v_score, "a": a_score}
        elif target_log == "2":
            if threat_level in ["HIGH", "CRITICAL"]: error_stream = [130] * 10
            return {"title": f"System Exception Flooding [{threat_level}]", "desc": desc_meta, "auth": list(cls.BASELINE_AUTH), "error": error_stream, "network": list(cls.BASELINE_NET), "v": v_score, "a": a_score}
        elif target_log == "3":
            return {"title": f"Perimeter Ingress Diagnostics [{threat_level}]", "desc": desc_meta, "auth": list(cls.BASELINE_AUTH), "error": list(cls.BASELINE_ERR), "network": net_stream, "v": v_score, "a": a_score}
        else:
            # Multi-stage killchains activate all fields at once
            if threat_level in ["HIGH", "CRITICAL"]:
                auth_stream[-1] = int(sum(auth_stream) * 4)
                net_stream[-1] = int(sum(net_stream) * 3)
            return {"title": f"Full-Spectrum Enterprise Killchain [{threat_level}]", "desc": desc_meta, "auth": auth_stream, "error": error_stream, "network": net_stream, "v": v_score, "a": a_score}

# ==========================================
# 🚀 PIPELINE LIFECYCLE MANAGEMENT UTILITIES
# ==========================================
def run_anomaly_detection(data: dict) -> list:
    """Evaluates telemetry patterns and aggregates active events into triage payloads."""
    global_console.print(f"\n[bold gold1]─[/bold gold1]" * 60)
    global_console.print(f"📡 [bold white]EXECUTING TARGETED LOG EXTRACTION:[/bold white] {data['title']}")
    global_console.print(f"[dim]Scenario Meta: {data['desc']}[/dim]")
    global_console.print(f"─" * 60)
    
    synthetic_events = []
    
    auth_class = AttackClassifier.classify(data['auth'])
    if auth_class != "NORMAL_ACTIVITY":
        global_console.print(f"  ⚠️  [ANOMALY FLAG] Authentication Matrix Branch -> Isolated: [bold red]{auth_class}[/bold red]")
        synthetic_events.append({"source": "Authentication Logs", "attack_type": auth_class})
        
    error_class = AttackClassifier.classify(data['error'])
    if error_class != "NORMAL_ACTIVITY":
        global_console.print(f"  ⚠️  [ANOMALY FLAG] Internal Exception Branch -> Isolated: [bold red]{error_class}[/bold red]")
        # Inject contextual cross-over label if running multi-stage testing setups
        type_lbl = "SYSTEM_EXPLOIT" if "Full-Spectrum" in data['title'] else error_class
        synthetic_events.append({"source": "System Error Logs", "attack_type": type_lbl})
        
    net_class = AttackClassifier.classify(data['network'])
    if net_class != "NORMAL_ACTIVITY":
        global_console.print(f"  ⚠️  [ANOMALY FLAG] Boundary Interface Network -> Isolated: [bold red]{net_class}[/bold red]")
        synthetic_events.append({"source": "Network Perimeter Logs", "attack_type": net_class})

    if not synthetic_events:
        global_console.print("  [bold green]✅ CONSOLE QUIET:[/bold green] Injected streams settled cleanly within noise limits.")
        
    return synthetic_events

def trigger_unified_intelligence_briefing(aggregated_threats: list, simulation_payload: dict, ai_engine):
    """Executes rule classification, calculates matrix scores, and pipes briefs to the AI console."""
    global_console.print("\n" + "═" * 80)
    global_console.print(" 🛡️  SENTINELAI SECURITY LAYER ORCHESTRATION INTERFACE ".center(80, "═"))
    global_console.print("═" * 80)
    
    # 1. Run Correlator Engine
    correlation_signature, correlation_confidence = EventCorrelator.correlate(aggregated_threats)
    
    # 2. Compute Risk Metrics via RiskScorer
    raw_v = simulation_payload["v"]
    raw_a = simulation_payload["a"]
    computed_score = RiskScorer.calculate(raw_v, raw_a)
    severity_label = RiskScorer.severity(computed_score)
    
    # Render Metrics Panel Dashboard layout via terminal colors
    sev_colors = {"CRITICAL": "bold red", "HIGH": "bold orange1", "MEDIUM": "bold yellow", "LOW": "bold green"}
    chosen_color = sev_colors.get(severity_label, "bold white")
    
    print(f" 🔹 Calculated Threat Signature Matrix : [bold gold1]{correlation_signature}[/bold gold1]")
    print(f" 🔹 Correlator Core Base Score         : {correlation_confidence}/100")
    print(f" 🔹 Injected Volumetric Metric Value   : {raw_v}")
    print(f" 🔹 Injected Anomaly Signature Value    : {raw_a}")
    global_console.print(f" 🔹 Fusion Core Consolidated Score     : [bold white]{computed_score}[/bold white]/100")
    global_console.print(f" 🔹 Determined Operational Severity    : [{chosen_color}]{severity_label}[/{chosen_color}]")

    # 3. Trigger Autonomous Generative Analysis Pipeline
    if ai_enabled and ai_engine:
        global_console.print("\n" + "═" * 80)
        global_console.print(" 🤖 AI SOC FORENSIC INTELLIGENCE INTERFACE DISPATCH ".center(80, "═"))
        global_console.print("═" * 80)
        
        manifest_payload = {
            "evaluation_timestamp": datetime.utcnow().isoformat() + "Z",
            "risk_scoring_matrix": {
                "calculated_fusion_score": computed_score,
                "assigned_severity_profile": severity_label,
                "input_volume_weight": raw_v,
                "input_anomaly_weight": raw_a
            },
            "correlation_engine_summary": {
                "signature_match": correlation_signature,
                "rule_confidence_rating": correlation_confidence
            },
            "tracked_anomalies_list": aggregated_threats
        }

        class SyntheticCarrier:
            def __init__(self, text, sev):
                self.description = text
                self.severity = sev

        carrier_instance = SyntheticCarrier(json.dumps(manifest_payload, indent=2), severity_label)

        with global_console.status("[bold white]Streaming scenario manifest parameters to Google Gemini Core...[/bold white]"):
            raw_markdown = ai_engine.analyze_event(carrier_instance)

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
    global_console.print(" 🛡️  SENTINELAI: ADVANCED ADAPTIVE ATTACK & RISK LEVEL SIMULATOR ".center(80, " "))
    global_console.print("[bold white]========================================================================[/bold white]")

    ai_engine = AIAnalyzer() if ai_enabled else None

    # Step 1: Select Telemetry Target Index
    print("\n📦 STEP 1: CHOOSE TARGET INGESTION SINK PROFILE:")
    print("   [1] Authentication Telemetry Pipeline Logs")
    print("   [2] System Error Core Application Logs")
    print("   [3] Network Boundary Gateway Device Logs")
    print("   [4] Full Multi-Tier Infrastructure Chain (All Sinks Interleaved)")
    
    target_log = input("\nEnter log target index option (1-4): ").strip()
    if target_log not in ["1", "2", "3", "4"]:
        print("❌ Invalid target index parameter matrix selector.")
        return

    # Step 2: Select Explicit Risk Severity Tier
    print("\n💥 STEP 2: CHOOSE TARGET ATTACK LEVEL SEVERITY PROFILE MATRIX:")
    print("   [LOW]      Simulates standard environmental shifts.      (Risk Range: 0-49)")
    print("   [MEDIUM]   Triggers threshold warning flags.            (Risk Range: 50-69)")
    print("   [HIGH]     Generates notable perimeter warnings.         (Risk Range: 70-84)")
    print("   [CRITICAL] Executes full infrastructural exploit storm.  (Risk Range: 85-100)")
    
    threat_level = input("\nEnter attack profile target level (LOW, MEDIUM, HIGH, CRITICAL): ").strip().upper()
    if threat_level not in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]:
        print("❌ Unknown severity layer variable declaration.")
        return

    # Process and build specific payloads
    simulation_payload = DynamicAttackMatrix.generate_targeted_profile(target_log, threat_level)
    discovered_threats = run_anomaly_detection(simulation_payload)
    
    # Process analytical outputs even if list arrays are empty to validate Low-severity metrics loops
    trigger_unified_intelligence_briefing(discovered_threats, simulation_payload, ai_engine)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting attack configuration manager safely.")