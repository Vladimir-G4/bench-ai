# benchai/utils.py

import difflib
import logging
from typing import Optional

# Initialize logger
logger = logging.getLogger("benchai")
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
formatter = logging.Formatter("🧪 [%(levelname)s] %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# === General Helpers ===

def fuzzy_score(a: str, b: str) -> float:
    """Return fuzzy match score between two strings."""
    return difflib.SequenceMatcher(None, a.strip().lower(), b.strip().lower()).ratio()

def short(s: str, max_len: int = 80) -> str:
    return s if len(s) <= max_len else s[:max_len - 3] + "..."

def log_success(message: str):
    logger.info(f"✅ {message}")

def log_failure(message: str):
    logger.warning(f"❌ {message}")

def log_debug(message: str):
    logger.debug(f"🐞 {message}")

def log_error(message: str):
    logger.error(f"💥 {message}")
