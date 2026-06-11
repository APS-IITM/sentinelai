from src.storage.base_store import BaseStore

class AttackLogStore(BaseStore):
    """
    Handles storage interactions for the Supabase simulated attack queue.
    Inherits save(), get_all(), latest(), and clear() from BaseStore.
    """
    TABLE_NAME = "simulated_attack_stream"
    
    @classmethod
    def delete_batch(cls, ids: list):
        """
        Extends the BaseStore to allow targeted deletions of specific log records.
        This prevents wiping out logs generated midway through a processing loop cycle.
        """
        if cls.TABLE_NAME is None:
            raise ValueError("TABLE_NAME not defined")
        if not ids:
            return None
            
        from src.storage.supabase_client import supabase
        return (
            supabase
            .table(cls.TABLE_NAME)
            .delete()
            .in_("id", ids)
            .execute()
        )