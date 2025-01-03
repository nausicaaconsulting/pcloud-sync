import hashlib

from sync import settings


def api_auth_secret_code():
    return hashlib.sha3_256(settings.SECRET_KEY.encode()).hexdigest()
