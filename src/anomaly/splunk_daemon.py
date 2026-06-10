import time
import sys
from loguru import logger

# Import your core Splunk infrastructure connection drivers
from src.splunk.client import connect, run_search
from src.splunk.queries import SplunkQueries

# Import your automated analysis pipeline engine elements
from src.anomaly.analyzer import AnomalyAnalyzer

# Configure Loguru output formatting for high-visibility terminal logging
logger.remove()
logger.add(
    sys.stdout, 
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level:7}</level> | <cyan>{message}</cyan>"
)


def run_soc_analysis_cycle(splunk_service, analyzer_instance):
    """
    Executes a single processing cycle: pulls metric trends out of Splunk,
    transforms row dictionaries into metrics, and feeds the anomaly engine.
    """
    logger.info("🔄 Commencing scheduled Splunk metric ingestion scan...")

    # 1. FETCH TREND DATA FROM THE SIEM VIA SPL
    # Uses the network transaction frequency trend query from your SplunkQueries class
    network_trend_query = SplunkQueries.network_trend()
    response = run_search(splunk_service, network_trend_query)

    if response.get("status") != "success":
        logger.error(f"❌ Splunk query execution failed: {response.get('message')}")
        return

    raw_events = response.get("data", [])
    logger.info(f"📊 Gathered {len(raw_events)} timeline data slices from the network index.")

    # A baseline window requires at least 10 entries for standard/ML model sanity
    if len(raw_events) < 10:
        logger.warning("⚠️ Insufficient data points returned from Splunk to calculate baseline variances. Skipping loop.")
        return

    # 2. TRANSFORM DICTIONARY ROW SEGMENTS INTO A SEQUENTIAL METRIC LIST
    # Extracts the raw hit count from each timeline slice to populate the values list
    try:
        metric_values = []
        for entry in raw_events:
            count_val = entry.get("count", 0)
            
            # Handle possible nested list arrays or string representations from Splunk Reader
            if isinstance(count_val, list):
                count_val = count_val[0]
            
            metric_values.append(float(count_val))

        logger.debug(f"📈 Raw metric timeline parsed for baseline verification: {metric_values}")

        # 3. CASCADE DIRECTLY INTO THE AUTOMATED DETECTION PIPELINE
        # The AnomalyAnalyzer runs math, tags MITRE vectors, and updates your Supabase tables.
        # We target the destination source name to match the index being actively scanned.
        analyzer_instance.analyze_series(source="splunk_network_index", values=metric_values)
        logger.success("✅ Ingestion cycle processed. Pipeline executed cleanly through to storage layers.")

    except Exception as transform_error:
        logger.error(f"❌ Failed to clean and process Splunk trend arrays: {str(transform_error)}")


def start_industrial_daemon(interval_seconds=30):
    """
    Spawns a continuous background worker daemon to poll your SIEM deployment
    independently of user interactions or frontend interface active states.
    """
    logger.info("🚀 Booting Industrial SOC Monitoring Daemon Loop...")
    
    try:
        splunk_service = connect()
        logger.success("🔌 Connected to Splunk Core Management API successfully via port 8089.")
    except Exception as conn_err:
        logger.critical(f"💥 Failed to establish initial Splunk management handshake: {str(conn_err)}")
        sys.exit(1)

    # Initialize a single persistent instance of your automated orchestrator
    analyzer_instance = AnomalyAnalyzer()
    logger.info(f"🧠 Local Anomaly and CTI engines active. Polling network trends every {interval_seconds} seconds.")

    try:
        while True:
            start_time = time.time()
            
            try:
                run_soc_analysis_cycle(splunk_service, analyzer_instance)
            except Exception as cycle_err:
                logger.error(f"⚠️ Unexpected error caught inside running daemon execution frame: {str(cycle_err)}")

            # Calculate actual processing execution lag to keep polling intervals uniform
            elapsed = time.time() - start_time
            sleep_time = max(1, interval_seconds - elapsed)
            time.sleep(sleep_time)

    except KeyboardInterrupt:
        logger.warning("🛑 Industrial SOC Daemon shutdown signal received. Terminating process cleanly.")


if __name__ == "__main__":
    # Run this file directly inside its own terminal window or background server thread context
    # Adjust interval_seconds to control your corporate monitoring frequency
    start_industrial_daemon(interval_seconds=30)