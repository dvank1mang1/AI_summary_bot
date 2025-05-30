from __future__ import annotations

import json
from datetime import datetime, timedelta
from pathlib import Path

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from ai_summary_bot.parsing import collect_articles
from handlers.news_sender import send_news_to_user
from storage.user_preferences import get_user_frequency, get_all_user_ids

_last_sent: dict[int, datetime] = {}


def start_scheduler(bot):
    sched = AsyncIOScheduler()
    sched.add_job(lambda: check_and_send(bot), "interval", minutes=60)
    sched.start()


async def check_and_send(bot):
    now = datetime.utcnow()
    json_path = await collect_articles(limit_per_channel=30)
    pool = json.loads(Path(json_path).read_text("utf-8"))
    if not pool:
        return
    article = pool[0]
    for uid in get_all_user_ids():
        freq = get_user_frequency(uid)
        delta = now - _last_sent.get(uid, now - timedelta(days=10))
        if ready(freq, delta):
            await send_news_to_user(bot, uid, article)
            _last_sent[uid] = now


def ready(freq: str, delta: timedelta) -> bool:
    return (
        (freq == "daily" and delta >= timedelta(days=1))
        or (freq == "semiweekly" and delta >= timedelta(days=3))
        or (freq == "weekly" and delta >= timedelta(days=7))
    )
