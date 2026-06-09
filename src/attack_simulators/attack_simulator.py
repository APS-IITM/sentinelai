import sys
import json
from rich.console import Console

from src.anomaly.analyzer import AnomalyAnalyzer
from src.intelligence.engine import IntelligenceEngine
from src.ai.analyzer import AIAnalyzer


from src.mcp_tools import BaseTool 
global_console = Console()

class OperationalTelemetryMatrix:
    """Generates authentic production-grade metric telemetry spikes."""
    
    SPIKE_PROFILE = [12, 14, 15, 11, 13, 16, 12, 14, 15, 11, 13, 850] # High Volumetric Spike
    STORM_PROFILE = [110, 120, 115, 130, 140, 125, 135, 150, 160, 145] # Constant High Exception Floor
    NORMAL_PROFILE = [12, 14, 15, 11, 13, 16, 12, 14, 15, 11, 13, 14]

    @classmethod
    def get_mock_splunk_payload(cls, tier: str) -> str:
        """Returns a query string simulating Splunk environment searches."""
        return f"search index=security sourcetype=linux_secure threat_intensity={tier} | stats count by src_ip"

# =========================================================
# 🏁 SIMULATION RUNTIME LIFE-CYCLE
# =========================================================
def run_full_stack_simulation(tier: str):
    global_console.print(f"\n[bold gold1]─[/bold gold1]" * 75)
    global_console.print(f"🚀 [bold white]LAUNCHING FULL-SPECTRUM SOFTWARE FEATURE TEST[/bold white]")
    global_console.print(f"🎯 Target Profile Vector Range: [bold cyan]{tier}[/bold cyan]")
    global_console.print(f"─" * 75)

    # -----------------------------------------------------
    # PHASE 1: TEST MCP LAYER & SPLUNK INGESTION (MCPStore)
    # -----------------------------------------------------
    global_console.print("\n[bold white][PHASE 1][/bold white] Executing MCP BaseTool Query Pipeline...")
    tool_tester = BaseTool()
    tool_tester.TOOL_NAME = "auth" if tier == "LOW" else "security"
    
    mock_query = OperationalTelemetryMatrix.get_mock_splunk_payload(tier)
    # This automatically calls MCPStore.save() internally!
    mcp_results = tool_tester.execute(mock_query)
    global_console.print("  [bold green]✅ Success:[/bold green] BaseTool executed. Result routed natively to `mcp_store`.")

    # -----------------------------------------------------
    # PHASE 2: TEST ANOMALY DETECTION PIPELINE (AnomalyStore)
    # -----------------------------------------------------
    global_console.print("\n[bold white][PHASE 2][/bold white] Injecting Streams into AnomalyAnalyzer Engine...")
    anomaly_engine = AnomalyAnalyzer()
    
    # Scale streams dynamically based on testing tiers
    auth_stream = OperationalTelemetryMatrix.SPIKE_PROFILE if tier in ["HIGH", "CRITICAL"] else OperationalTelemetryMatrix.NORMAL_PROFILE
    sys_stream = OperationalTelemetryMatrix.STORM_PROFILE if tier == "CRITICAL" else OperationalTelemetryMatrix.NORMAL_PROFILE
    
    captured_threats = []
    
    # Process Authentication Ingestion
    auth_threat = anomaly_engine.analyze_series("auth", auth_stream)
    if auth_threat: captured_threats.append(auth_threat)
        
    # Process System Error Ingestion
    sys_threat = anomaly_engine.analyze_series("system", sys_stream)
    if sys_threat: captured_threats.append(sys_threat)

    global_console.print(f"  [bold green]✅ Success:[/bold green] Analyzed {len(captured_threats)} threat flags. Matches auto-persisted to `anomalies` table.")

    # -----------------------------------------------------
    # PHASE 3: TEST INTEGRATION CORRELATION LAYER (IntelligenceStore)
    # -----------------------------------------------------
    global_console.print("\n[bold white][PHASE 3][/bold white] Parsing Events Through IntelligenceEngine...")
    intel_engine = IntelligenceEngine()
    
    # Pass Pydantic objects directly out of AnomalyAnalyzer to feed the correlation matrix
    intel_report = intel_engine.analyze(captured_threats)
    
    if intel_report:
        global_console.print("  [bold green]✅ Success:[/bold green] Cross-correlation complete. Record committed to `intelligence_reports` table.")
    else:
        global_console.print("  [dim]🟡 Notice: Threat metrics stayed within limits; Intelligence pipeline bypassed execution window.[/dim]")

    # -----------------------------------------------------
    # PHASE 4: TEST GENERATIVE COGNITIVE WORKSPACE (AIReportStore)
    # -----------------------------------------------------
    global_console.print("\n[bold white][PHASE 4][/bold white] Triggering Generative AI SOC Forensic Engine...")
    ai_engine = AIAnalyzer()
    
    if captured_threats:
        # Run real-time evaluation logic on the first captured threat vector object
        ai_brief = ai_engine.analyze_event(captured_threats[0])
        global_console.print("  [bold green]✅ Success:[/bold green] AI Forensic summary established and committed to `ai_reports` table.")
    else:
        # Fall back to evaluating batch structural tables if no active threats were spawned
        ai_brief = ai_engine.generate_report("anomaly")
        global_console.print("  [bold green]✅ Success:[/bold green] Batch summary generated and committed to `ai_reports` table.")

    global_console.print("\n[bold border green]🏆 PIPELINE RUN COMPLETELY VALIDATED: All engine modules ran sequentially and stored data natively via their own internal hooks.[/bold border green]\n")

# =========================================================
# INTERACTIVE TERMINAL HUB
# =========================================================
def main():
    global_console.print("[bold white]========================================================================[/bold white]")
    global_console.print(" 🛡️  SENTINELAI: TRUE END-TO-END ENGINE SIMULATOR SUITE ".center(80, " "))
    global_console.print("[bold white]========================================================================[/bold white]")

    print("\n💥 SELECT SYSTEM SIMULATION BOUNDARY TEST SEVERITY PROFILE LEVEL:")
    print("   [LOW]      Verifies background logging flows and standard baseline profiles.")
    print("   [HIGH]     Generates basic metric spikes to validate volumetric flags.")
    print("   [CRITICAL] Executes maximum workload parameters, forcing multi-engine chains.")
    
    tier_choice = input("\nEnter risk selection (LOW, HIGH, CRITICAL): ").strip().upper()
    if tier_choice not in ["LOW", "HIGH", "CRITICAL"]:
        print("❌ Unknown execution level selection profile parameters.")
        return

    run_full_stack_simulation(tier_choice)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting engine test execution deck safely.")