from __future__ import annotations

import json
from datetime import datetime, timedelta
from pathlib import Path
import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from ai_summary_bot.parsing import collect_articles
from handlers.news_sender import send_news_to_user
from storage.user_preferences import get_user_frequency, get_user_size, get_all_user_ids, get_last_sent, set_last_sent
from ai_summary_bot.search import serpapi_search, format_snippets
from ai_summary_bot.parsing import get_articles

_last_sent: dict[int, datetime] = {}



def start_scheduler(bot):
    scheduler = AsyncIOScheduler(job_defaults={"misfire_grace_time": 60})
    
    scheduler.add_job(
        check_and_send,             
        "interval",
        minutes=1,
        args=[bot],                 
        id="check_and_send_job"
    )

    scheduler.add_job(
        run_parsing,               
        "interval",
        hours=6,
        id="run_parsing_job"
    )
    
    scheduler.start()

async def run_parsing():
    await collect_articles()


async def check_and_send(bot):
    now = datetime.utcnow()
    user_ids = get_all_user_ids()

    for user_id in user_ids:
        freq = get_user_frequency(user_id)
        size = get_user_size(user_id)
        last_time = get_last_sent(user_id) or (now - timedelta(days=10))

        if is_due(freq, now, last_time):
            articles = get_articles(since=last_time)

            for article in articles:
                if size == "extended":
                    serp_results = await serpapi_search(article["title"])
                    formatted_context = format_snippets(serp_results)
                    article["external_context"] = formatted_context
                else:
                    article["external_context"] = None

                await send_news_to_user(bot, user_id, article)

            set_last_sent(user_id, now)


def is_due(freq, now, last_sent_time):
    if freq == "daily":
        return now - last_sent_time >= timedelta(days=1)
    if freq == "semiweekly":
        return now - last_sent_time >= timedelta(days=3)
    if freq == "weekly":
        return now - last_sent_time >= timedelta(days=7)
    return False
