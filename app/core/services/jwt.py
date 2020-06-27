from typing import Dict

from jwt import decode, encode

from app.settings import settings, Settings


class JWTService:
    def __init__(self, settings: Settings = settings):
        self.settings = settings

    def generate_token(self, payload: Dict) -> str:
        return encode(
            payload=payload,
            key=self.settings.JWT_PRIVATE_KEY,
            algorithm=self.settings.JWT_ALGORITHM,
        ).decode(encoding="utf-8")

    def verify_token(self, token: str) -> Dict:
        return decode(
            jwt=token,
            key=self.settings.JWT_PUBLIC_KEY,
            algorithms=[self.settings.JWT_ALGORITHM],
        )
