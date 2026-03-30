from __future__ import annotations

import json
import time
from pathlib import Path

STATE_FILE = Path('.faceplay_state.json')


def read_event() -> dict:
    if not STATE_FILE.exists():
        return {}
    try:
        return json.loads(STATE_FILE.read_text(encoding='utf-8'))
    except Exception:
        return {}


def event_recent(payload: dict, max_age_sec: float = 0.5) -> bool:
    ts = payload.get('ts', 0)
    return (time.time() - ts) <= max_age_sec
