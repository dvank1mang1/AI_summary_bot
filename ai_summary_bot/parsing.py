from __future__ import annotations

import asyncio
import json
import os
import re
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List
from datetime import datetime, timedelta

from dotenv import load_dotenv
from telethon import TelegramClient

load_dotenv()

API_ID: int = int(os.getenv("TG_API_ID", "0"))
API_HASH: str | None = os.getenv("TG_API_HASH")

CHANNELS: list[str] = [
    "@ChatGPT_BIAbotRUS",
    "@incubeai_pro",
    "@ai2smm",
    "@hiaimedia",
    "@GPTMainNews",
    "@seeallochnaya",
    "@ai_newz",
    "@Artificial_intelligence_in",
    "@ftsec",
    "@Castalia_Ai",
]

from ai.bayesian_model import select_important as bayesian_filter
from ai.fdr_model import select_important as fdr_filter
from ai.logreg_model import select_important as logreg_filter
from ai.tfidf_model import select_important as tfidf_filter
from ai.zscore_model import select_important as zscore_filter

MODEL_OPTIONS = {
    "bayesian": bayesian_filter,
    "fdr": fdr_filter,
    "logreg": logreg_filter,
    "tfidf": tfidf_filter,
    "zscore": zscore_filter,
}
MODELS_TO_USE = list(MODEL_OPTIONS.keys())

def _clean(text: str) -> str:
    text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n+", " ", text)
    text = re.sub(r"[\W_]+", " ", text)
    return text.strip()

async def _fetch(client: TelegramClient, limit: int = 30) -> List[Dict[str, Any]]:
    all_articles: list[dict[str, Any]] = []
    ok, fail = 0, 0

    for ch in CHANNELS:
        try:
            batch: list[dict[str, Any]] = []
            async for m in client.iter_messages(ch, limit=limit):
                if m.text and len(m.text.strip()) > 5:
                    first_line = m.text.strip().split("\n")[0]
                    if len(first_line) > 200:
                        first_line = first_line[:200].rsplit(" ", 1)[0] + "..."
                    title = first_line
                    batch.append(
                        {
                            "channel": ch,
                            "message_id": m.id,
                            "title": title,
                            "text": _clean(m.text),
                            "date": m.date,
                            "url": f"https://t.me/{ch[1:]}/{m.id}",
                        }
                    )
            if batch:
                ok += 1
                all_articles.extend(batch)
        except Exception as e:
            print(f"⚠️  {ch}: {e}")
            fail += 1

    print(f"Fetched from {ok} channels (errors: {fail})")
    return all_articles

def _filter(articles: list[dict[str, Any]]) -> list[dict[str, Any]]:
    current_time = datetime.utcnow()

    print(f"Всего статей до фильтрации: {len(articles)}")

    articles = [
        a for a in articles 
        if (current_time - (datetime.fromisoformat(a["date"]).replace(tzinfo=None) if isinstance(a["date"], str) else a["date"].replace(tzinfo=None))).days <= 1
    ]
    
    print(f"Статей после фильтрации старше одного дня: {len(articles)}")

    if not articles:
        return []

    votes: Counter[str] = Counter()
    for mdl in MODELS_TO_USE:
        chosen = MODEL_OPTIONS[mdl](articles)
        for art in chosen:
            votes[art["url"]] += 1

    threshold = len(MODELS_TO_USE) // 2 + 1
    final = [a for a in articles if votes[a["url"]] >= threshold]
    print(f"Статей после фильтрации моделями: {len(final)}")

    for a in final:
        if hasattr(a["date"], "isoformat"):
            a["date"] = a["date"].isoformat()

    return final


async def collect_articles(limit_per_channel: int = 30,
                           outfile: Path | str = "articles.json") -> Path:
    async with TelegramClient("ai_news_parser", API_ID, API_HASH) as cl:
        raw = await _fetch(cl, limit=limit_per_channel)

    selected = _filter(raw)
    outfile = Path(outfile)
    outfile.write_text(json.dumps(selected, ensure_ascii=False, indent=2), "utf-8")
    return outfile

def get_articles(since: datetime) -> list[dict]:
    if not os.path.exists("articles.json"):
        return []

    with open("articles.json", "r", encoding="utf-8") as f:
        articles = json.load(f)

    if since:
        articles = [a for a in articles if a.get("date") >= since.isoformat()]

    return articles

if __name__ == "__main__":
    asyncio.run(collect_articles())
