import json
import numpy as np
from loguru import logger

class AttackClassifier:

    @staticmethod
    def classify(values: list, events: list = None) -> str:
        """
        Evaluates trend step changes and checks explicit log metadata 
        signatures to accurately classify the threat vector.
        """
        # 🎯 STRATEGY 1: Inspect explicit log signatures if they exist
        if events:
            for e in events:
                if not isinstance(e, dict):
                    continue
                
                # Check column-level attack type text
                sim_type = str(e.get("attack_type", "")).upper()
                if "BRUTE_FORCE" in sim_type:
                    return "BRUTE_FORCE"
                if "PORT_SCAN" in sim_type or "NETWORK_SCAN" in sim_type:
                    return "PORT_SCAN"
                if "DDOS" in sim_type or "DOS" in sim_type:
                    return "DOS_ATTACK"
                if "ERROR_STORM" in sim_type or "ERROR" in sim_type:
                    return "ERROR_STORM"
                
                # --- FIX: SAFE STRIP/LOAD ESCAPED JSON STRINGS ---
                raw_event = e.get("event", {})
                inner_event = {}
                
                if isinstance(raw_event, dict):
                    inner_event = raw_event
                elif isinstance(raw_event, str):
                    try:
                        inner_event = json.loads(raw_event)
                    except Exception:
                        inner_event = {}

                # Fallback to inspecting internal event messages safely
                if isinstance(inner_event, dict):
                    msg = str(inner_event.get("message", "")).upper()
                    subsystem = str(inner_event.get("subsystem", ""))
                    target = str(inner_event.get("target_endpoint", "")).upper()
                    
                    if "PORT" in msg or "SCAN" in msg:
                        return "PORT_SCAN"
                    if "LOGIN" in target or "AUTH" in target or "VERIFICATION" in msg:
                        return "BRUTE_FORCE"
                    if "STACK_TRACE" in inner_event or subsystem:
                        return "ERROR_STORM"

        # 🎯 STRATEGY 2: Fall back to pure mathematical formulas for regular traffic
        if not values or len(values) < 3:
            return "UNKNOWN_TRAFFIC"

        arr = np.array(values, dtype=float)
        diffs = np.diff(arr)

        if diffs[-1] > np.median(arr) * 5:
            return "BRUTE_FORCE"

        if len(diffs) >= 3 and all(x > 0 for x in diffs[-3:]):
            return "PORT_SCAN"

        if arr[-1] > np.mean(arr[:-3]) * 3:
            return "DOS_ATTACK"

        return "VOLUME_SPIKE"