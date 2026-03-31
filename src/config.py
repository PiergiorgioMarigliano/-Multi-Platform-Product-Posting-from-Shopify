"""
Multi-Poster - Configuration Manager.
Loads credentials from the .env file in the same directory.
"""
import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    # Load .env file from the script's directory
    env_path = Path(__file__).parent / ".env"
    load_dotenv(env_path)
except ImportError:
    # python-dotenv not installed, fall back to system environment variables
    pass


def _get(key: str, default: str = "") -> str:
    """Read an environment variable, stripping whitespace."""
    return os.environ.get(key, default).strip()


# ============================================================
# TELEGRAM
# ============================================================
TELEGRAM_BOT_TOKEN = _get("TELEGRAM_BOT_TOKEN")

TELEGRAM_CHANNEL_IDS = [
    cid for cid in [
        _get("TELEGRAM_CHANNEL_ID_1"),
        _get("TELEGRAM_CHANNEL_ID_2"),
    ] if cid
]

# ============================================================
# WHATSAPP BUSINESS (Cloud API)
# ============================================================
WHATSAPP_TOKEN = _get("WHATSAPP_TOKEN")
WHATSAPP_PHONE_NUMBER_ID = _get("WHATSAPP_PHONE_NUMBER_ID")

WHATSAPP_GROUP_IDS = [
    gid for gid in [
        _get("WHATSAPP_GROUP_ID_1"),
        _get("WHATSAPP_GROUP_ID_2"),
    ] if gid
]

# ============================================================
# META (Facebook + Instagram)
# ============================================================
META_PAGE_ACCESS_TOKEN = _get("META_PAGE_ACCESS_TOKEN")
FACEBOOK_PAGE_ID = _get("FACEBOOK_PAGE_ID")
INSTAGRAM_ACCOUNT_ID = _get("INSTAGRAM_ACCOUNT_ID")
