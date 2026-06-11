import os
import json
from typing import List, Dict, Any
from src.storage.attack_log_store import AttackLogStore


class AttackRunner:

    def __init__(self, filename: str = "attack_stream.log"):
        """
        Initialized with fallback default configurations. 
        Note: File-handling structures are bypassed in favor of Supabase Cloud Store.
        """
        self.file_path = filename

    def push(self, events: List[Dict[str, Any]], attack_type: str) -> None:
        """
        Pushes wrapped simulation data records up to Supabase via AttackLogStore.
        """
        if not events:
            return

        try:
            # Batch record insertion into your Supabase database tier
            for e in events:
                AttackLogStore.save(e)
                
            print(f"[SUCCESS] Streamed {len(events)} '{attack_type}' simulation logs directly to Supabase cloud table.")
            
        except Exception as err:
            print(f"[FATAL WRITER EXCEPTION] Supabase pipeline stream writing error: {str(err)}")