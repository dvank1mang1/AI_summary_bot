from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict, List

from aiogram import Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder

_ARTICLES_PATH = Path("articles.json")
_MAX_LEN = 800
INTRO = "🚀 Свежее из мира нейросетей:\n\n"
OUTRO = "\n\nНажми «Узнать больше», чтобы вникнуть в тему!"
BTN_TEXT = "➡️ Узнать больше"


def _style(text: str) -> str:
    text = text.strip().replace("Источник", "").replace("  ", " ")
    if len(text) > _MAX_LEN:
        text = text[:_MAX_LEN] + "…"

    text = (
        text.replace("Machine Learning", "машинное обучение 📊")
        .replace("GPT", "GPT 🤖")
        .replace("AI", "AI 🧠")
    )
    return INTRO + text + OUTRO


def _prepare(path: Path) -> List[Dict]:
    data = json.loads(path.read_text("utf-8"))
    ready = []
    for art in data:
        ready.append({
            "text": _style(art["text"]),
            "url": art["url"],
            "date": art["date"],
            "title": art.get("title", "")
        })
    return ready


async def publish_articles(bot: Bot,
                           json_path: Path = _ARTICLES_PATH,
                           target_chat: int | str | None = None):
    channel_id = target_chat or os.getenv("TG_CHANNEL_ID")
    if not channel_id:
        raise RuntimeError("Neither target_chat nor TG_CHANNEL_ID set")

    arts = _prepare(json_path)
    for i, art in enumerate(arts):
        kb = InlineKeyboardBuilder()
        kb.button(text=BTN_TEXT, callback_data=f"more:{i}")
        await bot.send_message(
            channel_id,
            art["text"],
            reply_markup=kb.as_markup(),
            parse_mode="HTML",
            disable_web_page_preview=True,
        )
