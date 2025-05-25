import json
import os

PREFS_FILE = "storage/user_preferences.json"

# Загружаем настройки при запуске
if os.path.exists(PREFS_FILE):
    with open(PREFS_FILE, "r", encoding="utf-8") as f:
        user_data = json.load(f)
else:
    user_data = {}

# 🔒 Гарантируем структуру
def _get_user(user_id):
    user_id = str(user_id)
    if user_id not in user_data:
        user_data[user_id] = {"language": "ru", "frequency": "daily"}
    return user_data[user_id]

def _save():
    with open(PREFS_FILE, "w", encoding="utf-8") as f:
        json.dump(user_data, f, ensure_ascii=False, indent=2)

# Язык
def set_user_language(user_id: int, lang: str):
    _get_user(user_id)["language"] = lang
    _save()

def get_user_language(user_id: int) -> str:
    return _get_user(user_id)["language"]

# Частота
def set_user_frequency(user_id: int, frequency: str):
    _get_user(user_id)["frequency"] = frequency
    _save()

def get_user_frequency(user_id: int) -> str:
    return _get_user(user_id)["frequency"]
