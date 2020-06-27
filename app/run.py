from .api import create_api
from .settings import get_settings

settings = get_settings()
api = create_api(settings)
