from typing import Dict

from jwt import decode, encode

from app.settings import Settings


class JWTService:
    def __init__(self, settings: Settings):
        self._settings = settings

    def generate_token(self, payload: Dict) -> str:
        return encode(
            payload=payload,
            key=self._settings.JWT_PRIVATE_KEY,
            algorithm=self._settings.JWT_ALGORITHM,
        ).decode(encoding="utf-8")

    def verify_token(self, token: str) -> Dict:
        return decode(
            jwt=token,
            key=self._settings.JWT_PUBLIC_KEY,
            algorithms=[self._settings.JWT_ALGORITHM],
        )
