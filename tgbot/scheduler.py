from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from storage.user_preferences import get_user_frequency
from handlers.news_sender import send_news_to_user
from parse_sources import filter_articles


def start_scheduler(bot):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(lambda: check_and_send(bot), "interval", minutes=60)
    scheduler.start()

async def check_and_send(bot):
    now = datetime.utcnow()
    articles = get_articles() 
    user_ids = get_all_user_ids()

    for user_id in user_ids:
        freq = get_user_frequency(user_id)
        last_time = last_sent.get(user_id, now - timedelta(days=10))

        if is_due(freq, now, last_time):
            article = articles[0] if articles else None
            if article:
                await send_news_to_user(bot, user_id, article)
                last_sent[user_id] = now

def is_due(freq, now, last_sent_time):
    if freq == "daily":
        return now - last_sent_time >= timedelta(days=1)
    if freq == "semiweekly":
        return now - last_sent_time >= timedelta(days=3)
    if freq == "weekly":
        return now - last_sent_time >= timedelta(days=7)
    return False
