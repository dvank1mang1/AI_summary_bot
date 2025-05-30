import json
import os
from datetime import datetime

PREFS_FILE = "storage/user_preferences.json"


if os.path.exists(PREFS_FILE):
    with open(PREFS_FILE, "r", encoding="utf-8") as f:
        user_data = json.load(f)
else:
    user_data = {}


def _get_user(user_id):
    user_id = str(user_id)
    if user_id not in user_data:
        user_data[user_id] = {
        "language": "ru", 
        "frequency": "daily",
        "size": "normal",
        "last_sent": None
        }
    return user_data[user_id]

#save
def _save():
    with open(PREFS_FILE, "w", encoding="utf-8") as f:
        json.dump(user_data, f, ensure_ascii=False, indent=2)


#user language
def set_user_language(user_id: int, lang: str):
    _get_user(user_id)["language"] = lang
    _save()

def get_user_language(user_id: int) -> str:
    return _get_user(user_id)["language"]


#user frequency
def set_user_frequency(user_id: int, frequency: str):
    _get_user(user_id)["frequency"] = frequency
    _save()

def get_user_frequency(user_id: int) -> str:
    return _get_user(user_id)["frequency"]


#user size
def set_user_size(user_id: int, size: str):
    _get_user(user_id)["size"] = size
    _save()

def get_user_size(user_id: int) -> str:
    return _get_user(user_id)["size"]


#user last sent
def set_last_sent(user_id: int, send_time: datetime):
    _get_user(user_id)["last_sent"] = send_time.isoformat()
    _save()

def get_last_sent(user_id: int):
    raw = _get_user(user_id)["last_sent"]
    if raw:
        return datetime.fromisoformat(raw)
    return None


def get_all_user_ids():
    return [int(uid) for uid in user_data.keys()]