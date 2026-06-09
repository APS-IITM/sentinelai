from src.storage.supabase_client import supabase


class BaseStore:

    TABLE_NAME = None

    @classmethod
    def save(cls, record):

        if cls.TABLE_NAME is None:
            raise ValueError(
                "TABLE_NAME not defined"
            )

        return (
            supabase
            .table(cls.TABLE_NAME)
            .insert(record)
            .execute()
        )

    @classmethod
    def get_all(cls):

        if cls.TABLE_NAME is None:
            raise ValueError(
                "TABLE_NAME not defined"
            )

        response = (
            supabase
            .table(cls.TABLE_NAME)
            .select("*")
            .execute()
        )

        return response.data or []

    @classmethod
    def latest(cls):

        if cls.TABLE_NAME is None:
            raise ValueError(
                "TABLE_NAME not defined"
            )

        response = (
            supabase
            .table(cls.TABLE_NAME)
            .select("*")
            .order(
                "created_at",
                desc=True
            )
            .limit(1)
            .execute()
        )

        data = response.data or []

        return data[0] if data else None

    @classmethod
    def clear(cls):

        if cls.TABLE_NAME is None:
            raise ValueError(
                "TABLE_NAME not defined"
            )

        supabase.table(
            cls.TABLE_NAME
        ).delete().neq(
            "id",
            0
        ).execute()