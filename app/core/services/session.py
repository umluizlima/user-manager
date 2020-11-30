from uuid import uuid4

from app.core.adapters import CacheAdapter
from app.settings import Settings


class SessionService:
    def __init__(self, settings: Settings, cache_adapter: CacheAdapter):
        self._settings = settings
        self._cache_adapter = cache_adapter

    def generate_session(self, user_id: int) -> str:
        session_id = str(uuid4())
        self._cache_adapter.add_to_set(self._get_sessions_key(user_id), session_id)
        self._cache_adapter.set_with_expiration(
            self._get_session_key(session_id),
            self._settings.SESSION_EXPIRATION_SECONDS,
            user_id,
        )
        return session_id

    def verify_session(self, session_id: str) -> int:
        user_id = self._cache_adapter.get(self._get_session_key(session_id))
        if not user_id or not self._cache_adapter.is_in_set(
            self._get_sessions_key(user_id), session_id,
        ):
            return
        return int(user_id)

    def revoke_session(self, user_id: int, session_id: str):
        self._cache_adapter.remove_from_set(self._get_sessions_key(user_id), session_id)

    def revoke_all_sessions(self, user_id: int):
        self._cache_adapter.empty_set(self._get_sessions_key(user_id))

    @staticmethod
    def _get_session_key(session_id: str) -> str:
        return f"session:{session_id}"

    @staticmethod
    def _get_sessions_key(user_id: int) -> str:
        return f"user:{user_id}:sessions"
