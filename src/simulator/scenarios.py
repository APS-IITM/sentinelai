import random
import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any


class AttackScenarios:

    @staticmethod
    def get_scaling_factors(severity: str) -> dict:
        """
        Returns volumetric scale sizes and specific keyword modifiers 
        dependent on the randomized target baseline threat context.
        """
        configs = {
            "LOW": {"count": random.randint(5, 12), "weight": [0.7, 0.2, 0.1, 0.0]},
            "MEDIUM": {"count": random.randint(15, 30), "weight": [0.2, 0.6, 0.15, 0.05]},
            "HIGH": {"count": random.randint(45, 90), "weight": [0.05, 0.15, 0.6, 0.2]},
            "CRITICAL": {"count": random.randint(150, 350), "weight": [0.0, 0.05, 0.25, 0.7]}
        }
        return configs.get(severity.upper(), configs["LOW"])

    @staticmethod
    def brute_force(severity: str) -> List[Dict[str, Any]]:
        events = []
        cfg = AttackScenarios.get_scaling_factors(severity)
        targets = ["/api/v1/auth/login", "/admin/wp-login.php", "/ssh/v2", "/v2/oauth/token"]
        
        msg_map = {
            "LOW": "Transient single-account authentication authentication failure check",
            "MEDIUM": "Repeated verification failures detected matching standard user credentials signatures",
            "HIGH": "Distributed brute force dictionary evaluation matching active parallel cracking tooling profiles",
            "CRITICAL": "Massive credential stuffing campaign matching known botnet dictionary sets. Local authentication service latency spike registered."
        }

        for _ in range(cfg["count"]):
            events.append({
                "message": msg_map[severity],
                "target_endpoint": random.choice(targets),
                "attempt_ip": f"{random.randint(100,240)}.{random.randint(10,254)}.{random.randint(1,254)}.{random.randint(1,254)}",
                "user_agent": random.choice(["Hydra Bruteforcer Suite/9.5", "Medusa-SSH/2.2", "Mozilla/5.0 (Botnet Node Override)"]) if severity in ["HIGH", "CRITICAL"] else "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            })
        return events

    @staticmethod
    def port_scan(severity: str) -> List[Dict[str, Any]]:
        events = []
        cfg = AttackScenarios.get_scaling_factors(severity)
        
        # Scale range of target network asset scanning exposure matrix
        base_ports = [22, 23, 80, 443, 8080, 3306, 5432, 1521, 27017, 6379, 8443]
        selected_ports = random.sample(base_ports, min(len(base_ports), max(3, cfg["count"] // 5))) if severity != "CRITICAL" else base_ports

        msg_map = {
            "LOW": "Isolated standard TCP SYN probe flag baseline discovery checking trace",
            "MEDIUM": "Sequential host asset port scan sweeping across targeted framework interfaces",
            "HIGH": "Aggressive TCP/UDP full-range structural scanning matrix matching automated mapping suites",
            "CRITICAL": "Complete network infrastructure enumeration sweep detected. Perimeter multi-vector system reconnaissance mapping in progress."
        }

        for p in selected_ports:
            for _ in range(max(1, cfg["count"] // len(selected_ports))):
                events.append({
                    "message": msg_map[severity],
                    "targeted_port": p,
                    "scan_type": "SYN-Sweep-Nmap" if severity in ["LOW", "MEDIUM"] else "Full-Connect-Intrusive-XMAS-Scan"
                })
        return events

    @staticmethod
    def ddos(severity: str) -> List[Dict[str, Any]]:
        cfg = AttackScenarios.get_scaling_factors(severity)
        
        msg_map = {
            "LOW": "Micro volumetric edge buffer ingress spikes within nominal baseline variations",
            "MEDIUM": "Layer 7 endpoint application service flood targeting operational index routes",
            "HIGH": "Ingress pipe bandwidth saturation threshold tracking high-volume volumetric exhaustion patterns",
            "CRITICAL": "Severe distributed reflective amplification flood cascading global routing connection drops"
        }

        return [{
            "message": msg_map[severity],
            "pps_count": random.randint(1000, 5000) if severity == "LOW" else random.randint(120000, 1500000),
            "drop_percentage": round(random.uniform(0.0, 5.0), 2) if severity == "LOW" else round(random.uniform(25.5, 98.4), 2)
        } for _ in range(cfg["count"])]

    @staticmethod
    def error_storm(severity: str) -> List[Dict[str, Any]]:
        cfg = AttackScenarios.get_scaling_factors(severity)
        services = ["auth-worker", "payment-gateway", "db-pool-router", "api-gateway-edge"]
        
        msg_map = {
            "LOW": "Intermittent remote connection reset tracking standard operational timeouts",
            "MEDIUM": "Elevated component error responses signaling microservices container pressure warnings",
            "HIGH": "Fatal cascading memory heap allocations breaking pipeline tracking thread structures",
            "CRITICAL": "Total upstream infrastructure exception pool drain. Database connection pool exhausted, deadlocking production routing loops."
        }

        return [{
            "message": msg_map[severity],
            "subsystem": random.choice(services),
            "stack_trace": "NullReferenceException at core.internal.allocator.invoke()" if severity in ["LOW", "MEDIUM"] else "Fatal OOMError: Thread Allocation Context Exhausted inside db_pool.rs:line_341"
        } for _ in range(cfg["count"])]

    @staticmethod
    def wrap(events: List[Dict[str, Any]], attack_type: str, source: str, severity: str) -> List[Dict[str, Any]]:
        """
        Wraps logs natively assigning timestamps, UUID sequences, and enforcing 
        the specific parent structural severity level calculated by the simulator.
        """
        wrapped = []
        for e in events:
            wrapped.append({
                "event_id": str(uuid.uuid4()),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "source": source,
                "attack_type": attack_type,
                "severity": severity.upper(),
                "event": e
            })
        return wrapped